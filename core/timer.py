import time
import threading
from datetime import datetime

class QuizTimer:
    """پیشرفته‌ترین تایمر برای آزمون"""
    
    def __init__(self, duration_seconds=60):
        self.duration = duration_seconds
        self.remaining = duration_seconds
        self.is_running = False
        self.start_time = None
        self.thread = None
    
    def start(self):
        self.is_running = True
        self.start_time = datetime.now()
        return self
    
    def stop(self):
        self.is_running = False
        if self.start_time:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            self.remaining = max(0, self.duration - elapsed)
        return self.remaining
    
    def reset(self, new_duration=None):
        if new_duration:
            self.duration = new_duration
        self.remaining = self.duration
        self.is_running = False
        self.start_time = None
    
    def get_elapsed(self):
        if not self.start_time:
            return 0
        return min(self.duration, (datetime.now() - self.start_time).total_seconds())
    
    def get_remaining(self):
        if not self.is_running:
            return self.remaining
        return max(0, self.duration - self.get_elapsed())
    
    def is_expired(self):
        return self.get_remaining() <= 0
    
    def format_time(self, seconds=None):
        if seconds is None:
            seconds = int(self.get_remaining())
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"
    
    def run_with_warning(self, warning_callback=None, warning_times=[10, 30, 60]):
        """اجرا با هشدار در زمان‌های مشخص"""
        def _timer_thread():
            while self.is_running and not self.is_expired():
                remaining = self.get_remaining()
                
                if warning_callback and int(remaining) in warning_times:
                    warning_callback(int(remaining))
                
                time.sleep(0.5)
            
            if self.is_expired():
                self.is_running = False
        
        self.thread = threading.Thread(target=_timer_thread, daemon=True)
        self.thread.start()