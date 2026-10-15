"""
cli.py - Command Line Interface Module
Handles all user interactions and menu operations
"""

import getpass
from typing import Optional

from vault import PasswordVault
from password_generator import SecurePasswordGenerator
from strength_checker import PasswordStrengthChecker
from utils import (
    ColorCodes, print_banner, print_menu, 
    format_password_entry, print_separator
)


class SecureVaultCLI:
    """Command-line interface for SecureVault"""
    
    def __init__(self):
        """Initialize the CLI"""
        self.vault = PasswordVault()
        self.unlocked = False
    
    def setup_vault(self) -> bool:
        """
        Setup or unlock vault
        
        Returns:
            True if successful, False otherwise
        """
        if self.vault.vault_file.exists():
            print(f"\n{ColorCodes.YELLOW}Existing vault found.{ColorCodes.END}")
            master_password = getpass.getpass("Enter master password: ")
            return self.vault.unlock_vault(master_password)
        else:
            print(f"\n{ColorCodes.YELLOW}No vault found. Let's create one!{ColorCodes.END}")
            print(f"{ColorCodes.BOLD}Master password requirements:{ColorCodes.END}")
            print("  • Minimum 8 characters")
            print("  • Mix of uppercase, lowercase, digits, and special characters")
            
            while True:
                master_password = getpass.getpass("\nCreate master password: ")
                confirm_password = getpass.getpass("Confirm master password: ")
                
                if master_password != confirm_password:
                    print(f"{ColorCodes.RED}✗ Passwords don't match!{ColorCodes.END}")
                    continue
                
                strength = PasswordStrengthChecker.check_strength(master_password)
                if strength['score'] < 60:
                    print(f"{ColorCodes.YELLOW}⚠ Password strength: {strength['strength']} ({strength['score']}/100){ColorCodes.END}")
                    print("Consider using a stronger password for better security.")
                    choice = input("Continue anyway? (y/n): ")
                    if choice.lower() != 'y':
                        continue
                
                return self.vault.initialize_vault(master_password)
    
    def add_password_interactive(self):
        """Interactive password addition"""
        print(f"\n{ColorCodes.BOLD}Add New Password{ColorCodes.END}")
        service = input("Service/Website name: ").strip()
        
        if not service:
            print(f"{ColorCodes.RED}✗ Service name cannot be empty!{ColorCodes.END}")
            return
        
        username = input("Username/Email: ").strip()
        
        print("\nPassword options:")
        print("1. Enter manually")
        print("2. Generate secure password")
        choice = input("Choose (1/2): ").strip()
        
        if choice == '2':
            length = input("Password length (default 16): ").strip()
            length = int(length) if length.isdigit() else 16
            password = SecurePasswordGenerator.generate(length)
            print(f"{ColorCodes.GREEN}Generated password: {ColorCodes.BOLD}{password}{ColorCodes.END}")
        else:
            password = getpass.getpass("Enter password: ")
            
            # Show strength
            strength = PasswordStrengthChecker.check_strength(password)
            print(f"\n{strength['color']}Password Strength: {strength['strength']} ({strength['score']}/100){ColorCodes.END}")
        
        notes = input("Notes (optional): ").strip()
        
        self.vault.add_password(service, username, password, notes)
    
    def retrieve_password_interactive(self):
        """Interactive password retrieval"""
        print(f"\n{ColorCodes.BOLD}Retrieve Password{ColorCodes.END}")
        service = input("Service/Website name: ").strip()
        
        entry = self.vault.get_password(service)
        
        if entry:
            format_password_entry(service, entry)
        else:
            print(f"{ColorCodes.RED}✗ No entry found for '{service}'!{ColorCodes.END}")
    
    def update_password_interactive(self):
        """Interactive password update"""
        print(f"\n{ColorCodes.BOLD}Update Password{ColorCodes.END}")
        service = input("Service/Website name: ").strip()
        
        entry = self.vault.get_password(service)
        if not entry:
            print(f"{ColorCodes.RED}✗ No entry found for '{service}'!{ColorCodes.END}")
            return
        
        print(f"\nCurrent username: {entry['username']}")
        username = input("New username (leave empty to keep current): ").strip()
        
        print("New password:")
        print("1. Enter manually")
        print("2. Generate secure password")
        print("3. Keep current")
        choice = input("Choose (1/2/3): ").strip()
        
        password = None
        if choice == '1':
            password = getpass.getpass("Enter new password: ")
        elif choice == '2':
            length = input("Password length (default 16): ").strip()
            length = int(length) if length.isdigit() else 16
            password = SecurePasswordGenerator.generate(length)
            print(f"{ColorCodes.GREEN}Generated password: {ColorCodes.BOLD}{password}{ColorCodes.END}")
        
        notes = input("New notes (leave empty to keep current): ").strip()
        
        self.vault.update_password(
            service,
            username if username else None,
            password,
            notes if notes else None
        )
    
    def delete_password_interactive(self):
        """Interactive password deletion"""
        print(f"\n{ColorCodes.BOLD}Delete Password{ColorCodes.END}")
        service = input("Service/Website name: ").strip()
        
        entry = self.vault.get_password(service)
        if not entry:
            print(f"{ColorCodes.RED}✗ No entry found for '{service}'!{ColorCodes.END}")
            return
        
        confirm = input(f"{ColorCodes.RED}Are you sure you want to delete '{service}'? (yes/no): {ColorCodes.END}").strip().lower()
        
        if confirm == 'yes':
            self.vault.delete_password(service)
        else:
            print(f"{ColorCodes.YELLOW}Deletion cancelled.{ColorCodes.END}")
    
    def list_services_interactive(self):
        """List all stored services"""
        services = self.vault.list_services()
        
        if not services:
            print(f"\n{ColorCodes.YELLOW}No passwords stored yet.{ColorCodes.END}")
            return
        
        print(f"\n{ColorCodes.BOLD}Stored Services ({len(services)}):{ColorCodes.END}")
        print_separator()
        for i, service in enumerate(services, 1):
            entry = self.vault.get_password(service)
            print(f"{i:2}. {ColorCodes.BOLD}{service}{ColorCodes.END} ({entry['username']})")
        print_separator()
    
    def search_passwords_interactive(self):
        """Interactive password search"""
        print(f"\n{ColorCodes.BOLD}Search Passwords{ColorCodes.END}")
        query = input("Search query: ").strip()
        
        results = self.vault.search_passwords(query)
        
        if not results:
            print(f"{ColorCodes.YELLOW}No results found for '{query}'.{ColorCodes.END}")
            return
        
        print(f"\n{ColorCodes.BOLD}Search Results ({len(results)}):{ColorCodes.END}")
        print_separator()
        for i, service in enumerate(results, 1):
            entry = self.vault.get_password(service)
            print(f"{i}. {ColorCodes.BOLD}{service}{ColorCodes.END} ({entry['username']})")
        print_separator()
    
    def generate_password_interactive(self):
        """Interactive password generation"""
        print(f"\n{ColorCodes.BOLD}Generate Secure Password{ColorCodes.END}")
        
        length = input("Password length (8-64, default 16): ").strip()
        length = int(length) if length.isdigit() and 8 <= int(length) <= 64 else 16
        
        use_special = input("Include special characters? (Y/n): ").strip().lower() != 'n'
        use_digits = input("Include digits? (Y/n): ").strip().lower() != 'n'
        use_upper = input("Include uppercase? (Y/n): ").strip().lower() != 'n'
        
        password = SecurePasswordGenerator.generate(length, use_special, use_digits, use_upper)
        
        print(f"\n{ColorCodes.GREEN}{ColorCodes.BOLD}Generated Password:{ColorCodes.END}")
        print_separator()
        print(f"{ColorCodes.BOLD}{password}{ColorCodes.END}")
        print_separator()
        
        # Show strength analysis
        strength = PasswordStrengthChecker.check_strength(password)
        print(f"\n{strength['color']}Strength: {strength['strength']} ({strength['score']}/100){ColorCodes.END}")
        print(f"Entropy: {strength['entropy']:.1f} bits")
    
    def check_strength_interactive(self):
        """Interactive password strength checker"""
        print(f"\n{ColorCodes.BOLD}Password Strength Checker{ColorCodes.END}")
        password = getpass.getpass("Enter password to analyze: ")
        
        strength = PasswordStrengthChecker.check_strength(password)
        
        print_separator()
        print(f"{strength['color']}{ColorCodes.BOLD}Strength: {strength['strength']} ({strength['score']}/100){ColorCodes.END}")
        print(f"{ColorCodes.BOLD}Entropy:{ColorCodes.END} {strength['entropy']:.1f} bits")
        print(f"\n{ColorCodes.BOLD}Analysis:{ColorCodes.END}")
        for item in strength['feedback']:
            print(f"  {item}")
        print_separator()
    
    def run(self):
        """Main application loop"""
        print_banner()
        
        if not self.setup_vault():
            print(f"\n{ColorCodes.RED}Failed to setup vault. Exiting...{ColorCodes.END}")
            return
        
        self.unlocked = True
        
        while self.unlocked:
            print_menu()
            choice = input(f"\n{ColorCodes.BOLD}Choose an option (1-9):{ColorCodes.END} ").strip()
            
            try:
                if choice == '1':
                    self.add_password_interactive()
                elif choice == '2':
                    self.retrieve_password_interactive()
                elif choice == '3':
                    self.update_password_interactive()
                elif choice == '4':
                    self.delete_password_interactive()
                elif choice == '5':
                    self.list_services_interactive()
                elif choice == '6':
                    self.search_passwords_interactive()
                elif choice == '7':
                    self.generate_password_interactive()
                elif choice == '8':
                    self.check_strength_interactive()
                elif choice == '9':
                    print(f"\n{ColorCodes.GREEN}✓ Vault locked. Goodbye!{ColorCodes.END}\n")
                    self.unlocked = False
                else:
                    print(f"{ColorCodes.YELLOW}Invalid option. Please choose 1-9.{ColorCodes.END}")
            except KeyboardInterrupt:
                print(f"\n\n{ColorCodes.YELLOW}Operation cancelled.{ColorCodes.END}")
            except Exception as e:
                print(f"\n{ColorCodes.RED}✗ Error: {e}{ColorCodes.END}")
            
            if self.unlocked:
                input(f"\n{ColorCodes.CYAN}Press Enter to continue...{ColorCodes.END}")
                print("\n" * 2)