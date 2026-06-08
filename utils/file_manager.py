import json
import os
from datetime import datetime
from typing import Dict, List, Any

class FileManager:
    """مدیریت فایل‌ها و ذخیره‌سازی پیشرفت کاربر"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.reports_dir = "reports"
        self._ensure_directories()
    
    def _ensure_directories(self):
        """ایجاد دایرکتوری‌های لازم"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def save_user_progress(self, user_data: Dict, filename="user_progress.json"):
        """ذخیره پیشرفت کاربر"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=2, ensure_ascii=False)
    
    def load_user_progress(self, filename="user_progress.json") -> Dict:
        """بارگذاری پیشرفت کاربر"""
        filepath = os.path.join(self.data_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_report(self, report_data: Dict, filename=None):
        """ذخیره گزارش عملکرد"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.json"
        
        filepath = os.path.join(self.reports_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        return filepath
    
    def load_questions(self, filename="questions.json") -> Dict:
        """بارگذاری سوالات"""
        filepath = os.path.join(self.data_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}