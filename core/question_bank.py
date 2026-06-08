import json
import random
from typing import List, Dict, Optional

class QuestionBank:
    """مدیریت پیشرفته بانک سوالات با فیلترهای مختلف"""
    
    def __init__(self, json_path="data/questions.json"):
        self.flattened_questions = []
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                self.raw_data = json.load(f)
            self.flattened_questions = self._flatten_questions()
            print(f"✅ Loaded {len(self.flattened_questions)} questions successfully!")
        except FileNotFoundError:
            print(f"⚠️ {json_path} not found! Creating default questions...")
            self._create_default_questions()
            self.flattened_questions = self._flatten_questions()
        except json.JSONDecodeError:
            print(f"❌ Error parsing {json_path}! Using default questions...")
            self._create_default_questions()
            self.flattened_questions = self._flatten_questions()
    
    def _create_default_questions(self):
        """ایجاد سوالات پیش‌فرض"""
        self.raw_data = {
            "python": {
                "beginner": [
                    {
                        "id": "py_001",
                        "question": "What is the output of: print(2**3**2)?",
                        "type": "mcq",
                        "options": ["64", "512", "81", "729"],
                        "correct_answer": "512",
                        "explanation": "Exponentiation is right-associative: 2**(3**2) = 2**9 = 512",
                        "difficulty": 1,
                        "points": 10,
                        "tags": ["operators"]
                    },
                    {
                        "id": "py_002",
                        "question": "What is the output of: print(type(10/3))?",
                        "type": "mcq",
                        "options": ["<class 'int'>", "<class 'float'>", "<class 'complex'>", "Error"],
                        "correct_answer": "<class 'float'>",
                        "explanation": "In Python 3, division always returns a float",
                        "difficulty": 1,
                        "points": 10,
                        "tags": ["types"]
                    },
                    {
                        "id": "py_003",
                        "question": "Which keyword is used to define a function?",
                        "type": "mcq",
                        "options": ["def", "func", "define", "function"],
                        "correct_answer": "def",
                        "explanation": "The 'def' keyword is used to define functions",
                        "difficulty": 1,
                        "points": 10,
                        "tags": ["functions"]
                    },
                    {
                        "id": "py_004",
                        "question": "What is the correct way to create a list?",
                        "type": "mcq",
                        "options": ["(1,2,3)", "[1,2,3]", "{1,2,3}", "<1,2,3>"],
                        "correct_answer": "[1,2,3]",
                        "explanation": "Square brackets are used for lists",
                        "difficulty": 1,
                        "points": 10,
                        "tags": ["lists"]
                    },
                    {
                        "id": "py_005",
                        "question": "What does the 'len()' function do?",
                        "type": "mcq",
                        "options": ["Returns the length of an object", "Returns the last element", "Returns the largest element", "Returns the memory size"],
                        "correct_answer": "Returns the length of an object",
                        "explanation": "len() returns the number of items in a container",
                        "difficulty": 1,
                        "points": 10,
                        "tags": ["builtins"]
                    }
                ],
                "intermediate": [
                    {
                        "id": "py_006",
                        "question": "What is list comprehension?",
                        "type": "descriptive",
                        "correct_answer": "List comprehension is a concise way to create lists using brackets containing an expression followed by a for clause",
                        "explanation": "Example: [x*2 for x in range(10)] creates a list of even numbers",
                        "difficulty": 2,
                        "points": 15,
                        "tags": ["comprehension"]
                    },
                    {
                        "id": "py_007",
                        "question": "Difference between 'is' and '=='?",
                        "type": "descriptive",
                        "correct_answer": "'==' checks if values are equal, 'is' checks if they refer to the same object in memory",
                        "explanation": "Use 'is' for None comparison, '==' for value equality",
                        "difficulty": 2,
                        "points": 15,
                        "tags": ["operators"]
                    }
                ]
            },
            "algorithms": {
                "beginner": [
                    {
                        "id": "alg_001",
                        "question": "What is the time complexity of binary search?",
                        "type": "mcq",
                        "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"],
                        "correct_answer": "O(log n)",
                        "explanation": "Binary search halves the search space each iteration",
                        "difficulty": 2,
                        "points": 15,
                        "tags": ["searching"]
                    },
                    {
                        "id": "alg_002",
                        "question": "Which data structure uses LIFO?",
                        "type": "mcq",
                        "options": ["Queue", "Stack", "Array", "Linked List"],
                        "correct_answer": "Stack",
                        "explanation": "Last In First Out - like a stack of plates",
                        "difficulty": 1,
                        "points": 10,
                        "tags": ["data structures"]
                    }
                ]
            },
            "databases": {
                "beginner": [
                    {
                        "id": "db_001",
                        "question": "What does SQL stand for?",
                        "type": "mcq",
                        "options": ["Structured Query Language", "Simple Query Language", "Standard Query Language", "System Query Language"],
                        "correct_answer": "Structured Query Language",
                        "explanation": "SQL is used to communicate with databases",
                        "difficulty": 1,
                        "points": 5,
                        "tags": ["basics"]
                    },
                    {
                        "id": "db_002",
                        "question": "What is a primary key?",
                        "type": "descriptive",
                        "correct_answer": "A primary key is a unique identifier for each record in a database table, cannot be NULL and must be unique",
                        "explanation": "Primary keys ensure row-level uniqueness",
                        "difficulty": 2,
                        "points": 10,
                        "tags": ["keys"]
                    }
                ]
            }
        }
    
    def _flatten_questions(self) -> List[Dict]:
        """تبدیل ساختار تو در تو به لیست تخت"""
        questions = []
        for category, levels in self.raw_data.items():
            for level, q_list in levels.items():
                for q in q_list:
                    # اطمینان از وجود فیلدهای مورد نیاز
                    if "difficulty" not in q:
                        q["difficulty"] = 2
                    if "points" not in q:
                        q["points"] = 10
                    if "tags" not in q:
                        q["tags"] = ["general"]
                    if "type" not in q:
                        q["type"] = "mcq"
                    
                    q["category"] = category
                    q["level"] = level
                    questions.append(q)
        return questions
    
    def get_all_questions(self) -> List[Dict]:
        return self.flattened_questions
    
    def filter_questions(self, 
                        categories: Optional[List[str]] = None,
                        levels: Optional[List[str]] = None,
                        types: Optional[List[str]] = None,
                        tags: Optional[List[str]] = None,
                        min_difficulty: int = 1,
                        max_difficulty: int = 5) -> List[Dict]:
        """فیلتر پیشرفته سوالات"""
        filtered = self.flattened_questions
        
        if categories:
            filtered = [q for q in filtered if q.get("category", "") in categories]
        
        if levels:
            filtered = [q for q in filtered if q.get("level", "") in levels]
        
        if types:
            filtered = [q for q in filtered if q.get("type", "") in types]
        
        if tags:
            filtered = [q for q in filtered if any(tag in q.get("tags", []) for tag in tags)]
        
        # فیلتر بر اساس سختی
        filtered = [q for q in filtered if min_difficulty <= q.get("difficulty", 2) <= max_difficulty]
        
        return filtered
    
    def get_random_questions(self, num_questions: int, **filters) -> List[Dict]:
        """دریافت سوالات تصادفی با فیلتر"""
        filtered = self.filter_questions(**filters)
        
        if not filtered:
            print(f"⚠️ No questions found with given filters! Using all questions.")
            filtered = self.flattened_questions
        
        if len(filtered) < num_questions:
            print(f"⚠️ Only {len(filtered)} questions available, using all of them.")
            num_questions = len(filtered)
        
        if num_questions == 0:
            return []
        
        return random.sample(filtered, num_questions)
    
    def get_questions_by_pattern(self, pattern: str) -> List[Dict]:
        """جستجوی سوالات با الگو"""
        pattern = pattern.lower()
        return [
            q for q in self.flattened_questions 
            if pattern in q.get("question", "").lower() or 
               pattern in " ".join(q.get("tags", [])).lower()
        ]
    
    def get_statistics(self) -> Dict:
        """آمار بانک سوالات"""
        if not self.flattened_questions:
            return {
                "total_questions": 0,
                "categories": {},
                "difficulty_distribution": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            }
        
        # محاسبه توزیع سختی
        diff_dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for q in self.flattened_questions:
            diff = q.get("difficulty", 2)
            if 1 <= diff <= 5:
                diff_dist[diff] += 1
        
        return {
            "total_questions": len(self.flattened_questions),
            "categories": {cat: len([q for q in self.flattened_questions if q.get("category") == cat]) 
                          for cat in set(q.get("category", "unknown") for q in self.flattened_questions)},
            "difficulty_distribution": diff_dist
        }