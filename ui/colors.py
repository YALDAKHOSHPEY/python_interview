class Colors:
    """سیستم رنگی حرفه‌ای برای ترمینال"""
    
    # رنگ‌های پایه
    BLACK = '\033[0;30m'
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[0;37m'
    
    # رنگ‌های پررنگ (Bright)
    BRIGHT_BLACK = '\033[1;30m'
    BRIGHT_RED = '\033[1;31m'
    BRIGHT_GREEN = '\033[1;32m'
    BRIGHT_YELLOW = '\033[1;33m'
    BRIGHT_BLUE = '\033[1;34m'
    BRIGHT_PURPLE = '\033[1;35m'
    BRIGHT_CYAN = '\033[1;36m'
    BRIGHT_WHITE = '\033[1;37m'
    
    # سبک‌های متن
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    
    # پس‌زمینه
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_PURPLE = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    RESET = '\033[0m'
    
    @staticmethod
    def colorize(text, color, bold=False):
        """رنگ کردن متن"""
        style = Colors.BOLD if bold else ""
        return f"{style}{color}{text}{Colors.RESET}"
    
    @staticmethod
    def success(text):
        return f"{Colors.GREEN}✓ {text}{Colors.RESET}"
    
    @staticmethod
    def error(text):
        return f"{Colors.RED}✗ {text}{Colors.RESET}"
    
    @staticmethod
    def warning(text):
        return f"{Colors.YELLOW}⚠ {text}{Colors.RESET}"
    
    @staticmethod
    def info(text):
        return f"{Colors.CYAN}ℹ {text}{Colors.RESET}"
    
    @staticmethod
    def header(text):
        return f"\n{Colors.BRIGHT_CYAN}{Colors.BOLD}{'='*60}{Colors.RESET}\n{Colors.BRIGHT_YELLOW}{text.center(60)}{Colors.RESET}\n{Colors.BRIGHT_CYAN}{'='*60}{Colors.RESET}"