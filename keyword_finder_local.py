#!/usr/bin/env python3
"""
关键词相似度搜索 - 本地向量方案

优点：
- 完全免费（无API成本）
- 超快速（<0.1秒）
- 无限查询次数
- 数据私密（本地运行）

缺点：
- 需要安装sentence-transformers
- 首次下载模型（~500MB）
- 只返回相似度，不做分析

适用：频繁查询（每天>20次）
"""

import csv
import numpy as np
from typing import List, Dict
import json

# 首次运行需要安装：pip install sentence-transformers
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("❌ 需要安装 sentence-transformers")
    print("运行: pip install sentence-transformers")
    exit(1)


class LocalKeywordFinder:
    """本地向量搜索（完全免费）"""

    def __init__(self, keywords_csv_path: str, model_name: str = 'all-MiniLM-L6-v2'):
        """
        初始化

        参数:
            keywords_csv_path: CSV文件路径
            model_name: 模型名称
                - 'all-MiniLM-L6-v2' (推荐，轻量级，80MB)
                - 'all-mpnet-base-v2' (更准确，420MB)
        """
        print(f"📥 加载模型: {model_name}...")
        print(f"   (首次运行会下载模型，请稍候...)")

        # 加载模型（首次会下载）
        self.model = SentenceTransformer(model_name)

        print(f"✅ 模型加载完成")

        # 加载关键词数据
        print(f"📂 加载关键词数据: {keywords_csv_path}...")
        self.keywords_data = self._load_keywords(keywords_csv_path)
        self.keywords = [row['Keyword'] for row in self.keywords_data]

        # 生成embeddings
        print(f"🔄 生成向量embeddings ({len(self.keywords)}个关键词)...")
        self.embeddings = self.model.encode(
            self.keywords,
            show_progress_bar=True,
            convert_to_numpy=True
        )

        print(f"✅ 准备完成！可以开始搜索\n")

    def _load_keywords(self, csv_path: str) -> List[Dict]:
        """加载CSV数据"""
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def find_similar(self, query: str, top_k: int = 5, threshold: float = 0.3) -> List[Dict]:
        """
        找到最相似的关键词

        参数:
            query: 查询词
            top_k: 返回数量
            threshold: 相似度阈值（0-1，建议0.3-0.5）

        返回:
            [
                {
                    'keyword': '关键词',
                    'similarity': 0.85,
                    'data': {...原始数据...}
                }
            ]
        """
        # 生成查询的embedding
        query_embedding = self.model.encode([query], convert_to_numpy=True)

        # 计算余弦相似度
        # 归一化
        query_norm = query_embedding / np.linalg.norm(query_embedding)
        embeddings_norm = self.embeddings / np.linalg.norm(self.embeddings, axis=1, keepdims=True)

        # 余弦相似度
        similarities = np.dot(embeddings_norm, query_norm.T).flatten()

        # 过滤低于阈值的
        valid_indices = np.where(similarities >= threshold)[0]

        if len(valid_indices) == 0:
            return []

        # 排序
        top_indices = valid_indices[similarities[valid_indices].argsort()[::-1]][:top_k]

        # 构建结果
        results = []
        for idx in top_indices:
            results.append({
                'keyword': self.keywords[idx],
                'similarity': float(similarities[idx]),
                'data': self.keywords_data[idx]
            })

        return results

    def find_similar_batch(self, queries: List[str], top_k: int = 5) -> Dict[str, List[Dict]]:
        """
        批量查询（更高效）

        参数:
            queries: 查询词列表
            top_k: 每个查询返回数量

        返回:
            {
                'query1': [结果],
                'query2': [结果],
                ...
            }
        """
        # 批量生成embeddings（更快）
        query_embeddings = self.model.encode(queries, convert_to_numpy=True)

        results = {}
        for i, query in enumerate(queries):
            query_embedding = query_embeddings[i:i+1]

            # 计算相似度
            query_norm = query_embedding / np.linalg.norm(query_embedding)
            embeddings_norm = self.embeddings / np.linalg.norm(self.embeddings, axis=1, keepdims=True)
            similarities = np.dot(embeddings_norm, query_norm.T).flatten()

            # 排序
            top_indices = similarities.argsort()[::-1][:top_k]

            results[query] = [
                {
                    'keyword': self.keywords[idx],
                    'similarity': float(similarities[idx]),
                    'data': self.keywords_data[idx]
                }
                for idx in top_indices
            ]

        return results

    def cluster_keywords(self, n_clusters: int = 5) -> Dict:
        """
        自动聚类关键词

        参数:
            n_clusters: 分成几组

        返回:
            聚类结果
        """
        from sklearn.cluster import KMeans

        print(f"🔄 聚类分析 ({n_clusters}组)...")

        # KMeans聚类
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = kmeans.fit_predict(self.embeddings)

        # 组织结果
        clusters = {}
        for i in range(n_clusters):
            cluster_indices = np.where(labels == i)[0]
            clusters[f"Group {i+1}"] = [
                {
                    'keyword': self.keywords[idx],
                    'data': self.keywords_data[idx]
                }
                for idx in cluster_indices
            ]

        return clusters

    def save_embeddings(self, output_path: str):
        """保存embeddings（避免重复计算）"""
        np.savez(
            output_path,
            embeddings=self.embeddings,
            keywords=self.keywords
        )
        print(f"✅ Embeddings已保存: {output_path}")

    def load_embeddings(self, input_path: str):
        """加载已保存的embeddings"""
        data = np.load(input_path, allow_pickle=True)
        self.embeddings = data['embeddings']
        self.keywords = data['keywords'].tolist()
        print(f"✅ Embeddings已加载: {input_path}")


def main():
    """示例用法"""
    import sys

    if len(sys.argv) < 3:
        print("使用方法:")
        print(f"  python {sys.argv[0]} <keywords.csv> <查询词> [top_k]")
        print("\n示例:")
        print(f"  python {sys.argv[0]} product_keywords.csv 'pet feeder' 5")
        print("\n首次运行会下载模型（~80MB），请稍候...")
        return

    csv_path = sys.argv[1]
    query = sys.argv[2]
    top_k = int(sys.argv[3]) if len(sys.argv) > 3 else 5

    print(f"\n{'='*80}")
    print(f"🚀 本地向量搜索 - 完全免费")
    print(f"{'='*80}\n")

    # 初始化（首次会下载模型）
    finder = LocalKeywordFinder(csv_path)

    # 查找相似关键词
    print(f"🔍 搜索与 '{query}' 最相似的 {top_k} 个关键词...\n")

    results = finder.find_similar(query, top_k=top_k)

    # 显示结果
    print(f"{'='*80}")
    print(f"结果：")
    print(f"{'='*80}\n")

    if not results:
        print("❌ 没有找到相似的关键词（可能阈值太高）")
    else:
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['keyword']}")
            print(f"   相似度: {result['similarity']:.3f}")

            # 显示数据
            for key, value in result['data'].items():
                if key != 'Keyword':
                    print(f"   {key}: {value}")
            print()

    print(f"{'='*80}")
    print(f"💰 成本: $0 (完全免费)")
    print(f"⚡ 查询速度: <0.1秒")
    print(f"♾️  查询次数: 无限")
    print(f"{'='*80}\n")

    # 演示批量查询
    if len(results) > 0:
        print(f"\n💡 演示：批量查询")
        print(f"{'-'*80}\n")

        batch_queries = [query, results[0]['keyword']]
        batch_results = finder.find_similar_batch(batch_queries, top_k=3)

        for q, res in batch_results.items():
            print(f"查询: '{q}'")
            for r in res:
                print(f"  - {r['keyword']} (相似度: {r['similarity']:.3f})")
            print()


if __name__ == "__main__":
    main()
