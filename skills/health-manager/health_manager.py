#!/usr/bin/env python3
"""
私人医生级健康管理管家 - 核心逻辑模块
"""

import os
import json
import datetime
from typing import Dict, List, Optional, Any

class HealthManager:
    """健康管理核心类"""
    
    def __init__(self, data_dir: str = "/opt/moltbot/skills/health-manager/data"):
        self.data_dir = data_dir
        self.user_profile_path = os.path.join(data_dir, "user_profile.json")
        self.health_records_path = os.path.join(data_dir, "health_records.json")
        self.advice_history_path = os.path.join(data_dir, "advice_history.json")
        
        # 确保数据目录存在
        os.makedirs(data_dir, exist_ok=True)
        
        # 初始化数据文件（如果不存在）
        self._init_data_files()
    
    def _init_data_files(self):
        """初始化数据文件"""
        if not os.path.exists(self.user_profile_path):
            with open(self.user_profile_path, 'w') as f:
                json.dump({
                    "basic_info": {
                        "age": None,
                        "gender": None,
                        "height": None,
                        "weight": None,
                        "blood_type": None
                    },
                    "medical_history": [],
                    "allergies": [],
                    "medications": [],
                    "family_history": [],
                    "lifestyle": {
                        "exercise_frequency": None,
                        "sleep_hours": None,
                        "diet_preferences": None,
                        "smoking": False,
                        "alcohol": False
                    }
                }, f, indent=2, ensure_ascii=False)
        
        if not os.path.exists(self.health_records_path):
            with open(self.health_records_path, 'w') as f:
                json.dump([], f, indent=2, ensure_ascii=False)
        
        if not os.path.exists(self.advice_history_path):
            with open(self.advice_history_path, 'w') as f:
                json.dump([], f, indent=2, ensure_ascii=False)
    
    def update_user_profile(self, profile_data: Dict[str, Any]) -> bool:
        """更新用户健康档案"""
        try:
            with open(self.user_profile_path, 'r') as f:
                profile = json.load(f)
            
            # 递归更新字典
            def deep_update(original, updates):
                for key, value in updates.items():
                    if isinstance(value, dict) and key in original:
                        deep_update(original[key], value)
                    else:
                        original[key] = value
            
            deep_update(profile, profile_data)
            
            with open(self.user_profile_path, 'w') as f:
                json.dump(profile, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"更新用户档案失败: {e}")
            return False
    
    def get_user_profile(self) -> Dict[str, Any]:
        """获取用户健康档案"""
        try:
            with open(self.user_profile_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"读取用户档案失败: {e}")
            return {}
    
    def add_health_record(self, record: Dict[str, Any]) -> bool:
        """添加健康记录"""
        try:
            with open(self.health_records_path, 'r') as f:
                records = json.load(f)
            
            # 添加时间戳
            record['timestamp'] = datetime.datetime.now().isoformat()
            record['id'] = len(records) + 1
            
            records.append(record)
            
            with open(self.health_records_path, 'w') as f:
                json.dump(records, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"添加健康记录失败: {e}")
            return False
    
    def get_health_records(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取健康记录（最近的）"""
        try:
            with open(self.health_records_path, 'r') as f:
                records = json.load(f)
            
            # 按时间倒序排序
            records.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            return records[:limit]
        except Exception as e:
            print(f"读取健康记录失败: {e}")
            return []
    
    def generate_health_advice(self, query: str, context: Optional[str] = None) -> Dict[str, Any]:
        """生成健康建议"""
        # 这里应该集成AI模型或规则引擎
        # 目前作为框架占位符
        
        advice = {
            "query": query,
            "context": context,
            "timestamp": datetime.datetime.now().isoformat(),
            "advice": "基于您的健康档案和查询，建议您咨询专业医疗人员以获得准确的诊断和治疗建议。此建议仅供参考，不能替代专业医疗服务。",
            "confidence": "low",
            "sources": ["general_medical_guidelines"]
        }
        
        # 保存到历史记录
        try:
            with open(self.advice_history_path, 'r') as f:
                history = json.load(f)
            
            history.append(advice)
            
            with open(self.advice_history_path, 'w') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存建议历史失败: {e}")
        
        return advice
    
    def search_health_records(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """搜索健康记录"""
        records = self.get_health_records(limit=100)  # 获取所有记录
        matching_records = []
        
        for record in records:
            record_text = json.dumps(record).lower()
            if any(keyword.lower() in record_text for keyword in keywords):
                matching_records.append(record)
        
        return matching_records

# 工具函数
def format_health_advice(advice_dict: Dict[str, Any]) -> str:
    """格式化健康建议输出"""
    return f"""健康建议:

查询: {advice_dict.get('query', 'N/A')}
时间: {advice_dict.get('timestamp', 'N/A')}

建议内容:
{advice_dict.get('advice', '无建议内容')}

注意: 此建议仅供参考，不能替代专业医疗服务。
"""