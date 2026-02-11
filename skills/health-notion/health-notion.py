#!/usr/bin/env python3
"""
Health Notion - 个人健康管理Notion同步工具
直接使用Notion API，无需额外CLI工具
"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime
from pathlib import Path


# 环境变量
NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "")
NOTION_HEALTH_PAGE_ID = os.environ.get("NOTION_HEALTH_PAGE_ID", "3039de7521f8809894b4cdee8b678021")


def notion_headers():
    """返回Notion API请求头"""
    return {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }


def append_block_to_page(page_id, content):
    """向页面追加文本块"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    data = {
        "children": [{
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": content}}]
            }
        }]
    }
    response = requests.patch(url, headers=notion_headers(), json=data)
    return response.json()


def create_database_entry(database_id, properties):
    """在数据库中创建新条目"""
    url = "https://api.notion.com/v1/pages"
    data = {
        "parent": {"database_id": database_id},
        "properties": properties
    }
    response = requests.post(url, headers=notion_headers(), json=data)
    return response.json()


def query_database(database_id, filter_obj=None):
    """查询数据库"""
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    data = {"filter": filter_obj} if filter_obj else {}
    response = requests.post(url, headers=notion_headers(), json=data)
    return response.json()


def get_page_content(page_id):
    """获取页面内容"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.get(url, headers=notion_headers())
    return response.json()


def get_full_profile():
    """获取完整个人档案"""
    try:
        result = get_page_content(NOTION_HEALTH_PAGE_ID)
        
        if result.get("object") == "error":
            return f"❌ 查询失败: {result.get('message')}"
        
        records = result.get("results", [])
        if not records:
            return "暂无档案信息"
        
        # 提取文本内容
        content_lines = ["# 📋 个人健康档案"]
        content_lines.append(f"⏰ 查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        for block in records[:30]:  # 只取前30个块
            if block.get("type") == "paragraph":
                rich_text = block.get("paragraph", {}).get("rich_text", [])
                for text in rich_text:
                    if text.get("type") == "text":
                        content = text.get("text", {}).get("content", "")
                        if content.strip():
                            content_lines.append(content)
        
        return '\n'.join(content_lines)
    except Exception as e:
        return f"❌ 查询失败: {str(e)}"


def sync_user_to_notion():
    """同步USER.md健康信息到Notion病症档案"""
    try:
        user_path = Path("/home/admin/.openclaw/workspace/USER.md")
        if not user_path.exists():
            return "❌ 错误: USER.md文件不存在", None

        with open(user_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 转换为Markdown格式
        markdown_content = f"# 📋 个人健康档案\n\n"
        markdown_content += f"⏰ 同步时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        markdown_content += content

        # 添加到页面
        result = append_block_to_page(NOTION_HEALTH_PAGE_ID, markdown_content)

        if result.get("object") == "error":
            return f"❌ 同步失败: {result.get('message')}", None

        # 查询完整档案返回
        profile = get_full_profile()
        return "✅ 成功同步USER.md到Notion病症档案", profile

    except Exception as e:
        return f"❌ 同步失败: {str(e)}", None


def init_profile():
    """初始化/更新个人健康档案（直接写入页面内容）"""
    try:
        # 先删除页面所有内容
        result = get_page_content(NOTION_HEALTH_PAGE_ID)
        blocks = result.get("results", [])
        
        for block in blocks:
            block_id = block.get("id")
            url = f"https://api.notion.com/v1/blocks/{block_id}"
            requests.delete(url, headers=notion_headers())
        
        # 构建完整档案内容
        content = """## 基础信息

| 项目 | 数据 |
|-----|------|
| 身高 | 165cm |
| 体重 | 76kg |
| BMI | 27.9（超重） |
| 目标体重 | 65kg以下 |

## 健康状况

- **2型糖尿病**（确诊）
- **糖尿病肾病**（蛋白尿 711.61 mg/g，需要定期监测肾功能）
- 脂肪肝
- 高血压(低压高值)

## 当前用药

- 胰岛素（三餐前）+ 胰岛素（睡前）
- 胰激肽原酶肠溶片
- 非诺贝特软胶囊
- 普罗布考片
- 沙库巴曲缬沙坦钠片

## 血糖控制目标

- **空腹血糖**: 4.4-7.0 mmol/L
- **餐后血糖**: <10.0 mmol/L

## 饮食原则

### ✅ 可以吃（优先级高）
- 低GI主食（荞麦、燕麦、糙米、红豆）
- 绿叶蔬菜（菠菜、芹菜、西兰花）
- 优质蛋白（鱼类、禽类、蛋清）
- 富含Omega-3的鱼类

### ⚠️ 需要限制
- 高糖水果（荔枝、芒果、西瓜）
- 精制碳水（白米、白面、糯米）
- 高盐食物
- 饱和脂肪

### ❌ 避免
- 甜食、含糖饮料
- 加工肉制品
- 高嘌呤食物（针对肾病）
- 酒精
"""

        # 添加到页面
        result = append_block_to_page(NOTION_HEALTH_PAGE_ID, content)
        
        if result.get("object") == "error":
            return f"❌ 初始化失败: {result.get('message')}", None
        
        # 查询并返回完整档案
        profile = get_full_profile()
        return "✅ 个人健康档案初始化完成", profile
        
    except Exception as e:
        return f"❌ 初始化失败: {str(e)}", None


def add_glucose(value, note=""):
    """添加血糖记录"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    glucose_db_id = os.environ.get("NOTION_GLUCOSE_DB_ID", "")

    if not glucose_db_id:
        return "⚠️ 请设置NOTION_GLUCOSE_DB_ID环境变量"

    properties = {
        "Name": {"title": [{"text": {"content": f"血糖 {timestamp}"}}]},
        "血糖值": {"number": float(value)},
        "时间": {"date": {"start": timestamp}},
        "备注": {"rich_text": [{"text": {"content": note}}]}
    }

    result = create_database_entry(glucose_db_id, properties)

    if result.get("object") == "error":
        return f"❌ 添加失败: {result.get('message')}"

    return f"✅ 血糖记录已添加: {value} mmol/L"


def get_glucose(days=7):
    """查询血糖记录"""
    glucose_db_id = os.environ.get("NOTION_GLUCOSE_DB_ID", "")

    if not glucose_db_id:
        return "⚠️ 请设置NOTION_GLUCOSE_DB_ID环境变量"

    # 计算日期范围
    from datetime import timedelta
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

    filter_obj = {
        "property": "时间",
        "date": {"on_or_after": start_date}
    }

    result = query_database(glucose_db_id, filter_obj)

    if result.get("object") == "error":
        return f"❌ 查询失败: {result.get('message')}"

    # 格式化输出
    records = result.get("results", [])
    if not records:
        return "暂无血糖记录"

    output = ["📊 血糖记录 (最近7天)\n"]
    for record in records:
        props = record.get("properties", {})
        value = props.get("血糖值", {}).get("number", "N/A")
        time = props.get("时间", {}).get("date", {}).get("start", "N/A")
        note = props.get("备注", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")
        output.append(f"• {time}: {value} mmol/L {note}")

    return '\n'.join(output)


def add_meal(meal_type, food):
    """添加饮食记录"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    meal_db_id = os.environ.get("NOTION_MEAL_DB_ID", "")

    if not meal_db_id:
        return "⚠️ 请设置NOTION_MEAL_DB_ID环境变量"

    properties = {
        "Name": {"title": [{"text": {"content": f"{meal_type} {timestamp}"}}]},
        "餐饮类型": {"select": {"name": meal_type}},
        "食物": {"rich_text": [{"text": {"content": food}}]},
        "时间": {"date": {"start": timestamp}}
    }

    result = create_database_entry(meal_db_id, properties)

    if result.get("object") == "error":
        return f"❌ 添加失败: {result.get('message')}"

    return f"✅ 饮食记录已添加: {meal_type} - {food}"


def add_weight(weight):
    """添加体重记录"""
    timestamp = datetime.now().strftime('%Y-%m-%d')
    weight_db_id = os.environ.get("NOTION_WEIGHT_DB_ID", "")

    if not weight_db_id:
        return "⚠️ 请设置NOTION_WEIGHT_DB_ID环境变量"

    # 计算BMI (假设身高165cm)
    height = 1.65
    bmi = round(float(weight) / (height * height), 1)

    properties = {
        "Name": {"title": [{"text": {"content": f"体重 {timestamp}"}}]},
        "体重": {"number": float(weight)},
        "BMI": {"number": bmi},
        "日期": {"date": {"start": timestamp}}
    }

    result = create_database_entry(weight_db_id, properties)

    if result.get("object") == "error":
        return f"❌ 添加失败: {result.get('message')}"

    return f"✅ 体重记录已添加: {weight} kg (BMI: {bmi})"


def add_medication(drug, dosage):
    """添加用药记录"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    med_db_id = os.environ.get("NOTION_MEDICATION_DB_ID", "")

    if not med_db_id:
        return "⚠️ 请设置NOTION_MEDICATION_DB_ID环境变量"

    properties = {
        "Name": {"title": [{"text": {"content": f"{drug} {timestamp}"}}]},
        "药物": {"rich_text": [{"text": {"content": drug}}]},
        "剂量": {"rich_text": [{"text": {"content": dosage}}]},
        "时间": {"date": {"start": timestamp}}
    }

    result = create_database_entry(med_db_id, properties)

    if result.get("object") == "error":
        return f"❌ 添加失败: {result.get('message')}"

    return f"✅ 用药记录已添加: {drug} - {dosage}"


def get_report():
    """生成健康报告"""
    report = ["# 🏥 健康报告", f"⏰ 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]

    # 完整档案
    report.append("\n" + "="*30)
    profile = get_full_profile()
    report.append(profile)

    return '\n'.join(report)


def main():
    parser = argparse.ArgumentParser(description='🏥 Health Notion - 个人健康管理工具')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # sync命令
    parser_sync = subparsers.add_parser('sync', help='同步数据到Notion')
    parser_sync.add_argument('target', choices=['user'], help='同步目标')

    # init命令
    parser_init = subparsers.add_parser('init', help='初始化健康档案')
    
    # add命令
    parser_add = subparsers.add_parser('add', help='添加记录')
    parser_add.add_argument('type', choices=['glucose', 'meal', 'weight', 'medication'], help='记录类型')
    parser_add.add_argument('value', help='记录值')
    parser_add.add_argument('--note', default='', help='备注')

    # get命令
    parser_get = subparsers.add_parser('get', help='查询记录')
    parser_get.add_argument('type', choices=['glucose', 'profile'], help='查询类型')
    parser_get.add_argument('--days', type=int, default=7, help='查询天数')

    # report命令
    subparsers.add_parser('report', help='生成健康报告')

    args = parser.parse_args()

    if not NOTION_API_KEY:
        print("❌ 错误: 请设置NOTION_API_KEY环境变量")
        sys.exit(1)

    if args.command == 'sync':
        if args.target == 'user':
            msg, profile = sync_user_to_notion()
            print(msg)
            if profile:
                print("\n" + "="*50)
                print(profile)

    elif args.command == 'init':
        msg, profile = init_profile()
        print(msg)
        if profile:
            print("\n" + "="*50)
            print(profile)

    elif args.command == 'add':
        if args.type == 'glucose':
            print(add_glucose(args.value, args.note))
        elif args.type == 'meal':
            print(add_meal(args.value, args.note))
        elif args.type == 'weight':
            print(add_weight(args.value))
        elif args.type == 'medication':
            print(add_medication(args.value, args.note))

    elif args.command == 'get':
        if args.type == 'glucose':
            print(get_glucose(args.days))
        elif args.type == 'profile':
            print(get_full_profile())

    elif args.command == 'report':
        print(get_report())

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
