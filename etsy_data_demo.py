#!/usr/bin/env python3
"""
Etsy数据获取演示
使用Etsy官方API v3（免费、合法）
"""

import requests
import json

class EtsyDataFetcher:
    """
    Etsy数据获取器

    前提：
    1. 注册Etsy开发者账号: https://www.etsy.com/developers/register
    2. 创建应用获取API Key
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://openapi.etsy.com/v3/application"

    def search_listings(self, keywords, limit=10):
        """
        搜索Etsy商品

        Args:
            keywords: 搜索关键词
            limit: 返回结果数量（最多100）

        Returns:
            商品列表数据
        """
        endpoint = f"{self.base_url}/listings/active"

        headers = {
            "x-api-key": self.api_key
        }

        params = {
            "keywords": keywords,
            "limit": limit,
            "sort_on": "score",  # 按相关性排序
            "includes": "Images,Shop,User"  # 包含图片、店铺、用户信息
        }

        try:
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ API请求失败: {e}")
            return None

    def analyze_competition(self, data):
        """
        分析竞争情况
        """
        if not data or 'results' not in data:
            print("❌ 无数据可分析")
            return

        listings = data['results']

        if not listings:
            print("❌ 没有找到相关商品")
            return

        print(f"\n📊 找到 {len(listings)} 个相关商品\n")
        print("=" * 80)

        prices = []
        total_favorites = 0

        for i, listing in enumerate(listings[:10], 1):
            title = listing.get('title', 'N/A')[:50]
            price = float(listing.get('price', {}).get('amount', 0)) / 100  # 价格单位是分
            currency = listing.get('price', {}).get('currency_code', 'USD')
            favorites = listing.get('num_favorers', 0)
            views = listing.get('views', 0)
            shop_name = listing.get('shop', {}).get('shop_name', 'N/A') if 'shop' in listing else 'N/A'

            prices.append(price)
            total_favorites += favorites

            print(f"\n{i}. {title}...")
            print(f"   价格: {currency} ${price:.2f}")
            print(f"   收藏: {favorites} | 浏览: {views}")
            print(f"   店铺: {shop_name}")

        # 统计分析
        print("\n" + "=" * 80)
        print("\n📈 市场分析:")
        print("-" * 80)

        if prices:
            avg_price = sum(prices) / len(prices)
            min_price = min(prices)
            max_price = max(prices)

            print(f"价格范围: ${min_price:.2f} - ${max_price:.2f}")
            print(f"平均价格: ${avg_price:.2f}")

            # 定价建议
            suggested_min = avg_price * 0.8
            suggested_max = avg_price * 1.2
            print(f"\n💡 定价建议: ${suggested_min:.2f} - ${suggested_max:.2f}")

        avg_favorites = total_favorites / len(listings) if listings else 0
        print(f"\n平均收藏数: {avg_favorites:.0f}")

        # 竞争度判断
        print("\n🎯 竞争度评估:")
        if len(listings) >= 100:
            print("  ⚠️  高竞争 - 搜索结果饱和")
        elif len(listings) >= 50:
            print("  ⚠️  中等竞争 - 需要差异化")
        else:
            print("  ✅ 低竞争 - 有机会")

        if avg_favorites > 1000:
            print("  📈 高需求 - 用户喜爱度高")
        elif avg_favorites > 100:
            print("  📊 中等需求")
        else:
            print("  📉 低需求 - 可能是小众市场")

        print("\n" + "=" * 80)


def demo_without_api():
    """
    无API Key的演示（说明数据结构）
    """
    print("🔧 Etsy API 使用说明")
    print("=" * 80)
    print("\n📋 获取API Key步骤:")
    print("1. 访问: https://www.etsy.com/developers/register")
    print("2. 创建开发者账号（免费）")
    print("3. 创建一个应用（App）")
    print("4. 获取 API Key（Keystring）")
    print("\n⚡ 使用方法:")
    print("```python")
    print("fetcher = EtsyDataFetcher(api_key='your_api_key_here')")
    print("data = fetcher.search_listings('handmade jewelry')")
    print("fetcher.analyze_competition(data)")
    print("```")
    print("\n" + "=" * 80)

    print("\n📊 可获取的数据类型:")
    print("-" * 80)
    print("✅ 商品标题、描述")
    print("✅ 价格（精确）")
    print("✅ 收藏数（favorites）")
    print("✅ 浏览数（views）")
    print("✅ 店铺信息")
    print("✅ 商品图片URL")
    print("✅ 标签（tags）")
    print("❌ 销量数据（Etsy不公开）")
    print("❌ 店铺收入（Etsy不公开）")

    print("\n" + "=" * 80)
    print("\n💰 替代方案（获取销量估算）:")
    print("-" * 80)
    print("1. eRank - 免费版可用，付费$6/月")
    print("   - 销量估算算法")
    print("   - 关键词搜索量")
    print("   - SEO分析")
    print("\n2. Marmalead - $19/月")
    print("   - 详细的市场数据")
    print("   - 竞争对手分析")
    print("\n3. 手动估算法:")
    print("   - 收藏数 ÷ 10 ≈ 月销量（经验公式）")
    print("   - 评论数 × 50 ≈ 总销量（经验公式）")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    # 演示模式（无API Key）
    demo_without_api()

    print("\n\n🔑 如果你有API Key，取消下面的注释来使用:")
    print("-" * 80)
    print("""
# api_key = "your_etsy_api_key_here"
# fetcher = EtsyDataFetcher(api_key)
#
# # 示例：搜索手工珠宝
# print("\\n🔍 搜索关键词: handmade jewelry")
# data = fetcher.search_listings("handmade jewelry", limit=20)
#
# if data:
#     fetcher.analyze_competition(data)
    """)
