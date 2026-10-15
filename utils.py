"""
utils.py - Utility Functions and Constants
Common utilities used across the application
"""


class ColorCodes:
    """ANSI color codes for beautiful terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_banner():
    """Print application banner"""
    banner = f"""
{ColorCodes.CYAN}{ColorCodes.BOLD}
╔═══════════════════════════════════════════════════════╗
║           SecureVault Password Manager                ║
║        Military-Grade Encryption • AES-128            ║
║         B.Tech 4th Year Capstone Project              ║
╚═══════════════════════════════════════════════════════╝
{ColorCodes.END}"""
    print(banner)


def print_menu():
    """Print main menu"""
    menu = f"""
{ColorCodes.BOLD}Main Menu:{ColorCodes.END}
{ColorCodes.CYAN}1.{ColorCodes.END} Add New Password
{ColorCodes.CYAN}2.{ColorCodes.END} Retrieve Password
{ColorCodes.CYAN}3.{ColorCodes.END} Update Password
{ColorCodes.CYAN}4.{ColorCodes.END} Delete Password
{ColorCodes.CYAN}5.{ColorCodes.END} List All Services
{ColorCodes.CYAN}6.{ColorCodes.END} Search Passwords
{ColorCodes.CYAN}7.{ColorCodes.END} Generate Secure Password
{ColorCodes.CYAN}8.{ColorCodes.END} Check Password Strength
{ColorCodes.CYAN}9.{ColorCodes.END} Lock Vault & Exit
"""
    print(menu)


def format_password_entry(service: str, entry: dict):
    """
    Format and display a password entry
    
    Args:
        service: Service/website name
        entry: Password entry dictionary
    """
    print(f"\n{ColorCodes.GREEN}{'='*50}{ColorCodes.END}")
    print(f"{ColorCodes.BOLD}Service:{ColorCodes.END} {service}")
    print(f"{ColorCodes.BOLD}Username:{ColorCodes.END} {entry['username']}")
    print(f"{ColorCodes.BOLD}Password:{ColorCodes.END} {entry['password']}")
    if entry['notes']:
        print(f"{ColorCodes.BOLD}Notes:{ColorCodes.END} {entry['notes']}")
    print(f"{ColorCodes.BOLD}Created:{ColorCodes.END} {entry['created'][:10]}")
    print(f"{ColorCodes.BOLD}Modified:{ColorCodes.END} {entry['modified'][:10]}")
    print(f"{ColorCodes.GREEN}{'='*50}{ColorCodes.END}")


def print_separator(char='=', length=50, color=ColorCodes.CYAN):
    """
    Print a separator line
    
    Args:
        char: Character to use for separator
        length: Length of separator
        color: ANSI color code
    """
    print(f"{color}{char*length}{ColorCodes.END}")