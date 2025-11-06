#!/usr/bin/env python3
"""
AI驱动的电商产品策略分析工具

真正的价值：
1. 竞品差异化分析
2. 市场空白点识别
3. 具体的listing优化建议
4. 定价策略
5. 产品改进方向
"""

import csv
import json
import requests
from typing import Dict, List, Optional
from datetime import datetime
from collections import Counter

class ProductStrategyAnalyzer:
    """
    产品策略分析器 - 提供可执行的洞察和建议
    """

    def __init__(self, etsy_api_key: Optional[str] = None, anthropic_api_key: Optional[str] = None):
        self.etsy_api_key = etsy_api_key
        self.anthropic_api_key = anthropic_api_key
        self.etsy_base_url = "https://openapi.etsy.com/v3/application"

    def analyze_strategy(self, csv_path: str) -> Dict:
        """
        完整的策略分析
        """
        print(f"\n{'='*80}")
        print(f"🎯 产品策略分析报告")
        print(f"{'='*80}\n")

        # 1. 加载基础数据
        erank_data = self._load_erank_data(csv_path)
        if not erank_data:
            return {}

        product_name = erank_data[0].get('Product', 'Unknown Product')

        print(f"📦 产品: {product_name}\n")

        # 2. 获取竞品详细数据（如果有API）
        competitors = []
        if self.etsy_api_key:
            primary_kw = self._get_primary_keyword(erank_data)
            competitors = self._fetch_detailed_competitors(primary_kw)

        # 3. 核心分析模块
        insights = {}

        print(f"\n{'='*80}")
        print(f"📊 市场洞察分析")
        print(f"{'='*80}\n")

        # 3.1 市场空白分析
        insights['market_gaps'] = self._analyze_market_gaps(erank_data, competitors)

        # 3.2 竞品差异化分析
        insights['differentiation'] = self._analyze_differentiation(competitors)

        # 3.3 定价策略
        insights['pricing_strategy'] = self._analyze_pricing_strategy(competitors)

        # 3.4 关键词策略
        insights['keyword_strategy'] = self._analyze_keyword_strategy(erank_data, competitors)

        # 3.5 产品改进建议
        insights['product_improvements'] = self._analyze_product_opportunities(competitors)

        # 4. Listing优化建议（如果有AI API）
        if self.anthropic_api_key and competitors:
            insights['listing_optimization'] = self._generate_listing_optimization(
                product_name, erank_data, competitors
            )

        # 5. 综合行动计划
        insights['action_plan'] = self._generate_action_plan(insights)

        return insights

    def _load_erank_data(self, csv_path: str) -> List[Dict]:
        """加载eRank数据"""
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            print(f"❌ 加载失败: {e}")
            return []

    def _get_primary_keyword(self, data: List[Dict]) -> str:
        """获取主关键词"""
        for row in data:
            if row.get('Keyword Type', '').lower() == 'primary':
                return row.get('Keyword')
        return data[0].get('Keyword') if data else ""

    def _fetch_detailed_competitors(self, keyword: str, limit: int = 30) -> List[Dict]:
        """获取详细的竞品数据"""
        if not self.etsy_api_key:
            return []

        print(f"🔍 正在分析竞品市场...")

        endpoint = f"{self.etsy_base_url}/listings/active"
        headers = {"x-api-key": self.etsy_api_key}
        params = {
            "keywords": keyword,
            "limit": limit,
            "sort_on": "score"
        }

        try:
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get('results'):
                print(f"✅ 已获取 {len(data['results'])} 个竞品数据\n")
                return data['results']
            return []
        except Exception as e:
            print(f"❌ API错误: {e}\n")
            return []

    def _analyze_market_gaps(self, erank_data: List[Dict], competitors: List[Dict]) -> Dict:
        """
        市场空白分析 - 找到未被充分满足的需求
        """
        print(f"🔍 市场空白分析")
        print(f"{'-'*80}\n")

        gaps = {
            'underserved_keywords': [],
            'price_gaps': [],
            'feature_opportunities': []
        }

        # 1. 关键词空白分析
        print("1️⃣  关键词机会分析:")
        for kw_data in erank_data:
            keyword = kw_data.get('Keyword', '')
            volume = int(str(kw_data.get('Search Volume', '0')).replace(',', ''))
            competition = kw_data.get('Competition', '')

            # 高搜索量 + 低竞争 = 黄金机会
            if volume > 1000 and competition.lower() in ['low', 'medium']:
                opportunity_score = volume / (
                    {'low': 1, 'medium': 2, 'high': 4}.get(competition.lower(), 4)
                )
                gaps['underserved_keywords'].append({
                    'keyword': keyword,
                    'volume': volume,
                    'competition': competition,
                    'opportunity_score': opportunity_score
                })
                print(f"   ✅ {keyword}")
                print(f"      搜索量: {volume:,} | 竞争: {competition}")
                print(f"      💡 机会评分: {opportunity_score:.0f}")

        if not gaps['underserved_keywords']:
            print(f"   ⚠️  没有发现明显的关键词空白\n")
        else:
            print()

        # 2. 价格空白分析
        if competitors:
            print("2️⃣  价格空白分析:")
            prices = []
            for comp in competitors:
                price_data = comp.get('price', {})
                if price_data:
                    price = float(price_data.get('amount', 0)) / 100
                    prices.append(price)

            if prices:
                prices.sort()
                # 寻找价格区间的空白
                for i in range(len(prices) - 1):
                    gap = prices[i+1] - prices[i]
                    if gap > 20:  # 价格差距 > $20
                        gaps['price_gaps'].append({
                            'low': prices[i],
                            'high': prices[i+1],
                            'gap': gap,
                            'opportunity': f"${prices[i]:.2f} - ${prices[i+1]:.2f} 之间缺少产品"
                        })
                        print(f"   💰 价格空白: ${prices[i]:.2f} - ${prices[i+1]:.2f}")
                        print(f"      差距: ${gap:.2f}")

            if not gaps['price_gaps']:
                print(f"   ℹ️  价格分布较均匀，无明显空白\n")
            else:
                print()

        # 3. 功能/特性空白（通过标题分析）
        if competitors:
            print("3️⃣  产品特性分析:")
            feature_keywords = [
                'wifi', 'smart', 'automatic', 'timer', 'camera', 'app',
                'remote', 'voice', 'alexa', 'stainless', 'large', 'portable'
            ]

            feature_counts = {feat: 0 for feat in feature_keywords}

            for comp in competitors:
                title = comp.get('title', '').lower()
                for feat in feature_keywords:
                    if feat in title:
                        feature_counts[feat] += 1

            total_comps = len(competitors)
            underused_features = []

            for feat, count in feature_counts.items():
                percentage = (count / total_comps) * 100 if total_comps > 0 else 0
                if percentage < 30 and percentage > 0:  # 少于30%的竞品有此特性
                    underused_features.append({
                        'feature': feat,
                        'usage_rate': percentage,
                        'opportunity': f"只有{percentage:.0f}%竞品提到'{feat}'，可能是差异化点"
                    })
                    print(f"   🎯 '{feat}': 仅{percentage:.0f}%的竞品使用")

            gaps['feature_opportunities'] = underused_features

            if not underused_features:
                print(f"   ℹ️  竞品功能覆盖较全面\n")
            else:
                print()

        print(f"{'-'*80}\n")
        return gaps

    def _analyze_differentiation(self, competitors: List[Dict]) -> Dict:
        """
        差异化策略分析
        """
        print(f"🎨 差异化策略分析")
        print(f"{'-'*80}\n")

        if not competitors:
            print("⚠️  需要Etsy API数据才能进行差异化分析\n")
            return {}

        diff_strategies = {
            'price_positioning': [],
            'quality_indicators': [],
            'unique_angles': []
        }

        # 1. 价格定位策略
        print("1️⃣  价格定位建议:")
        prices = []
        favorites = []

        for comp in competitors[:10]:  # 分析前10个竞品
            price_data = comp.get('price', {})
            if price_data:
                price = float(price_data.get('amount', 0)) / 100
                fav = comp.get('num_favorers', 0)
                prices.append(price)
                favorites.append(fav)

        if prices:
            avg_price = sum(prices) / len(prices)
            high_end = sorted(prices)[-3:]  # 前3高价
            low_end = sorted(prices)[:3]    # 前3低价

            strategies = []

            # 策略A: 高端定位
            avg_high_fav = sum([favorites[prices.index(p)] for p in high_end if p in prices]) / 3
            strategies.append({
                'name': '高端定位',
                'price_range': f"${min(high_end):.2f} - ${max(high_end):.2f}",
                'rationale': '通过优质材料、精致工艺、独特设计justify高价',
                'avg_favorites': avg_high_fav,
                'pros': ['更高利润率', '品牌溢价', '目标高端客户'],
                'cons': ['市场较小', '需要优质产品', '营销成本高']
            })

            # 策略B: 性价比定位
            strategies.append({
                'name': '性价比定位',
                'price_range': f"${avg_price*0.8:.2f} - ${avg_price*0.95:.2f}",
                'rationale': '略低于平均价，突出"同样质量，更优价格"',
                'pros': ['快速获取市场份额', '容易吸引价格敏感客户'],
                'cons': ['利润率较低', '可能被认为低质']
            })

            # 策略C: 价值定位
            strategies.append({
                'name': '价值定位（推荐）',
                'price_range': f"${avg_price*1.1:.2f} - ${avg_price*1.3:.2f}",
                'rationale': '略高于平均价，通过独特卖点justify溢价',
                'pros': ['平衡利润和市场', '体现产品价值', '避免价格战'],
                'cons': ['需要清晰的差异化卖点']
            })

            for strat in strategies:
                print(f"\n   {strat['name']}: {strat['price_range']}")
                print(f"   理由: {strat['rationale']}")
                print(f"   优势: {', '.join(strat['pros'][:2])}")

            diff_strategies['price_positioning'] = strategies

        print(f"\n{'-'*80}\n")

        # 2. 质量指标分析
        print("2️⃣  如何体现产品质量:")

        quality_tips = [
            {
                'aspect': '专业摄影',
                'why': f"Top 10竞品平均有{sum([len(c.get('images', [])) for c in competitors[:10]])//10:.0f}张图片",
                'action': '至少7-10张高质量图片，包括使用场景、细节特写、尺寸对比'
            },
            {
                'aspect': '详细描述',
                'why': '客户无法实际触摸产品，需要通过文字建立信任',
                'action': '材料说明、尺寸规格、使用说明、保养建议'
            },
            {
                'aspect': '评论管理',
                'why': '社会证明是电商最重要的转化因素',
                'action': '前期通过朋友/家人获得初始评论，积极回复所有评论'
            },
            {
                'aspect': '品牌故事',
                'why': 'Etsy用户重视手工/独特/有故事的产品',
                'action': '在About页面讲述创作灵感、制作过程、品牌理念'
            }
        ]

        for tip in quality_tips:
            print(f"\n   📌 {tip['aspect']}")
            print(f"      为什么: {tip['why']}")
            print(f"      行动: {tip['action']}")

        diff_strategies['quality_indicators'] = quality_tips

        print(f"\n{'-'*80}\n")

        # 3. 独特角度
        print("3️⃣  可能的差异化角度:")

        unique_angles = [
            {
                'angle': '可持续/环保',
                'description': '使用环保材料、可回收包装',
                'target': '环保意识强的消费者',
                'example': '"Eco-friendly materials, plastic-free packaging"'
            },
            {
                'angle': '个性化定制',
                'description': '提供刻字、颜色选择、尺寸定制',
                'target': '寻找独特礼物的买家',
                'example': '"Personalized with your pet\'s name"'
            },
            {
                'angle': '本地制造',
                'description': '强调手工制作、本地生产',
                'target': '支持小企业的买家',
                'example': '"Handmade in [Your City], supporting local artisans"'
            },
            {
                'angle': '功能创新',
                'description': '独特的设计或功能改进',
                'target': '追求新奇的早期采用者',
                'example': '"First pet feeder with dual-camera monitoring"'
            }
        ]

        for angle in unique_angles:
            print(f"\n   🎯 {angle['angle']}")
            print(f"      策略: {angle['description']}")
            print(f"      目标客户: {angle['target']}")
            print(f"      示例文案: {angle['example']}")

        diff_strategies['unique_angles'] = unique_angles

        print(f"\n{'-'*80}\n")

        return diff_strategies

    def _analyze_pricing_strategy(self, competitors: List[Dict]) -> Dict:
        """定价策略详细分析"""
        print(f"💰 定价策略制定")
        print(f"{'-'*80}\n")

        if not competitors:
            print("⚠️  需要Etsy API数据\n")
            return {}

        prices = []
        price_fav_map = {}

        for comp in competitors:
            price_data = comp.get('price', {})
            if price_data:
                price = float(price_data.get('amount', 0)) / 100
                fav = comp.get('num_favorers', 0)
                prices.append(price)
                price_fav_map[price] = fav

        if not prices:
            return {}

        prices.sort()
        avg_price = sum(prices) / len(prices)

        # 价格-受欢迎度分析
        print("1️⃣  最优价格点分析:")

        # 计算每个价格区间的平均收藏数
        price_ranges = [
            (0, 30, 'Budget'),
            (30, 50, 'Mid-range'),
            (50, 80, 'Premium'),
            (80, 999, 'Luxury')
        ]

        for low, high, category in price_ranges:
            range_prices = [p for p in prices if low <= p < high]
            if range_prices:
                avg_fav = sum([price_fav_map.get(p, 0) for p in range_prices]) / len(range_prices)
                print(f"\n   {category} (${low}-${high})")
                print(f"   竞品数: {len(range_prices)}")
                print(f"   平均收藏: {avg_fav:.0f}")
                if avg_fav > 500:
                    print(f"   💡 这个价格区间很受欢迎！")

        # 建议定价
        print(f"\n2️⃣  推荐定价:")
        print(f"\n   基于市场数据，建议定价范围: ${avg_price*0.9:.2f} - ${avg_price*1.2:.2f}")
        print(f"\n   具体策略:")
        print(f"   • 新店铺/新产品: ${avg_price*0.85:.2f} (吸引首批客户)")
        print(f"   • 有初始评论后: ${avg_price*1.0:.2f} (市场平均价)")
        print(f"   • 建立品牌后: ${avg_price*1.15:.2f}+ (溢价)")

        print(f"\n{'-'*80}\n")

        return {
            'avg_market_price': avg_price,
            'recommended_range': (avg_price*0.9, avg_price*1.2),
            'price_ranges': price_ranges
        }

    def _analyze_keyword_strategy(self, erank_data: List[Dict], competitors: List[Dict]) -> Dict:
        """关键词策略"""
        print(f"🔑 关键词/SEO策略")
        print(f"{'-'*80}\n")

        # 1. 关键词优先级
        print("1️⃣  关键词优先级排序:")

        keyword_priority = []
        for kw_data in erank_data:
            keyword = kw_data.get('Keyword', '')
            volume = int(str(kw_data.get('Search Volume', '0')).replace(',', ''))
            competition = kw_data.get('Competition', 'Unknown')
            kw_type = kw_data.get('Keyword Type', '')

            # 计算优先级评分
            comp_score = {'Low': 3, 'Medium': 2, 'High': 1}.get(competition, 1)
            type_score = {'Primary': 3, 'Variant': 2, 'Long-tail': 2.5}.get(kw_type, 1)
            priority_score = (volume / 1000) * comp_score * type_score

            keyword_priority.append({
                'keyword': keyword,
                'volume': volume,
                'competition': competition,
                'type': kw_type,
                'priority_score': priority_score
            })

        keyword_priority.sort(key=lambda x: x['priority_score'], reverse=True)

        for i, kw in enumerate(keyword_priority[:5], 1):
            print(f"\n   {i}. {kw['keyword']}")
            print(f"      搜索量: {kw['volume']:,} | 竞争: {kw['competition']}")
            print(f"      优先级评分: {kw['priority_score']:.0f}")

            if i == 1:
                print(f"      💡 建议: 用作标题主关键词")
            elif i <= 3:
                print(f"      💡 建议: 在标题/前100字描述中使用")
            else:
                print(f"      💡 建议: 用于标签")

        # 2. 标题建议
        print(f"\n\n2️⃣  标题优化建议:")
        if keyword_priority:
            primary = keyword_priority[0]['keyword']
            secondary = keyword_priority[1]['keyword'] if len(keyword_priority) > 1 else ''

            print(f"\n   结构: [主关键词] - [差异化卖点] - [次关键词]")
            print(f"\n   示例:")
            print(f"   ❌ 差: 'Pet Feeder'")
            print(f"   ⚠️  可以: '{primary.title()}'")
            print(f"   ✅ 好: '{primary.title()} - Smart WiFi Enabled - {secondary.title()}'")
            print(f"\n   要点:")
            print(f"   • 前5个词最重要（Etsy算法权重高）")
            print(f"   • 包含2-3个关键词但保持自然")
            print(f"   • 突出独特卖点")

        # 3. 标签策略
        print(f"\n\n3️⃣  标签(Tags)策略:")
        print(f"\n   Etsy允许13个标签，建议分配:")
        print(f"   • 3-4个：高搜索量主关键词")
        print(f"   • 3-4个：长尾关键词")
        print(f"   • 2-3个：产品特性（如'wifi', 'automatic'）")
        print(f"   • 2-3个：目标客户（如'dog owner', 'pet parent'）")

        if competitors:
            # 分析竞品常用标签
            all_tags = []
            for comp in competitors[:20]:
                tags = comp.get('tags', [])
                all_tags.extend(tags)

            tag_freq = Counter(all_tags)
            top_tags = tag_freq.most_common(10)

            if top_tags:
                print(f"\n   竞品高频标签（参考）:")
                for tag, count in top_tags[:5]:
                    print(f"   • {tag} (使用{count}次)")

        print(f"\n{'-'*80}\n")

        return {'keyword_priority': keyword_priority}

    def _analyze_product_opportunities(self, competitors: List[Dict]) -> Dict:
        """产品改进机会分析"""
        print(f"🔧 产品改进机会")
        print(f"{'-'*80}\n")

        if not competitors:
            print("⚠️  需要Etsy API数据\n")
            return {}

        print("基于竞品分析，以下方面可能是改进机会:\n")

        opportunities = [
            {
                'area': '材料升级',
                'analysis': '如果竞品多用塑料，考虑使用不锈钢/陶瓷',
                'benefit': '更耐用、更高端、justify更高价格',
                'action': '在标题和描述中强调"Premium Stainless Steel"'
            },
            {
                'area': '尺寸选择',
                'analysis': '提供多个尺寸选项（小型犬/大型犬）',
                'benefit': '扩大目标市场，一个listing覆盖更多客户',
                'action': '创建变体(Variations)，让买家选择尺寸'
            },
            {
                'area': '配件/赠品',
                'analysis': '附赠额外价值（如清洁刷、说明书、贴纸）',
                'benefit': '提升感知价值，增加开箱体验',
                'action': '在图片中展示包装内容物'
            },
            {
                'area': '售后服务',
                'analysis': '提供30天无理由退货、1年保修',
                'benefit': '降低购买风险，提升转化率',
                'action': '在描述前部分突出"Hassle-free Returns"'
            }
        ]

        for opp in opportunities:
            print(f"💡 {opp['area']}")
            print(f"   分析: {opp['analysis']}")
            print(f"   好处: {opp['benefit']}")
            print(f"   行动: {opp['action']}\n")

        print(f"{'-'*80}\n")

        return {'opportunities': opportunities}

    def _generate_action_plan(self, insights: Dict) -> List[Dict]:
        """生成优先级行动计划"""
        print(f"📋 行动计划（按优先级）")
        print(f"{'='*80}\n")

        action_items = []

        # Phase 1: 产品开发前
        print("Phase 1: 产品开发前 (第1-2周)")
        print(f"{'-'*80}\n")

        phase1 = [
            {
                'priority': 'HIGH',
                'task': '确定差异化卖点',
                'detail': '从市场空白分析中选择1-2个核心差异点',
                'time': '2天',
                'output': '差异化定位文档'
            },
            {
                'priority': 'HIGH',
                'task': '制定定价策略',
                'detail': '根据定价分析确定初始价格和调价计划',
                'time': '1天',
                'output': '定价表'
            },
            {
                'priority': 'MEDIUM',
                'task': '产品原型/样品',
                'detail': '如果需要制作样品，确保体现差异化特性',
                'time': '1-2周',
                'output': '产品样品'
            }
        ]

        for item in phase1:
            marker = '🔴' if item['priority'] == 'HIGH' else '🟡'
            print(f"{marker} {item['task']}")
            print(f"   详情: {item['detail']}")
            print(f"   预计时间: {item['time']}")
            print(f"   交付物: {item['output']}\n")

        action_items.extend(phase1)

        # Phase 2: Listing创建
        print("\nPhase 2: Listing创建 (第3周)")
        print(f"{'-'*80}\n")

        phase2 = [
            {
                'priority': 'HIGH',
                'task': '专业摄影',
                'detail': '至少7-10张图片：主图、使用场景、细节、尺寸对比',
                'time': '2-3天',
                'output': '产品图片库'
            },
            {
                'priority': 'HIGH',
                'task': '优化标题',
                'detail': '使用关键词策略分析的前3个关键词',
                'time': '2小时',
                'output': 'SEO优化的标题'
            },
            {
                'priority': 'HIGH',
                'task': '撰写描述',
                'detail': '前100字包含核心关键词和卖点',
                'time': '4小时',
                'output': '产品描述'
            },
            {
                'priority': 'MEDIUM',
                'task': '设置标签',
                'detail': '13个标签，平衡热门词和长尾词',
                'time': '1小时',
                'output': '标签列表'
            }
        ]

        for item in phase2:
            marker = '🔴' if item['priority'] == 'HIGH' else '🟡'
            print(f"{marker} {item['task']}")
            print(f"   详情: {item['detail']}")
            print(f"   预计时间: {item['time']}\n")

        action_items.extend(phase2)

        # Phase 3: 上线和优化
        print("\nPhase 3: 上线和优化 (第4周起)")
        print(f"{'-'*80}\n")

        phase3 = [
            {
                'priority': 'HIGH',
                'task': '获取初始评论',
                'detail': '通过朋友/家人/首批客户优惠获得5-10个评论',
                'time': '2-4周',
                'output': '5+ 正面评论'
            },
            {
                'priority': 'MEDIUM',
                'task': '监控数据',
                'detail': '每周检查浏览量、收藏数、转化率',
                'time': '持续',
                'output': '数据分析表'
            },
            {
                'priority': 'MEDIUM',
                'task': 'A/B测试',
                'detail': '测试不同的主图、标题、价格',
                'time': '持续',
                'output': '优化报告'
            }
        ]

        for item in phase3:
            marker = '🔴' if item['priority'] == 'HIGH' else '🟡'
            print(f"{marker} {item['task']}")
            print(f"   详情: {item['detail']}")
            print(f"   预计时间: {item['time']}\n")

        action_items.extend(phase3)

        print(f"{'='*80}\n")

        return action_items


def main():
    import sys

    analyzer = ProductStrategyAnalyzer()

    if len(sys.argv) < 2:
        print("🎯 产品策略分析工具")
        print("=" * 80)
        print("\n这个工具提供:")
        print("  ✅ 市场空白分析")
        print("  ✅ 差异化策略建议")
        print("  ✅ 定价策略")
        print("  ✅ 关键词/SEO优化")
        print("  ✅ 具体行动计划")
        print("\n使用方法:")
        print(f"  python {sys.argv[0]} analyze <csv> [etsy_api_key]")
        print("\n示例:")
        print(f"  python {sys.argv[0]} analyze product_keywords.csv")
        print(f"  python {sys.argv[0]} analyze product_keywords.csv your_api_key")
        return

    command = sys.argv[1]

    if command == 'analyze':
        if len(sys.argv) < 3:
            print("❌ 请提供CSV文件路径")
            return

        csv_path = sys.argv[2]

        if len(sys.argv) >= 4:
            api_key = sys.argv[3]
            analyzer = ProductStrategyAnalyzer(etsy_api_key=api_key)
            print("✅ 将使用Etsy API进行深度分析\n")
        else:
            print("ℹ️  未提供Etsy API，将仅基于eRank数据分析\n")

        insights = analyzer.analyze_strategy(csv_path)

        # 保存结果
        if insights:
            output_json = csv_path.replace('.csv', '_strategy.json')
            with open(output_json, 'w', encoding='utf-8') as f:
                json.dump(insights, f, indent=2, ensure_ascii=False)

            print(f"\n💾 完整策略报告已保存: {output_json}")
            print(f"\n{'='*80}")
            print(f"✅ 分析完成！请根据行动计划执行")
            print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
