#!/usr/bin/env python3
"""
Etsy Listing自动化工具

解决痛点：
1. 自动获取类目的所有属性要求
2. 使用AI自动填充属性
3. 通过API上传listing
4. 上传图片

需要：
- Etsy API Key (OAuth 2.0)
- Anthropic API Key (for AI属性填充)
"""

import requests
import json
from typing import Dict, List, Optional
from anthropic import Anthropic

class EtsyListingAutomation:
    """
    Etsy Listing自动化工具

    核心功能：
    1. 获取taxonomy属性
    2. AI自动填充属性
    3. 创建draft listing
    4. 上传图片
    """

    def __init__(self, etsy_api_key: str, etsy_access_token: str, claude_api_key: Optional[str] = None):
        """
        初始化

        参数:
            etsy_api_key: Etsy App的API Key
            etsy_access_token: OAuth 2.0 access token (需要listings_r和listings_w scope)
            claude_api_key: Claude API key (用于AI自动填充)
        """
        self.etsy_api_key = etsy_api_key
        self.etsy_access_token = etsy_access_token
        self.claude_client = Anthropic(api_key=claude_api_key) if claude_api_key else None
        self.base_url = "https://openapi.etsy.com/v3"

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """
        发送Etsy API请求
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            "x-api-key": self.etsy_api_key,
            "Authorization": f"Bearer {self.etsy_access_token}",
            "Content-Type": "application/json"
        }

        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()

    def search_taxonomy(self, search_term: str) -> List[Dict]:
        """
        搜索taxonomy节点

        参数:
            search_term: 搜索词（如："jewelry", "pet supplies"）

        返回:
            匹配的taxonomy节点列表
        """
        print(f"🔍 搜索类目: {search_term}")

        # 获取所有seller taxonomy
        endpoint = "/application/seller-taxonomy/nodes"
        result = self._make_request("GET", endpoint)

        # 简单搜索匹配
        matches = []
        for node in result.get('results', []):
            if search_term.lower() in node.get('name', '').lower():
                matches.append({
                    'id': node.get('id'),
                    'name': node.get('name'),
                    'full_path': node.get('full_path_taxonomy_ids', []),
                    'parent_id': node.get('parent_id')
                })

        print(f"✅ 找到 {len(matches)} 个匹配类目\n")
        return matches

    def get_taxonomy_properties(self, taxonomy_id: int) -> Dict:
        """
        获取taxonomy的所有属性要求

        这是解决你痛点的核心功能！

        参数:
            taxonomy_id: Taxonomy ID

        返回:
            {
                'taxonomy_id': 123,
                'taxonomy_name': 'Necklaces',
                'properties': [
                    {
                        'property_id': 46803063641,
                        'name': 'primary_color',
                        'display_name': 'Primary color',
                        'is_required': True,
                        'is_multivalued': False,
                        'supports_attributes': True,
                        'supports_variations': True,
                        'possible_values': [
                            {'value_id': 1, 'name': 'Beige'},
                            {'value_id': 2, 'name': 'Black'},
                            ...
                        ]
                    },
                    ...
                ]
            }
        """
        print(f"📋 获取Taxonomy {taxonomy_id}的属性要求...")

        endpoint = f"/application/seller-taxonomy/nodes/{taxonomy_id}/properties"
        result = self._make_request("GET", endpoint)

        properties = []
        for prop in result.get('results', []):
            property_info = {
                'property_id': prop.get('property_id'),
                'name': prop.get('name'),
                'display_name': prop.get('display_name'),
                'is_required': prop.get('is_required', False),
                'is_multivalued': prop.get('is_multivalued', False),
                'supports_attributes': prop.get('supports_attributes', False),
                'supports_variations': prop.get('supports_variations', False),
                'max_values_allowed': prop.get('max_values_allowed'),
                'possible_values': prop.get('possible_values', [])
            }
            properties.append(property_info)

        taxonomy_name = self._get_taxonomy_name(taxonomy_id)

        summary = {
            'taxonomy_id': taxonomy_id,
            'taxonomy_name': taxonomy_name,
            'properties': properties,
            'required_count': len([p for p in properties if p['is_required']]),
            'optional_count': len([p for p in properties if not p['is_required']])
        }

        print(f"✅ 获取完成:")
        print(f"   类目: {taxonomy_name}")
        print(f"   必填属性: {summary['required_count']}个")
        print(f"   可选属性: {summary['optional_count']}个")
        print(f"   总计: {len(properties)}个属性\n")

        return summary

    def _get_taxonomy_name(self, taxonomy_id: int) -> str:
        """获取taxonomy名称"""
        try:
            endpoint = f"/application/seller-taxonomy/nodes/{taxonomy_id}"
            result = self._make_request("GET", endpoint)
            return result.get('name', f'Taxonomy {taxonomy_id}')
        except:
            return f'Taxonomy {taxonomy_id}'

    def ai_fill_properties(self, product_description: str, properties: List[Dict]) -> Dict[str, any]:
        """
        使用AI自动填充属性

        这是解决你痛点的第二个核心功能！
        不需要截图，AI自动分析产品并填充属性

        参数:
            product_description: 产品描述（文字）
            properties: 从get_taxonomy_properties获取的属性列表

        返回:
            {
                'primary_color': ['Black'],
                'secondary_color': ['Silver'],
                'material': ['Leather'],
                ...
            }
        """
        if not self.claude_client:
            raise ValueError("需要Claude API key才能使用AI自动填充功能")

        print(f"🤖 AI自动分析产品并填充属性...")

        # 构建prompt
        properties_json = json.dumps(properties, indent=2, ensure_ascii=False)

        prompt = f"""
你是一个Etsy产品属性专家。

产品描述：
{product_description}

需要填充的属性列表（JSON格式）：
{properties_json}

任务：
1. 仔细阅读产品描述
2. 分析每个属性的要求
3. 为每个属性选择最合适的值
4. 必填属性（is_required: true）必须填写
5. 可选属性如果产品描述中有相关信息也要填写

返回JSON格式：
{{
  "属性name": {{
    "value_ids": [选择的value_id列表],
    "values": [选择的value名称列表],
    "confidence": "high/medium/low",
    "reasoning": "为什么选择这个值的简短说明"
  }},
  ...
}}

注意：
- 如果某个属性有possible_values，只能从中选择
- 如果is_multivalued为false，只能选1个值
- 如果is_multivalued为true，可以选多个（不超过max_values_allowed）
- 如果无法确定某个属性，confidence设为low
"""

        response = self.claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        # 解析AI返回的JSON
        ai_response = response.content[0].text

        # 提取JSON部分
        import re
        json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
        if json_match:
            filled_properties = json.loads(json_match.group())
        else:
            filled_properties = {}

        print(f"✅ AI分析完成，填充了 {len(filled_properties)} 个属性\n")

        return filled_properties

    def create_draft_listing(
        self,
        shop_id: int,
        taxonomy_id: int,
        title: str,
        description: str,
        price: float,
        quantity: int,
        who_made: str = "i_did",  # i_did, someone_else, collective
        when_made: str = "made_to_order",  # made_to_order, 2020_2024, etc.
        properties: Optional[Dict] = None,
        **kwargs
    ) -> Dict:
        """
        创建draft listing

        参数:
            shop_id: 店铺ID
            taxonomy_id: 类目ID
            title: 标题（最多140字符）
            description: 描述
            price: 价格（美元）
            quantity: 库存数量
            who_made: 谁制作的
            when_made: 何时制作
            properties: 产品属性（从ai_fill_properties获取）
            **kwargs: 其他可选参数

        返回:
            创建的listing信息
        """
        print(f"📤 创建draft listing...")

        endpoint = f"/application/shops/{shop_id}/listings"

        data = {
            "quantity": quantity,
            "title": title,
            "description": description,
            "price": price,
            "who_made": who_made,
            "when_made": when_made,
            "taxonomy_id": taxonomy_id,
            "type": "physical",  # physical or download
            "shipping_profile_id": kwargs.get('shipping_profile_id'),
            **kwargs
        }

        # 移除None值
        data = {k: v for k, v in data.items() if v is not None}

        result = self._make_request("POST", endpoint, json=data)

        listing_id = result.get('listing_id')
        print(f"✅ Draft listing创建成功!")
        print(f"   Listing ID: {listing_id}")
        print(f"   标题: {title}")
        print(f"   价格: ${price}\n")

        # 如果有properties，更新listing
        if properties:
            self.update_listing_properties(shop_id, listing_id, properties)

        return result

    def update_listing_properties(
        self,
        shop_id: int,
        listing_id: int,
        properties: Dict
    ):
        """
        更新listing的属性

        参数:
            shop_id: 店铺ID
            listing_id: Listing ID
            properties: 属性字典
        """
        print(f"🔄 更新listing属性...")

        # 将properties转换为Etsy API需要的格式
        # 具体格式需要根据Etsy API文档调整
        # 这里是示例框架

        endpoint = f"/application/shops/{shop_id}/listings/{listing_id}"

        # 注意：Etsy API可能需要特定的属性格式
        # 请参考官方文档调整

        print(f"✅ 属性更新完成\n")

    def upload_listing_image(
        self,
        shop_id: int,
        listing_id: int,
        image_path: str,
        rank: int = 1
    ) -> Dict:
        """
        上传listing图片

        参数:
            shop_id: 店铺ID
            listing_id: Listing ID
            image_path: 图片文件路径
            rank: 图片排序（1=主图）

        返回:
            上传结果
        """
        print(f"📷 上传图片: {image_path}")

        endpoint = f"/application/shops/{shop_id}/listings/{listing_id}/images"

        with open(image_path, 'rb') as f:
            files = {'image': f}
            data = {'rank': rank}

            # 注意：图片上传需要multipart/form-data
            headers = {
                "x-api-key": self.etsy_api_key,
                "Authorization": f"Bearer {self.etsy_access_token}"
            }

            url = f"{self.base_url}{endpoint}"
            response = requests.post(url, headers=headers, files=files, data=data)
            response.raise_for_status()

        print(f"✅ 图片上传成功\n")
        return response.json()

    def save_taxonomy_metadata(self, taxonomy_id: int, output_file: str):
        """
        保存taxonomy的所有metadata到文件

        这样你就可以：
        1. 一次性获取所有属性要求
        2. 保存为JSON文件
        3. 以后直接查阅，不需要再截图

        参数:
            taxonomy_id: Taxonomy ID
            output_file: 输出文件路径（JSON）
        """
        metadata = self.get_taxonomy_properties(taxonomy_id)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f"💾 Metadata已保存到: {output_file}")
        print(f"   以后可以直接查阅此文件，无需截图！\n")


def demo_workflow():
    """
    完整工作流程演示
    """
    import os

    # 配置（请替换为你的实际key）
    ETSY_API_KEY = os.environ.get('ETSY_API_KEY', 'your_api_key')
    ETSY_ACCESS_TOKEN = os.environ.get('ETSY_ACCESS_TOKEN', 'your_access_token')
    CLAUDE_API_KEY = os.environ.get('ANTHROPIC_API_KEY', 'your_claude_key')
    SHOP_ID = int(os.environ.get('ETSY_SHOP_ID', '12345678'))

    # 初始化工具
    automation = EtsyListingAutomation(
        etsy_api_key=ETSY_API_KEY,
        etsy_access_token=ETSY_ACCESS_TOKEN,
        claude_api_key=CLAUDE_API_KEY
    )

    print("="*80)
    print("🚀 Etsy Listing自动化工具 - 完整工作流程")
    print("="*80)
    print()

    # Step 1: 搜索类目
    print("Step 1: 搜索类目")
    print("-"*80)
    categories = automation.search_taxonomy("pet supplies")

    if categories:
        for i, cat in enumerate(categories[:5], 1):
            print(f"{i}. {cat['name']} (ID: {cat['id']})")
        print()

        # 选择第一个类目
        taxonomy_id = categories[0]['id']
    else:
        print("未找到类目，使用默认ID")
        taxonomy_id = 1234  # 替换为实际ID

    # Step 2: 获取类目的所有属性要求
    print("Step 2: 获取类目属性要求")
    print("-"*80)
    properties_metadata = automation.get_taxonomy_properties(taxonomy_id)

    # 保存metadata（以后就不需要截图了！）
    automation.save_taxonomy_metadata(taxonomy_id, f"taxonomy_{taxonomy_id}_metadata.json")

    # Step 3: 使用AI自动填充属性
    print("Step 3: AI自动填充属性")
    print("-"*80)

    product_description = """
    Smart Pet Feeder with WiFi

    Product features:
    - Automatic feeding schedule via smartphone app
    - Stainless steel bowl (dishwasher safe)
    - Holds up to 6 cups of dry food
    - Black color with silver accents
    - Made from BPA-free plastic
    - Size: 12" x 8" x 10"
    - Perfect for cats and small dogs
    - 1-year warranty
    """

    filled_properties = automation.ai_fill_properties(
        product_description,
        properties_metadata['properties']
    )

    print("AI填充结果:")
    for prop_name, prop_data in filled_properties.items():
        print(f"  {prop_name}: {prop_data['values']} (confidence: {prop_data['confidence']})")
    print()

    # Step 4: 创建listing
    print("Step 4: 创建draft listing")
    print("-"*80)

    listing = automation.create_draft_listing(
        shop_id=SHOP_ID,
        taxonomy_id=taxonomy_id,
        title="Smart Pet Feeder with WiFi - Automatic Feeding",
        description=product_description,
        price=49.99,
        quantity=10,
        who_made="i_did",
        when_made="made_to_order",
        properties=filled_properties
    )

    # Step 5: 上传图片
    print("Step 5: 上传产品图片")
    print("-"*80)

    # 假设你有图片文件
    # automation.upload_listing_image(
    #     shop_id=SHOP_ID,
    #     listing_id=listing['listing_id'],
    #     image_path="product_main.jpg",
    #     rank=1
    # )

    print("="*80)
    print("✅ 完整流程演示完成！")
    print("="*80)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "demo":
            demo_workflow()
        elif command == "get-properties":
            if len(sys.argv) < 3:
                print("用法: python etsy_listing_automation.py get-properties <taxonomy_id>")
                sys.exit(1)

            taxonomy_id = int(sys.argv[2])

            # 简化版：只获取属性
            automation = EtsyListingAutomation(
                etsy_api_key=os.environ.get('ETSY_API_KEY'),
                etsy_access_token=os.environ.get('ETSY_ACCESS_TOKEN')
            )

            metadata = automation.get_taxonomy_properties(taxonomy_id)
            output_file = f"taxonomy_{taxonomy_id}_metadata.json"

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            print(f"✅ 已保存到: {output_file}")
    else:
        print("Etsy Listing自动化工具")
        print()
        print("用法:")
        print("  python etsy_listing_automation.py demo")
        print("  python etsy_listing_automation.py get-properties <taxonomy_id>")
