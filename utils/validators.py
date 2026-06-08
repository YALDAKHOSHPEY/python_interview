import re
from typing import Tuple, Optional

class Validators:
    """کلاس اعتبارسنجی ورودی‌ها"""
    
    @staticmethod
    def validate_number_input(user_input: str, min_val: int = 1, max_val: int = 100) -> Tuple[bool, Optional[int]]:
        """اعتبارسنجی ورودی عددی"""
        try:
            num = int(user_input)
            if min_val <= num <= max_val:
                return True, num
            return False, None
        except ValueError:
            return False, None
    
    @staticmethod
    def validate_choice_input(user_input: str, num_options: int) -> Tuple[bool, Optional[int]]:
        """اعتبارسنجی انتخاب گزینه"""
        if user_input.lower() in ['s', 'skip', '']:
            return True, -1  # -1 means skip
        
        try:
            choice = int(user_input)
            if 1 <= choice <= num_options:
                return True, choice - 1
            return False, None
        except ValueError:
            return False, None
    
    @staticmethod
    def validate_answer_text(answer: str, min_length: int = 1) -> bool:
        """اعتبارسنجی پاسخ متنی"""
        if not answer or len(answer.strip()) < min_length:
            return False
        return True
    
    @staticmethod
    def sanitize_input(user_input: str) -> str:
        """پاکسازی ورودی کاربر"""
        # حذف فضاهای اضافی
        cleaned = user_input.strip()
        # حذف کاراکترهای خطرناک (برای امنیت)
        cleaned = re.sub(r'[<>{}]', '', cleaned)
        return cleaned