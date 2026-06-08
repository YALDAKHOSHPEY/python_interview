import json
import math
from datetime import datetime

class ScoringSystem:
    """سیستم نمره‌دهی پیشرفته با ضریب سختی و سرعت"""
    
    def __init__(self):
        self.session_data = {
            "total_points": 0,
            "correct_answers": 0,
            "wrong_answers": 0,
            "skipped": 0,
            "time_bonus": 0,
            "streak_bonus": 0,
            "consecutive_correct": 0,
            "question_history": []
        }
        self._cached_stats = None
    
    def calculate_question_score(self, question_data, is_correct, time_taken=None):
        """محاسبه امتیاز بر اساس سختی، سرعت و streak"""
        base_points = question_data.get("points", 10)
        
        if not is_correct:
            self.session_data["consecutive_correct"] = 0
            return 0
        
        # امتیاز پایه
        score = base_points
        
        # ضریب سختی (1-5)
        difficulty = question_data.get("difficulty", 1)
        score *= (1 + (difficulty - 1) * 0.1)
        
        # پاداش سرعت (اگر تایمر وجود داشته باشد)
        if time_taken and question_data.get("time_limit"):
            time_limit = question_data["time_limit"]
            if time_taken < time_limit * 0.3:
                time_bonus = base_points * 0.3
                self.session_data["time_bonus"] += time_bonus
                score += time_bonus
            elif time_taken < time_limit * 0.6:
                time_bonus = base_points * 0.15
                self.session_data["time_bonus"] += time_bonus
                score += time_bonus
        
        # پاداش زنجیره پاسخ صحیح
        self.session_data["consecutive_correct"] += 1
        if self.session_data["consecutive_correct"] >= 3:
            streak_bonus = base_points * 0.2
            self.session_data["streak_bonus"] += streak_bonus
            score += streak_bonus
        
        return int(score)
    
    def add_result(self, question_id, is_correct, points_earned, time_taken=None):
        """ثبت نتیجه یک سوال"""
        self.session_data["question_history"].append({
            "question_id": question_id,
            "correct": is_correct,
            "points": points_earned,
            "time": time_taken,
            "timestamp": datetime.now().isoformat()
        })
        
        if is_correct:
            self.session_data["correct_answers"] += 1
            self.session_data["total_points"] += points_earned
        else:
            self.session_data["wrong_answers"] += 1
        
        # پاک کردن کش آمار
        self._cached_stats = None
    
    def get_final_stats(self):
        """دریافت آمار نهایی"""
        # استفاده از کش اگر وجود داشته باشد
        if self._cached_stats:
            return self._cached_stats
        
        total_attempted = self.session_data["correct_answers"] + self.session_data["wrong_answers"]
        
        # محاسبه دقت
        if total_attempted > 0:
            accuracy = (self.session_data["correct_answers"] / total_attempted * 100)
        else:
            accuracy = 0
        
        stats = {
            "total_points": self.session_data["total_points"],
            "accuracy": accuracy,
            "correct": self.session_data["correct_answers"],
            "wrong": self.session_data["wrong_answers"],
            "skipped": self.session_data["skipped"],
            "time_bonus": self.session_data["time_bonus"],
            "streak_bonus": self.session_data["streak_bonus"],
            "max_streak": self._calculate_max_streak(),
            "performance_grade": self._calculate_grade(accuracy)
        }
        
        self._cached_stats = stats
        return stats
    
    def _calculate_max_streak(self):
        """محاسبه بیشترین زنجیره پاسخ صحیح"""
        max_streak = 0
        current = 0
        for q in self.session_data["question_history"]:
            if q["correct"]:
                current += 1
                max_streak = max(max_streak, current)
            else:
                current = 0
        return max_streak
    
    def _calculate_grade(self, accuracy):
        """محاسبه نمره نهایی (A+ تا F) - بدون فراخوانی بازگشتی"""
        if accuracy >= 90:
            return "A+"
        elif accuracy >= 80:
            return "A"
        elif accuracy >= 70:
            return "B"
        elif accuracy >= 60:
            return "C"
        elif accuracy >= 50:
            return "D"
        else:
            return "F"
    
    def reset(self):
        """ریست کردن سیستم نمره‌دهی"""
        self.session_data = {
            "total_points": 0,
            "correct_answers": 0,
            "wrong_answers": 0,
            "skipped": 0,
            "time_bonus": 0,
            "streak_bonus": 0,
            "consecutive_correct": 0,
            "question_history": []
        }
        self._cached_stats = None