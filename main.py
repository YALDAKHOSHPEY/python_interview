#!/usr/bin/env python3
"""
Professional Interview Preparation System
Author: Advanced Python Developer
Version: 2.0.0
"""

import sys
import os
from datetime import datetime
from typing import List, Dict

# اضافه کردن مسیرها
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.question_bank import QuestionBank
from core.scoring import ScoringSystem
from core.timer import QuizTimer
from ui.colors import Colors
import time

class ProfessionalInterviewSystem:
    """سیستم حرفه‌ای آمادگی مصاحبه"""
    
    def __init__(self):
        self.question_bank = QuestionBank()
        self.scoring = ScoringSystem()
        self.current_session = {
            "start_time": None,
            "mode": None,
            "questions": [],
            "current_index": 0
        }
    
    def safe_int_input(self, prompt, default=None):
        """دریافت ورودی عددی با مدیریت خطا"""
        while True:
            user_input = input(prompt).strip()
            if not user_input and default is not None:
                return default
            try:
                return int(user_input)
            except ValueError:
                print(Colors.error(f"Invalid input! Please enter a number (or press Enter for default)."))
    
    def display_welcome(self):
        """نمایش صفحه خوش‌آمدگویی حرفه‌ای"""
        print(Colors.header("🚀 PROFESSIONAL INTERVIEW PREPARATION SYSTEM"))
        print(f"\n{Colors.BRIGHT_WHITE}Welcome to the most advanced interview prep tool!{Colors.RESET}")
        print(f"{Colors.DIM}Master Python, Algorithms, System Design & More{Colors.RESET}\n")
        
        stats = self.question_bank.get_statistics()
        print(f"{Colors.BRIGHT_CYAN}📚 Question Bank Statistics:{Colors.RESET}")
        print(f"   Total Questions: {Colors.BRIGHT_YELLOW}{stats['total_questions']}{Colors.RESET}")
        print(f"   Categories: {', '.join(stats['categories'].keys())}")
        
        # نمایش توزیع سختی موجود
        available_diffs = [d for d, count in stats['difficulty_distribution'].items() if count > 0]
        if available_diffs:
            print(f"   Available Difficulties: {available_diffs}")
        print(f"   Difficulty Levels: 1 (Easy) → 5 (Expert)\n")
    
    def show_main_menu(self):
        """نمایش منوی اصلی با گزینه‌های حرفه‌ای"""
        while True:
            print(Colors.header("MAIN MENU"))
            print(f"{Colors.BRIGHT_GREEN}1.{Colors.RESET} 🎯 Start Quiz")
            print(f"{Colors.BRIGHT_GREEN}2.{Colors.RESET} 🎓 Mock Interview (Timed)")
            print(f"{Colors.BRIGHT_GREEN}3.{Colors.RESET} 🏆 Challenge Mode (Hard Questions)")
            print(f"{Colors.BRIGHT_GREEN}4.{Colors.RESET} 🔍 Practice Specific Topic")
            print(f"{Colors.BRIGHT_GREEN}5.{Colors.RESET} 📊 View Statistics")
            print(f"{Colors.BRIGHT_GREEN}6.{Colors.RESET} 🎲 Random Question")
            print(f"{Colors.BRIGHT_GREEN}7.{Colors.RESET} 📈 Performance Report")
            print(f"{Colors.BRIGHT_GREEN}8.{Colors.RESET} 🚪 Exit")
            
            choice = input(f"\n{Colors.BRIGHT_CYAN}Select option (1-8): {Colors.RESET}").strip()
            
            if choice == '1':
                self.start_quiz_mode()
            elif choice == '2':
                self.start_mock_interview()
            elif choice == '3':
                self.start_challenge_mode()
            elif choice == '4':
                self.practice_topic()
            elif choice == '5':
                self.show_statistics()
            elif choice == '6':
                self.random_question()
            elif choice == '7':
                self.generate_report()
            elif choice == '8':
                print(Colors.success("Thanks for practicing! Good luck with your interviews! 🎉"))
                sys.exit(0)
            else:
                print(Colors.error("Invalid option! Please try again."))
    
    def start_quiz_mode(self):
        """حالت عادی آزمون"""
        print(Colors.header("QUIZ MODE"))
        
        num_questions = self.safe_int_input(
            f"{Colors.BRIGHT_YELLOW}Number of questions (default 5): {Colors.RESET}", 
            default=5
        )
        
        # نمایش توزیع سختی موجود
        stats = self.question_bank.get_statistics()
        available_difficulties = [d for d, count in stats['difficulty_distribution'].items() if count > 0]
        
        print(f"\n{Colors.BRIGHT_CYAN}Available difficulty levels: {available_difficulties}{Colors.RESET}")
        difficulty_input = input(f"{Colors.BRIGHT_YELLOW}Difficulty (1-5, or press Enter for all): {Colors.RESET}").strip()
        
        # دریافت سوالات بدون فیلتر سختی اگر کاربر Enter زد
        if not difficulty_input:
            questions = self.question_bank.get_random_questions(num_questions=num_questions)
        else:
            try:
                difficulty = int(difficulty_input)
                questions = self.question_bank.get_random_questions(
                    num_questions=num_questions,
                    min_difficulty=difficulty,
                    max_difficulty=difficulty
                )
            except ValueError:
                print(Colors.error("Invalid difficulty! Using all difficulties."))
                questions = self.question_bank.get_random_questions(num_questions=num_questions)
        
        if not questions:
            print(Colors.error(f"No questions found with difficulty {difficulty_input}!"))
            print(Colors.info(f"Available difficulties: {available_difficulties}"))
            print(Colors.info("Showing all questions instead..."))
            questions = self.question_bank.get_random_questions(
                num_questions=min(num_questions, self.question_bank.get_statistics()['total_questions'])
            )
        
        if questions:
            self.run_quiz_session(questions, timed=False)
        else:
            print(Colors.error("No questions available in the database!"))
    
    def start_mock_interview(self):
        """شبیه‌سازی مصاحبه واقعی با تایمر"""
        print(Colors.header("🎤 MOCK INTERVIEW MODE"))
        print(f"{Colors.BRIGHT_RED}⚠ This simulates a real interview with time limits!{Colors.RESET}\n")
        
        time_per_question = self.safe_int_input(
            f"{Colors.BRIGHT_YELLOW}Seconds per question (default 60): {Colors.RESET}",
            default=60
        )
        
        num_questions = self.safe_int_input(
            f"{Colors.BRIGHT_YELLOW}Number of questions (default 5): {Colors.RESET}",
            default=5
        )
        
        # در مصاحبه از سوالات با سختی متوسط به بالا استفاده کن
        questions = self.question_bank.get_random_questions(
            num_questions=num_questions,
            min_difficulty=2
        )
        
        if not questions:
            print(Colors.warning("Not enough medium/hard questions! Using all available questions."))
            questions = self.question_bank.get_random_questions(num_questions=num_questions)
        
        if not questions:
            print(Colors.error("No questions available!"))
            return
        
        # اضافه کردن محدودیت زمانی به سوالات
        for q in questions:
            q['time_limit'] = time_per_question
        
        self.run_quiz_session(questions, timed=True, time_per_question=time_per_question)
    
    def start_challenge_mode(self):
        """حالت چالش - سوالات سخت فقط"""
        print(Colors.header("🏆 CHALLENGE MODE - EXPERT LEVEL"))
        print(f"{Colors.BRIGHT_RED}Only difficult questions (Level 3-5)!{Colors.RESET}\n")
        
        num_questions = self.safe_int_input(
            f"{Colors.BRIGHT_YELLOW}Number of challenge questions (default 5): {Colors.RESET}",
            default=5
        )
        
        questions = self.question_bank.get_random_questions(
            num_questions=num_questions,
            min_difficulty=3,
            max_difficulty=5
        )
        
        if not questions:
            print(Colors.warning("Not enough hard questions! Showing all available questions."))
            questions = self.question_bank.get_random_questions(num_questions=num_questions)
        
        if not questions:
            print(Colors.error("No questions available!"))
            return
        
        self.run_quiz_session(questions, timed=False, challenge_mode=True)
    
    def practice_topic(self):
        """تمرکز روی یک موضوع خاص"""
        print(Colors.header("TOPIC PRACTICE"))
        
        # نمایش موضوعات موجود
        stats = self.question_bank.get_statistics()
        categories = list(stats['categories'].keys())
        
        if not categories:
            print(Colors.error("No categories available!"))
            return
        
        print(f"\n{Colors.BRIGHT_CYAN}Available topics:{Colors.RESET}")
        for i, cat in enumerate(categories, 1):
            count = stats['categories'][cat]
            print(f"  {i}. {cat.title()} ({count} questions)")
        
        choice = self.safe_int_input(
            f"\n{Colors.BRIGHT_YELLOW}Select topic number: {Colors.RESET}",
            default=1
        )
        
        if choice < 1 or choice > len(categories):
            print(Colors.error("Invalid choice!"))
            return
        
        selected_category = categories[choice - 1]
        
        questions = self.question_bank.filter_questions(categories=[selected_category])
        
        if not questions:
            print(Colors.error(f"No questions found for {selected_category}"))
            return
        
        print(f"\n{Colors.success(f'Found {len(questions)} questions on {selected_category}')}")
        num_questions = min(
            self.safe_int_input(f"Number of questions to practice: {Colors.RESET}", default=5),
            len(questions)
        )
        
        import random
        selected_questions = random.sample(questions, num_questions)
        self.run_quiz_session(selected_questions, timed=False)
    
    def run_quiz_session(self, questions: List[Dict], timed: bool = False, time_per_question: int = 60, challenge_mode: bool = False):
        """اجرای جلسه آزمون اصلی"""
        if not questions:
            print(Colors.error("No questions found!"))
            return
        
        self.scoring = ScoringSystem()  # Reset scoring
        self.current_session['questions'] = questions
        self.current_session['start_time'] = datetime.now()
        
        print(Colors.header("QUIZ STARTED"))
        print(f"Total Questions: {len(questions)}")
        if timed:
            print(f"Time per question: {time_per_question} seconds")
        if challenge_mode:
            print(f"{Colors.BRIGHT_RED}Challenge Mode Active! Good luck!{Colors.RESET}")
        
        input(f"\n{Colors.BRIGHT_GREEN}Press Enter to begin...{Colors.RESET}")
        
        for idx, question in enumerate(questions, 1):
            print(f"\n{Colors.BRIGHT_CYAN}{'='*60}{Colors.RESET}")
            print(f"{Colors.BOLD}Question {idx}/{len(questions)} | Category: {question.get('category', 'Unknown').upper()} | Difficulty: {question.get('difficulty', 1)}/5{Colors.RESET}")
            print(f"{Colors.BRIGHT_YELLOW}Points: {question.get('points', 10)} | Tags: {', '.join(question.get('tags', ['general']))}{Colors.RESET}")
            print(f"{Colors.BRIGHT_CYAN}{'='*60}{Colors.RESET}\n")
            
            print(f"{Colors.BRIGHT_WHITE}{question['question']}{Colors.RESET}\n")
            
            # تایمر برای سوالات زمان‌دار
            timer = None
            if timed and question.get('time_limit'):
                timer = QuizTimer(question['time_limit']).start()
                timer.run_with_warning(
                    lambda t: print(Colors.warning(f"⚠ {t} seconds remaining!"))
                )
            
            start_time = time.time()
            
            if question.get('type') == 'mcq':
                for opt_idx, option in enumerate(question.get('options', []), 1):
                    print(f"  {opt_idx}. {option}")
                
                user_input = input(f"\n{Colors.BRIGHT_GREEN}Your answer (number) or 's' to skip: {Colors.RESET}").strip()
                
                if timer and timer.is_expired():
                    print(Colors.error("Time's up!"))
                    is_correct = False
                elif user_input.lower() in ['s', 'skip']:
                    self.scoring.session_data['skipped'] += 1
                    print(Colors.warning("Question skipped"))
                    is_correct = False
                else:
                    try:
                        choice_idx = int(user_input) - 1
                        if 0 <= choice_idx < len(question.get('options', [])):
                            user_answer = question['options'][choice_idx]
                            is_correct = (user_answer == question.get('correct_answer', ''))
                            
                            if is_correct:
                                print(Colors.success("✓ CORRECT!"))
                            else:
                                print(Colors.error(f"✗ WRONG! Correct answer: {question.get('correct_answer', 'N/A')}"))
                            
                            print(f"{Colors.DIM}💡 Explanation: {question.get('explanation', 'No explanation available')}{Colors.RESET}")
                        else:
                            print(Colors.error("Invalid option number!"))
                            is_correct = False
                    except (ValueError, IndexError):
                        print(Colors.error("Invalid input! Marked as wrong."))
                        is_correct = False
            
            else:  # descriptive
                print(f"{Colors.DIM}(Write your answer. Be thorough and professional.){Colors.RESET}")
                user_answer = input(f"\n{Colors.BRIGHT_GREEN}Your answer: {Colors.RESET}").strip()
                
                if timer and timer.is_expired():
                    print(Colors.error("Time's up!"))
                    is_correct = False
                elif user_answer.lower() in ['s', 'skip']:
                    self.scoring.session_data['skipped'] += 1
                    print(Colors.warning("Question skipped"))
                    is_correct = False
                else:
                    print(f"\n{Colors.BRIGHT_CYAN}Sample answer:{Colors.RESET}")
                    print(f"{Colors.DIM}{question.get('correct_answer', 'N/A')}{Colors.RESET}")
                    print(f"\n{Colors.DIM}💡 {question.get('explanation', 'No explanation available')}{Colors.RESET}")
                    
                    correct_input = input(f"\n{Colors.BRIGHT_YELLOW}Was your answer correct? (y/n): {Colors.RESET}").lower()
                    is_correct = (correct_input == 'y')
            
            time_taken = time.time() - start_time
            if timer:
                timer.stop()
            
            # محاسبه امتیاز
            points_earned = self.scoring.calculate_question_score(question, is_correct, time_taken)
            self.scoring.add_result(question.get('id', f'q_{idx}'), is_correct, points_earned, time_taken)
            
            print(f"\n{Colors.BRIGHT_PURPLE}Points earned: {points_earned}{Colors.RESET}")
            
            if idx < len(questions):
                input(f"\n{Colors.DIM}Press Enter for next question...{Colors.RESET}")
        
        # نمایش نتیجه نهایی
        self.show_final_results(challenge_mode)
    
    def show_final_results(self, challenge_mode=False):
        """نمایش نتایج نهایی پیشرفته"""
        stats = self.scoring.get_final_stats()
        session_duration = (datetime.now() - self.current_session['start_time']).total_seconds()
        
        print(Colors.header("📊 FINAL RESULTS"))
        
        # نمایش نمره با گرید رنگی
        grade_colors = {
            'A+': Colors.BRIGHT_GREEN, 'A': Colors.GREEN,
            'B': Colors.BRIGHT_CYAN, 'C': Colors.YELLOW,
            'D': Colors.BRIGHT_YELLOW, 'F': Colors.RED
        }
        grade_color = grade_colors.get(stats['performance_grade'], Colors.WHITE)
        
        print(f"\n{Colors.BOLD}Performance Grade: {grade_color}{stats['performance_grade']}{Colors.RESET}")
        print(f"{Colors.BOLD}Total Score: {Colors.BRIGHT_YELLOW}{stats['total_points']}{Colors.RESET}")
        print(f"Accuracy: {stats['accuracy']:.1f}%")
        print(f"Correct: {stats['correct']} | Wrong: {stats['wrong']} | Skipped: {stats['skipped']}")
        print(f"Max Streak: {stats['max_streak']}")
        print(f"Time Bonus: +{stats['time_bonus']:.0f} | Streak Bonus: +{stats['streak_bonus']:.0f}")
        print(f"Total Time: {int(session_duration // 60)}m {int(session_duration % 60)}s")
        
        # پیام تشویقی بر اساس عملکرد
        if stats['accuracy'] >= 90:
            print(f"\n{Colors.BRIGHT_GREEN}🏆 EXCELLENT! You're interview-ready! 🏆{Colors.RESET}")
        elif stats['accuracy'] >= 70:
            print(f"\n{Colors.BRIGHT_CYAN}👍 GOOD JOB! A bit more practice and you'll be perfect!{Colors.RESET}")
        elif stats['accuracy'] >= 50:
            print(f"\n{Colors.YELLOW}📚 KEEP GOING! Review the topics you missed.{Colors.RESET}")
        else:
            print(f"\n{Colors.BRIGHT_RED}💪 DON'T GIVE UP! Every mistake is a learning opportunity.{Colors.RESET}")
        
        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
    
    def show_statistics(self):
        """نمایش آمار کلی"""
        stats = self.question_bank.get_statistics()
        print(Colors.header("📈 SYSTEM STATISTICS"))
        print(f"\n{Colors.BRIGHT_CYAN}Total Questions: {Colors.BRIGHT_YELLOW}{stats['total_questions']}{Colors.RESET}")
        
        if stats['total_questions'] > 0:
            print(f"\n{Colors.BOLD}Categories Breakdown:{Colors.RESET}")
            for cat, count in stats['categories'].items():
                bar_length = int(count / stats['total_questions'] * 40)
                bar = "█" * bar_length
                print(f"  {cat.title():15} : {bar} {count}")
            
            print(f"\n{Colors.BOLD}Difficulty Distribution:{Colors.RESET}")
            for diff in range(1, 6):
                count = stats['difficulty_distribution'].get(diff, 0)
                if count > 0:
                    bar_length = int(count / stats['total_questions'] * 40)
                    bar = "█" * bar_length
                    stars = "★" * diff
                    print(f"  Level {diff} {stars:5} : {bar} {count}")
        else:
            print(Colors.warning("No questions found in database!"))
    
    def random_question(self):
        """نمایش یک سوال تصادفی"""
        all_q = self.question_bank.get_all_questions()
        if not all_q:
            print(Colors.error("No questions available!"))
            return
        
        import random
        question = random.choice(all_q)
        
        print(Colors.header("🎲 RANDOM QUESTION"))
        print(f"\n{Colors.BRIGHT_WHITE}{question.get('question', 'No question text')}{Colors.RESET}")
        print(f"\nCategory: {question.get('category', 'Unknown')} | Difficulty: {question.get('difficulty', 1)}/5")
        
        if question.get('type') == 'mcq':
            for opt in question.get('options', []):
                print(f"  • {opt}")
            
            input(f"\n{Colors.DIM}Think about it... Press Enter to see answer{Colors.RESET}")
            print(f"\n{Colors.BRIGHT_GREEN}Answer: {question.get('correct_answer', 'N/A')}{Colors.RESET}")
        
        print(f"\n{Colors.DIM}💡 {question.get('explanation', 'No explanation available')}{Colors.RESET}")
        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
    
    def generate_report(self):
        """تولید گزارش عملکرد"""
        print(Colors.header("📄 PERFORMANCE REPORT"))
        print(f"{Colors.warning('This feature requires saving session history.')}")
        print(f"{Colors.info('Coming soon: Detailed analytics and progress tracking!')}")
        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
    
    def run(self):
        """اجرای اصلی سیستم"""
        self.display_welcome()
        self.show_main_menu()

if __name__ == "__main__":
    system = ProfessionalInterviewSystem()
    try:
        system.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.warning('Session interrupted. Goodbye!')}")
        sys.exit(0)