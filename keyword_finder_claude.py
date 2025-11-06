#!/usr/bin/env python3
"""
关键词相似度搜索 - Claude直接Prompt方案

优点：
- 超级简单
- 成本低（$0.06/查询）
- 不仅找相似词，还能分析为什么相似

适用：偶尔查询（每天<20次）
"""

import csv
from anthropic import Anthropic

class KeywordFinder:
    """使用Claude找相似关键词"""

    def __init__(self, api_key: str, keywords_csv_path: str):
        self.client = Anthropic(api_key=api_key)
        self.keywords_data = self._load_keywords(keywords_csv_path)

    def _load_keywords(self, csv_path: str) -> str:
        """加载关键词CSV为文本"""
        with open(csv_path, 'r', encoding='utf-8') as f:
            return f.read()

    def find_similar(self, query: str, top_k: int = 5) -> dict:
        """
        找到与query最相似的关键词

        参数:
            query: 查询关键词
            top_k: 返回多少个结果

        返回:
            {
                'similar_keywords': [...],
                'analysis': '...',
                'cost_estimate': 0.06
            }
        """
        prompt = f"""
我有以下关键词数据库（CSV格式）：

{self.keywords_data}

任务：找到与"{query}"最相似的{top_k}个关键词。

请以以下JSON格式返回：

{{
  "similar_keywords": [
    {{
      "keyword": "关键词",
      "search_volume": 数字,
      "competition": "竞争度",
      "similarity_reason": "为什么相似的简短说明",
      "relevance_score": 0-10的评分
    }}
  ],
  "analysis": "总体分析和建议",
  "keyword_group": "这组关键词的类别（如：宠物用品、智能设备等）"
}}

要求：
1. 考虑语义相似性（不仅仅是词语匹配）
2. 考虑搜索意图相似性
3. 按相关性评分排序（高到低）
"""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        # 估算成本
        input_tokens = len(self.keywords_data) // 4  # 粗略估算
        output_tokens = len(response.content[0].text) // 4
        cost = (input_tokens / 1_000_000 * 3) + (output_tokens / 1_000_000 * 15)

        return {
            'result': response.content[0].text,
            'cost_estimate': round(cost, 4),
            'input_tokens': input_tokens,
            'output_tokens': output_tokens
        }

    def group_keywords(self, keywords: list) -> dict:
        """
        将一组关键词分组归类

        参数:
            keywords: 关键词列表

        返回:
            分组结果
        """
        keywords_str = "\n".join([f"- {kw}" for kw in keywords])

        prompt = f"""
请将以下关键词按主题分组：

{keywords_str}

参考我的完整关键词数据库：
{self.keywords_data}

返回JSON格式：
{{
  "groups": [
    {{
      "group_name": "组名",
      "keywords": ["关键词1", "关键词2"],
      "description": "这组关键词的特点",
      "market_opportunity": "市场机会分析"
    }}
  ]
}}
"""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            'result': response.content[0].text,
            'cost_estimate': 0.08  # 粗略估算
        }

    def suggest_long_tail(self, base_keyword: str) -> dict:
        """
        基于主关键词建议长尾词

        参数:
            base_keyword: 主关键词

        返回:
            长尾词建议
        """
        prompt = f"""
基于我的关键词数据库：

{self.keywords_data}

主关键词："{base_keyword}"

任务：
1. 从数据库中找出相关的长尾关键词（3-5个词的组合）
2. 如果数据库中没有，基于市场洞察建议新的长尾词

返回JSON格式：
{{
  "existing_long_tail": [
    {{
      "keyword": "长尾词",
      "search_volume": "如果有",
      "opportunity": "为什么值得关注"
    }}
  ],
  "suggested_new_long_tail": [
    {{
      "keyword": "建议的新长尾词",
      "rationale": "为什么建议这个词",
      "estimated_volume": "估算的搜索量范围"
    }}
  ]
}}
"""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            'result': response.content[0].text,
            'cost_estimate': 0.06
        }


def main():
    """示例用法"""
    import sys
    import json

    if len(sys.argv) < 3:
        print("使用方法:")
        print(f"  python {sys.argv[0]} <keywords.csv> <查询词> [API_KEY]")
        print("\n示例:")
        print(f"  python {sys.argv[0]} product_keywords.csv 'pet feeder' sk-ant-xxx")
        print("\n如果不提供API_KEY，将从环境变量ANTHROPIC_API_KEY读取")
        return

    csv_path = sys.argv[1]
    query = sys.argv[2]
    api_key = sys.argv[3] if len(sys.argv) > 3 else None

    if not api_key:
        import os
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            print("❌ 错误：未提供API key，也未设置环境变量ANTHROPIC_API_KEY")
            return

    print(f"\n🔍 搜索与 '{query}' 相似的关键词...")
    print(f"📂 数据源: {csv_path}\n")

    finder = KeywordFinder(api_key, csv_path)

    # 查找相似关键词
    result = finder.find_similar(query, top_k=5)

    print(f"{'='*80}")
    print(f"结果：")
    print(f"{'='*80}\n")
    print(result['result'])
    print(f"\n{'='*80}")
    print(f"💰 估算成本: ${result['cost_estimate']:.4f}")
    print(f"📊 Tokens: 输入{result['input_tokens']:,} / 输出{result['output_tokens']:,}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
