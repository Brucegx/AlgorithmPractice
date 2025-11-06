#!/usr/bin/env python3
"""
Google Trends 数据获取演示
免费、无需API key、合法
"""

from pytrends.request import TrendReq
import time

def get_trends_data(keywords, timeframe='today 12-m'):
    """
    获取Google Trends数据

    Args:
        keywords: 关键词列表（最多5个）
        timeframe: 时间范围
            - 'today 12-m' (过去12个月)
            - 'today 3-m' (过去3个月)
            - 'today 5-y' (过去5年)
    """
    print(f"📊 正在获取关键词趋势: {keywords}")
    print(f"⏰ 时间范围: {timeframe}\n")

    try:
        # 初始化pytrends（模拟浏览器）
        pytrends = TrendReq(hl='en-US', tz=360)

        # 构建查询
        pytrends.build_payload(keywords, timeframe=timeframe, geo='US')

        # 获取随时间变化的兴趣度（0-100）
        interest_over_time = pytrends.interest_over_time()

        if interest_over_time.empty:
            print("❌ 没有找到数据")
            return None

        print("✅ 数据获取成功！\n")
        print("=" * 60)
        print("📈 过去12个月平均搜索热度:")
        print("=" * 60)

        for keyword in keywords:
            if keyword in interest_over_time.columns:
                avg_interest = interest_over_time[keyword].mean()
                max_interest = interest_over_time[keyword].max()
                min_interest = interest_over_time[keyword].min()
                recent_interest = interest_over_time[keyword].tail(4).mean()  # 最近4周

                print(f"\n关键词: {keyword}")
                print(f"  平均热度: {avg_interest:.1f}/100")
                print(f"  峰值热度: {max_interest:.1f}/100")
                print(f"  最低热度: {min_interest:.1f}/100")
                print(f"  近期热度: {recent_interest:.1f}/100 (最近4周)")

                # 趋势判断
                if recent_interest > avg_interest * 1.2:
                    print(f"  📈 趋势: 上升 (+{((recent_interest/avg_interest-1)*100):.1f}%)")
                elif recent_interest < avg_interest * 0.8:
                    print(f"  📉 趋势: 下降 ({((recent_interest/avg_interest-1)*100):.1f}%)")
                else:
                    print(f"  ➡️  趋势: 稳定")

        print("\n" + "=" * 60)

        # 获取相关话题（免费）
        print("\n🔍 相关话题:")
        print("=" * 60)
        try:
            related_topics = pytrends.related_topics()
            for keyword, data in related_topics.items():
                if 'rising' in data and not data['rising'].empty:
                    print(f"\n{keyword} - 上升趋势话题:")
                    print(data['rising'][['topic_title', 'value']].head(5).to_string(index=False))
        except Exception as e:
            print(f"相关话题获取失败（可能需要等待）: {e}")

        print("\n" + "=" * 60)

        # 获取相关查询
        print("\n🔎 相关搜索词:")
        print("=" * 60)
        try:
            related_queries = pytrends.related_queries()
            for keyword, data in related_queries.items():
                if 'rising' in data and not data['rising'].empty:
                    print(f"\n{keyword} - 上升搜索词:")
                    print(data['rising'][['query', 'value']].head(5).to_string(index=False))
        except Exception as e:
            print(f"相关搜索词获取失败: {e}")

        return interest_over_time

    except Exception as e:
        print(f"❌ 错误: {e}")
        return None


if __name__ == "__main__":
    # 示例：验证几个产品关键词
    test_keywords = ["smart pet feeder", "cat water fountain"]

    print("🚀 Google Trends 产品验证工具")
    print("=" * 60)
    print("📌 注意：")
    print("  - 完全免费，无需API key")
    print("  - 数据来自Google官方")
    print("  - 请求间隔建议 >2秒（避免被限流）")
    print("=" * 60)
    print()

    data = get_trends_data(test_keywords)

    if data is not None:
        print("\n✅ 完成！数据已获取")
        print(f"📊 数据点数量: {len(data)} 个时间点")
