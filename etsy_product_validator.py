#!/usr/bin/env python3
"""
Etsy产品验证工具 - 混合数据源版本

数据源：
1. eRank数据（手动导入CSV）
2. Etsy API（自动获取）
3. Google Trends（自动获取）

使用方法：
1. 在eRank查询关键词，导出数据
2. 运行此脚本分析
"""

import csv
import json
from datetime import datetime
from typing import Dict, List, Optional

class ProductValidator:
    """
    产品验证器 - 混合多个数据源
    """

    def __init__(self, etsy_api_key: Optional[str] = None):
        self.etsy_api_key = etsy_api_key

    def load_erank_data(self, csv_path: str) -> List[Dict]:
        """
        加载从eRank导出的CSV数据

        CSV格式示例：
        Keyword,Search Volume,Competition,Clicks,Engagement
        smart pet feeder,12500,High,850,6.8%
        """
        print(f"📂 加载eRank数据: {csv_path}")

        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)

            print(f"✅ 成功加载 {len(data)} 条关键词数据\n")
            return data

        except FileNotFoundError:
            print(f"❌ 文件不存在: {csv_path}")
            return []
        except Exception as e:
            print(f"❌ 加载失败: {e}")
            return []

    def analyze_keywords(self, erank_data: List[Dict]) -> Dict:
        """
        分析eRank关键词数据
        """
        if not erank_data:
            return {}

        print("=" * 80)
        print("📊 关键词分析报告")
        print("=" * 80)
        print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # 分析每个关键词
        results = []

        for i, row in enumerate(erank_data, 1):
            keyword = row.get('Keyword', 'N/A')
            search_volume = row.get('Search Volume', '0')
            competition = row.get('Competition', 'Unknown')
            clicks = row.get('Clicks', '0')
            engagement = row.get('Engagement', '0%')

            # 转换数据类型
            try:
                volume = int(search_volume.replace(',', ''))
            except:
                volume = 0

            try:
                click_count = int(clicks.replace(',', ''))
            except:
                click_count = 0

            # 计算评分
            score = self._calculate_keyword_score(volume, competition, click_count)

            result = {
                'keyword': keyword,
                'volume': volume,
                'competition': competition,
                'clicks': click_count,
                'engagement': engagement,
                'score': score
            }
            results.append(result)

            # 打印单个关键词分析
            print(f"{i}. {keyword}")
            print(f"   搜索量: {volume:,}/月")
            print(f"   竞争度: {competition}")
            print(f"   点击数: {click_count:,}")
            print(f"   参与度: {engagement}")
            print(f"   综合评分: {score}/10")

            # 推荐判断
            if score >= 7:
                print(f"   ✅ 推荐 - 高潜力关键词")
            elif score >= 5:
                print(f"   ⚠️  考虑 - 中等潜力")
            else:
                print(f"   ❌ 不推荐 - 潜力较低")
            print()

        # 综合统计
        print("=" * 80)
        print("\n📈 综合统计:")
        print("-" * 80)

        total_volume = sum(r['volume'] for r in results)
        avg_volume = total_volume / len(results) if results else 0
        high_potential = len([r for r in results if r['score'] >= 7])
        medium_potential = len([r for r in results if 5 <= r['score'] < 7])

        print(f"总搜索量: {total_volume:,}/月")
        print(f"平均搜索量: {avg_volume:,.0f}/月")
        print(f"\n关键词机会:")
        print(f"  ✅ 高潜力: {high_potential} 个")
        print(f"  ⚠️  中潜力: {medium_potential} 个")
        print(f"  ❌ 低潜力: {len(results) - high_potential - medium_potential} 个")

        print("\n" + "=" * 80)

        # 推荐关键词列表
        recommended = sorted([r for r in results if r['score'] >= 7],
                           key=lambda x: x['score'], reverse=True)

        if recommended:
            print("\n🎯 推荐主攻关键词:")
            print("-" * 80)
            for i, rec in enumerate(recommended[:5], 1):
                print(f"{i}. {rec['keyword']}")
                print(f"   评分: {rec['score']}/10 | 搜索量: {rec['volume']:,}")

        print("\n" + "=" * 80)

        return {
            'keywords': results,
            'stats': {
                'total_volume': total_volume,
                'avg_volume': avg_volume,
                'high_potential': high_potential,
                'medium_potential': medium_potential
            },
            'recommended': recommended
        }

    def _calculate_keyword_score(self, volume: int, competition: str, clicks: int) -> float:
        """
        计算关键词评分（0-10）

        考虑因素：
        - 搜索量（越高越好）
        - 竞争度（中等最佳）
        - 点击数（越高越好）
        """
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

    def create_csv_template(self, output_path: str = "erank_template.csv"):
        """
        创建CSV模板，供用户填写eRank数据
        """
        headers = ['Keyword', 'Search Volume', 'Competition', 'Clicks', 'Engagement']
        sample_data = [
            ['smart pet feeder', '12500', 'High', '850', '6.8%'],
            ['cat water fountain', '8900', 'Medium', '620', '7.0%'],
            ['dog treat dispenser', '5600', 'Low', '380', '6.8%'],
        ]

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(sample_data)

        print(f"✅ CSV模板已创建: {output_path}")
        print(f"\n使用方法:")
        print(f"1. 在eRank查询关键词")
        print(f"2. 复制数据到此CSV文件")
        print(f"3. 运行: python {__file__} analyze {output_path}")


def main():
    """
    主函数 - 命令行接口
    """
    import sys

    validator = ProductValidator()

    if len(sys.argv) < 2:
        print("🔧 Etsy产品验证工具")
        print("=" * 80)
        print("\n使用方法:")
        print(f"  python {sys.argv[0]} template        # 创建CSV模板")
        print(f"  python {sys.argv[0]} analyze <csv>   # 分析eRank数据")
        print("\n示例:")
        print(f"  python {sys.argv[0]} template")
        print(f"  python {sys.argv[0]} analyze erank_data.csv")
        print("\n" + "=" * 80)
        return

    command = sys.argv[1]

    if command == 'template':
        validator.create_csv_template()

    elif command == 'analyze':
        if len(sys.argv) < 3:
            print("❌ 请提供CSV文件路径")
            print(f"示例: python {sys.argv[0]} analyze erank_data.csv")
            return

        csv_path = sys.argv[2]
        erank_data = validator.load_erank_data(csv_path)

        if erank_data:
            results = validator.analyze_keywords(erank_data)

            # 保存JSON结果
            output_json = csv_path.replace('.csv', '_results.json')
            with open(output_json, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            print(f"\n💾 详细结果已保存: {output_json}")

    else:
        print(f"❌ 未知命令: {command}")
        print(f"可用命令: template, analyze")


if __name__ == "__main__":
    main()
