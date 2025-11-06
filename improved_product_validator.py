#!/usr/bin/env python3
"""
改进版：支持多关键词产品验证

CSV格式：一个产品的所有相关关键词在一个文件
"""

import csv
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
import time

class ImprovedProductValidator:
    """
    改进的产品验证器

    支持：
    1. 一个产品多个关键词（主关键词+变体）
    2. 自动调用Etsy API补充竞品数据
    3. 综合评分和推荐
    """

    def __init__(self, etsy_api_key: Optional[str] = None):
        self.etsy_api_key = etsy_api_key
        self.etsy_base_url = "https://openapi.etsy.com/v3/application"

    def analyze_product(self, csv_path: str) -> Dict:
        """
        分析一个产品（包含多个关键词）

        CSV格式：
        Product,Keyword,Search Volume,Competition,Clicks,Engagement,Keyword Type
        Smart Pet Feeder,smart pet feeder,12500,High,850,6.8%,Primary
        Smart Pet Feeder,automatic pet feeder,8900,Medium,620,7.0%,Variant
        Smart Pet Feeder,wifi pet feeder,5600,Low,380,6.8%,Variant
        """
        print(f"\n{'='*80}")
        print(f"📦 产品验证报告")
        print(f"{'='*80}")
        print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # 加载数据
        keywords_data = self._load_csv(csv_path)
        if not keywords_data:
            return {}

        # 按产品分组
        products = self._group_by_product(keywords_data)

        all_results = {}

        for product_name, keywords in products.items():
            print(f"\n{'='*80}")
            print(f"📦 产品: {product_name}")
            print(f"{'='*80}\n")

            # 1. eRank关键词分析
            keyword_analysis = self._analyze_keywords(keywords)

            # 2. Etsy API竞品分析（如果有API key）
            etsy_analysis = None
            if self.etsy_api_key:
                primary_keyword = self._get_primary_keyword(keywords)
                if primary_keyword:
                    print(f"\n🔍 正在从Etsy获取竞品数据...")
                    etsy_analysis = self._fetch_etsy_competitors(primary_keyword)

            # 3. 综合评分
            final_score = self._calculate_product_score(
                keyword_analysis,
                etsy_analysis
            )

            # 4. 生成建议
            recommendations = self._generate_recommendations(
                product_name,
                keyword_analysis,
                etsy_analysis,
                final_score
            )

            all_results[product_name] = {
                'keywords': keyword_analysis,
                'etsy_competitors': etsy_analysis,
                'final_score': final_score,
                'recommendations': recommendations
            }

        return all_results

    def _load_csv(self, csv_path: str) -> List[Dict]:
        """加载CSV数据"""
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            print(f"✅ 成功加载 {len(data)} 条关键词数据")
            return data
        except Exception as e:
            print(f"❌ 加载失败: {e}")
            return []

    def _group_by_product(self, data: List[Dict]) -> Dict[str, List[Dict]]:
        """按产品名称分组"""
        products = {}
        for row in data:
            product = row.get('Product', 'Unknown')
            if product not in products:
                products[product] = []
            products[product].append(row)
        return products

    def _get_primary_keyword(self, keywords: List[Dict]) -> Optional[str]:
        """获取主关键词"""
        for kw in keywords:
            if kw.get('Keyword Type', '').lower() == 'primary':
                return kw.get('Keyword')
        # 如果没有标记primary，返回第一个
        return keywords[0].get('Keyword') if keywords else None

    def _analyze_keywords(self, keywords: List[Dict]) -> Dict:
        """分析关键词组"""
        print(f"📊 关键词分析 ({len(keywords)} 个关键词):")
        print(f"{'-'*80}\n")

        results = []
        total_volume = 0
        primary_keyword = None

        for i, kw_data in enumerate(keywords, 1):
            keyword = kw_data.get('Keyword', 'N/A')
            search_volume = kw_data.get('Search Volume', '0')
            competition = kw_data.get('Competition', 'Unknown')
            clicks = kw_data.get('Clicks', '0')
            engagement = kw_data.get('Engagement', '0%')
            kw_type = kw_data.get('Keyword Type', 'Variant')

            # 转换数据
            try:
                volume = int(str(search_volume).replace(',', ''))
            except:
                volume = 0

            try:
                click_count = int(str(clicks).replace(',', ''))
            except:
                click_count = 0

            total_volume += volume

            # 计算评分
            score = self._calculate_keyword_score(volume, competition, click_count)

            result = {
                'keyword': keyword,
                'type': kw_type,
                'volume': volume,
                'competition': competition,
                'clicks': click_count,
                'engagement': engagement,
                'score': score
            }
            results.append(result)

            # 标记主关键词
            marker = "🎯" if kw_type.lower() == 'primary' else "  "

            print(f"{marker} {i}. {keyword} ({kw_type})")
            print(f"     搜索量: {volume:,}/月 | 竞争: {competition}")
            print(f"     点击数: {click_count:,} | 参与度: {engagement}")
            print(f"     评分: {score}/10", end="")

            if score >= 7:
                print(f" ✅ 高潜力")
            elif score >= 5:
                print(f" ⚠️  中等")
            else:
                print(f" ❌ 较低")
            print()

        # 统计
        print(f"\n{'-'*80}")
        print(f"📈 关键词组统计:")
        print(f"   总搜索量: {total_volume:,}/月")
        print(f"   平均搜索量: {total_volume//len(results):,}/月")
        high_potential = len([r for r in results if r['score'] >= 7])
        print(f"   高潜力关键词: {high_potential}/{len(results)}")

        return {
            'keywords': results,
            'total_volume': total_volume,
            'avg_volume': total_volume // len(results) if results else 0,
            'high_potential_count': high_potential
        }

    def _fetch_etsy_competitors(self, keyword: str, limit: int = 20) -> Optional[Dict]:
        """
        从Etsy API获取竞品数据

        采集数据：
        1. 前20个竞品的基本信息
        2. 价格分布
        3. 收藏数统计
        4. 销量估算
        """
        if not self.etsy_api_key:
            return None

        endpoint = f"{self.etsy_base_url}/listings/active"
        headers = {"x-api-key": self.etsy_api_key}
        params = {
            "keywords": keyword,
            "limit": limit,
            "sort_on": "score",
            "includes": "Images,Shop"
        }

        try:
            response = requests.get(endpoint, headers=headers, params=params)

            if response.status_code == 429:
                print("⚠️  API限流，等待60秒...")
                time.sleep(60)
                return None

            response.raise_for_status()
            data = response.json()

            if not data.get('results'):
                print("❌ 没有找到竞品")
                return None

            # 分析竞品
            return self._analyze_competitors(data['results'])

        except Exception as e:
            print(f"❌ Etsy API错误: {e}")
            return None

    def _analyze_competitors(self, listings: List[Dict]) -> Dict:
        """
        分析Etsy竞品数据

        返回：
        - 价格分布
        - 收藏数统计
        - 销量估算
        - 竞争程度
        """
        print(f"\n{'='*80}")
        print(f"🏪 Etsy竞品分析 ({len(listings)} 个商品)")
        print(f"{'='*80}\n")

        prices = []
        favorites = []
        shops = set()
        tags_counter = {}

        for listing in listings:
            # 价格（单位：分）
            price_data = listing.get('price', {})
            if price_data:
                price = float(price_data.get('amount', 0)) / 100
                prices.append(price)

            # 收藏数
            fav_count = listing.get('num_favorers', 0)
            favorites.append(fav_count)

            # 店铺
            shop = listing.get('shop', {})
            if shop:
                shops.add(shop.get('shop_name'))

            # 标签
            tags = listing.get('tags', [])
            for tag in tags:
                tags_counter[tag] = tags_counter.get(tag, 0) + 1

        # 统计分析
        analysis = {
            'competitor_count': len(listings),
            'unique_shops': len(shops),
            'price_stats': self._calculate_price_stats(prices),
            'favorites_stats': self._calculate_favorites_stats(favorites),
            'sales_estimate': self._estimate_sales(favorites),
            'top_tags': sorted(tags_counter.items(), key=lambda x: x[1], reverse=True)[:10]
        }

        # 打印报告
        self._print_competitor_report(analysis)

        return analysis

    def _calculate_price_stats(self, prices: List[float]) -> Dict:
        """计算价格统计"""
        if not prices:
            return {}

        sorted_prices = sorted(prices)
        return {
            'min': sorted_prices[0],
            'max': sorted_prices[-1],
            'avg': sum(prices) / len(prices),
            'median': sorted_prices[len(sorted_prices)//2],
            'q1': sorted_prices[len(sorted_prices)//4],
            'q3': sorted_prices[len(sorted_prices)*3//4]
        }

    def _calculate_favorites_stats(self, favorites: List[int]) -> Dict:
        """计算收藏数统计"""
        if not favorites:
            return {}

        sorted_fav = sorted(favorites, reverse=True)
        return {
            'max': sorted_fav[0],
            'avg': sum(favorites) / len(favorites),
            'median': sorted_fav[len(sorted_fav)//2],
            'top_10_avg': sum(sorted_fav[:10]) / min(10, len(sorted_fav))
        }

    def _estimate_sales(self, favorites: List[int]) -> Dict:
        """
        估算销量

        公式：月销量 ≈ 收藏数 ÷ 10
        """
        if not favorites:
            return {}

        sorted_fav = sorted(favorites, reverse=True)

        return {
            'top_seller_monthly': sorted_fav[0] // 10 if sorted_fav else 0,
            'avg_seller_monthly': (sum(favorites) // len(favorites)) // 10 if favorites else 0,
            'top_10_avg_monthly': (sum(sorted_fav[:10]) // min(10, len(sorted_fav))) // 10 if sorted_fav else 0,
            'note': '基于"收藏数÷10"公式估算，误差±50%'
        }

    def _print_competitor_report(self, analysis: Dict):
        """打印竞品分析报告"""
        price_stats = analysis.get('price_stats', {})
        fav_stats = analysis.get('favorites_stats', {})
        sales = analysis.get('sales_estimate', {})

        print(f"💰 价格分析:")
        if price_stats:
            print(f"   价格区间: ${price_stats['min']:.2f} - ${price_stats['max']:.2f}")
            print(f"   平均价格: ${price_stats['avg']:.2f}")
            print(f"   中位数: ${price_stats['median']:.2f}")
            print(f"   建议定价: ${price_stats['q1']:.2f} - ${price_stats['q3']:.2f}")

        print(f"\n❤️  收藏数分析:")
        if fav_stats:
            print(f"   Top商品收藏: {fav_stats['max']:,}")
            print(f"   平均收藏: {fav_stats['avg']:.0f}")
            print(f"   Top10平均: {fav_stats['top_10_avg']:.0f}")

        print(f"\n📊 销量估算:")
        if sales:
            print(f"   Top卖家月销: ~{sales['top_seller_monthly']} 单")
            print(f"   平均月销: ~{sales['avg_seller_monthly']} 单")
            print(f"   Top10平均月销: ~{sales['top_10_avg_monthly']} 单")
            print(f"   ⚠️  {sales['note']}")

        print(f"\n🏪 竞争情况:")
        print(f"   竞品数量: {analysis['competitor_count']}")
        print(f"   独立店铺: {analysis['unique_shops']}")

        if analysis['competitor_count'] > 50:
            print(f"   竞争程度: 🔴 高")
        elif analysis['competitor_count'] > 20:
            print(f"   竞争程度: 🟡 中")
        else:
            print(f"   竞争程度: 🟢 低")

        print(f"\n🏷️  热门标签:")
        for tag, count in analysis['top_tags'][:5]:
            print(f"   - {tag} ({count}次)")

    def _calculate_keyword_score(self, volume: int, competition: str, clicks: int) -> float:
        """计算关键词评分（同之前）"""
        score = 0.0

        # 搜索量评分（0-4分）
        if volume >= 10000:
            score += 4.0
        elif volume >= 5000:
            score += 3.5
        elif volume >= 1000:
            score += 3.0
        elif volume >= 500:
            score += 2.0
        elif volume >= 100:
            score += 1.0

        # 竞争度评分（0-3分）
        comp_lower = competition.lower()
        if 'low' in comp_lower:
            score += 3.0
        elif 'medium' in comp_lower or 'moderate' in comp_lower:
            score += 2.5
        elif 'high' in comp_lower:
            score += 1.5

        # 点击数评分（0-3分）
        if clicks >= 1000:
            score += 3.0
        elif clicks >= 500:
            score += 2.5
        elif clicks >= 100:
            score += 2.0
        elif clicks >= 50:
            score += 1.5
        elif clicks >= 10:
            score += 1.0

        return round(score, 1)

    def _calculate_product_score(self, keyword_analysis: Dict, etsy_analysis: Optional[Dict]) -> Dict:
        """
        计算产品综合评分（0-10分）
        """
        print(f"\n{'='*80}")
        print(f"🎯 综合评分")
        print(f"{'='*80}\n")

        scores = {}

        # 1. 关键词评分（基于eRank数据）
        kw_score = 0
        if keyword_analysis:
            avg_kw_score = sum(k['score'] for k in keyword_analysis['keywords']) / len(keyword_analysis['keywords'])
            total_volume = keyword_analysis['total_volume']

            # 搜索量权重
            volume_score = min(total_volume / 5000, 5.0)  # 最高5分

            # 综合关键词评分
            kw_score = (avg_kw_score * 0.6 + volume_score * 0.4)

        scores['keyword_score'] = round(kw_score, 1)
        print(f"📊 关键词评分: {scores['keyword_score']}/10")

        # 2. 市场需求评分（基于Etsy数据）
        demand_score = 0
        if etsy_analysis:
            fav_stats = etsy_analysis.get('favorites_stats', {})
            sales_est = etsy_analysis.get('sales_estimate', {})

            # 收藏数反映需求
            avg_fav = fav_stats.get('avg', 0)
            if avg_fav > 1000:
                demand_score = 5.0
            elif avg_fav > 500:
                demand_score = 4.0
            elif avg_fav > 100:
                demand_score = 3.0
            elif avg_fav > 50:
                demand_score = 2.0
            else:
                demand_score = 1.0

        scores['demand_score'] = round(demand_score, 1)
        print(f"❤️  市场需求: {scores['demand_score']}/5")

        # 3. 竞争程度评分（越低越好）
        competition_score = 0
        if etsy_analysis:
            competitor_count = etsy_analysis.get('competitor_count', 0)

            # 竞品越少越好
            if competitor_count < 20:
                competition_score = 5.0  # 低竞争
            elif competitor_count < 50:
                competition_score = 3.5  # 中竞争
            elif competitor_count < 100:
                competition_score = 2.0  # 高竞争
            else:
                competition_score = 1.0  # 极高竞争

        scores['competition_score'] = round(competition_score, 1)
        print(f"🏪 竞争程度: {scores['competition_score']}/5 (越高越好)")

        # 4. 盈利潜力评分
        profit_score = 0
        if etsy_analysis:
            price_stats = etsy_analysis.get('price_stats', {})
            sales_est = etsy_analysis.get('sales_estimate', {})

            avg_price = price_stats.get('avg', 0)
            avg_monthly_sales = sales_est.get('avg_seller_monthly', 0)

            # 估算月收入
            estimated_revenue = avg_price * avg_monthly_sales

            if estimated_revenue > 2000:
                profit_score = 5.0
            elif estimated_revenue > 1000:
                profit_score = 4.0
            elif estimated_revenue > 500:
                profit_score = 3.0
            elif estimated_revenue > 200:
                profit_score = 2.0
            else:
                profit_score = 1.0

        scores['profit_score'] = round(profit_score, 1)
        print(f"💰 盈利潜力: {scores['profit_score']}/5")

        # 总分
        total = scores['keyword_score'] * 0.4 + scores['demand_score'] * 0.2 + scores['competition_score'] * 0.2 + scores['profit_score'] * 0.2
        scores['total_score'] = round(total, 1)

        print(f"\n{'='*80}")
        print(f"🏆 总分: {scores['total_score']}/10")

        if scores['total_score'] >= 7.5:
            print(f"评级: ⭐⭐⭐⭐⭐ 强烈推荐")
        elif scores['total_score'] >= 6.0:
            print(f"评级: ⭐⭐⭐⭐ 推荐")
        elif scores['total_score'] >= 4.5:
            print(f"评级: ⭐⭐⭐ 谨慎考虑")
        else:
            print(f"评级: ⭐⭐ 不推荐")

        return scores

    def _generate_recommendations(self, product_name: str, keyword_analysis: Dict,
                                 etsy_analysis: Optional[Dict], final_score: Dict) -> List[str]:
        """生成行动建议"""
        print(f"\n{'='*80}")
        print(f"💡 行动建议")
        print(f"{'='*80}\n")

        recommendations = []

        total_score = final_score['total_score']

        if total_score >= 7.5:
            recommendations.append("✅ 强烈推荐进入此市场")
        elif total_score >= 6.0:
            recommendations.append("✅ 推荐进入，但需注意差异化")
        elif total_score >= 4.5:
            recommendations.append("⚠️  谨慎考虑，市场机会有限")
        else:
            recommendations.append("❌ 不推荐，考虑其他产品")

        # 关键词建议
        if keyword_analysis:
            best_keywords = sorted(keyword_analysis['keywords'],
                                 key=lambda x: x['score'], reverse=True)[:3]
            recommendations.append(f"\n📊 主攻关键词:")
            for kw in best_keywords:
                recommendations.append(f"   - {kw['keyword']} (评分: {kw['score']}/10)")

        # 定价建议
        if etsy_analysis:
            price_stats = etsy_analysis.get('price_stats', {})
            if price_stats:
                q1 = price_stats.get('q1', 0)
                q3 = price_stats.get('q3', 0)
                recommendations.append(f"\n💰 定价建议: ${q1:.2f} - ${q3:.2f}")

        # 竞争策略
        competition_score = final_score.get('competition_score', 0)
        if competition_score < 3:
            recommendations.append("\n🏪 竞争策略: 市场竞争激烈，必须强调差异化")
            recommendations.append("   - 独特设计/功能")
            recommendations.append("   - 优质客户服务")
            recommendations.append("   - 专业产品摄影")
        else:
            recommendations.append("\n🏪 竞争策略: 市场竞争适中，注重SEO优化")

        # 打印建议
        for rec in recommendations:
            print(rec)

        return recommendations

    def create_improved_template(self, output_path: str = "product_keywords.csv"):
        """
        创建改进的CSV模板

        一个产品的所有关键词在一起
        """
        headers = ['Product', 'Keyword', 'Search Volume', 'Competition', 'Clicks', 'Engagement', 'Keyword Type']

        sample_data = [
            # 产品1：智能宠物喂食器
            ['Smart Pet Feeder', 'smart pet feeder', '12500', 'High', '850', '6.8%', 'Primary'],
            ['Smart Pet Feeder', 'automatic pet feeder', '8900', 'Medium', '620', '7.0%', 'Variant'],
            ['Smart Pet Feeder', 'wifi pet feeder', '5600', 'Low', '380', '6.8%', 'Variant'],
            ['Smart Pet Feeder', 'pet feeder with camera', '3200', 'Medium', '210', '6.5%', 'Long-tail'],

            # 产品2：猫咪饮水机
            ['Cat Water Fountain', 'cat water fountain', '18000', 'High', '1200', '6.7%', 'Primary'],
            ['Cat Water Fountain', 'automatic cat water bowl', '4500', 'Medium', '320', '7.1%', 'Variant'],
            ['Cat Water Fountain', 'pet water dispenser', '6700', 'Medium', '450', '6.7%', 'Variant'],
        ]

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(sample_data)

        print(f"✅ 改进的CSV模板已创建: {output_path}\n")
        print(f"说明：")
        print(f"  - Product列：产品名称（多个关键词用相同的产品名）")
        print(f"  - Keyword Type：")
        print(f"    * Primary - 主关键词（用于Etsy API查询）")
        print(f"    * Variant - 变体关键词")
        print(f"    * Long-tail - 长尾关键词")
        print(f"\n从eRank获取数据：")
        print(f"  1. 在eRank搜索每个关键词")
        print(f"  2. 记录: Search Volume, Competition, Clicks, Engagement")
        print(f"  3. 填入CSV对应列")


def main():
    import sys

    validator = ImprovedProductValidator()

    if len(sys.argv) < 2:
        print("🔧 改进版 Etsy 产品验证工具")
        print("=" * 80)
        print("\n特性:")
        print("  ✅ 支持一个产品多个关键词")
        print("  ✅ 自动调用Etsy API获取竞品数据")
        print("  ✅ 综合评分和详细建议")
        print("\n使用方法:")
        print(f"  python {sys.argv[0]} template               # 创建CSV模板")
        print(f"  python {sys.argv[0]} analyze <csv>          # 分析产品")
        print(f"  python {sys.argv[0]} analyze <csv> <api_key>  # 使用Etsy API")
        print("\n示例:")
        print(f"  python {sys.argv[0]} template")
        print(f"  python {sys.argv[0]} analyze products.csv")
        print(f"  python {sys.argv[0]} analyze products.csv your_etsy_api_key")
        print("\n" + "=" * 80)
        return

    command = sys.argv[1]

    if command == 'template':
        validator.create_improved_template()

    elif command == 'analyze':
        if len(sys.argv) < 3:
            print("❌ 请提供CSV文件路径")
            return

        csv_path = sys.argv[2]

        # 可选：Etsy API key
        if len(sys.argv) >= 4:
            api_key = sys.argv[3]
            validator = ImprovedProductValidator(etsy_api_key=api_key)
            print(f"✅ 将使用Etsy API获取竞品数据\n")
        else:
            print(f"ℹ️  未提供Etsy API key，将只分析eRank数据")
            print(f"   要使用Etsy API，请运行: python {sys.argv[0]} analyze {csv_path} <api_key>\n")

        results = validator.analyze_product(csv_path)

        # 保存结果
        if results:
            output_json = csv_path.replace('.csv', '_full_report.json')
            with open(output_json, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n💾 完整报告已保存: {output_json}")


if __name__ == "__main__":
    main()
