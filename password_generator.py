"""
password_generator.py - Secure Password Generation Module
Cryptographically secure random password generation
"""

import secrets
import string


class SecurePasswordGenerator:
    """Cryptographically secure password generator"""
    
    @staticmethod
    def generate(length: int = 16, use_special: bool = True, 
                 use_digits: bool = True, use_upper: bool = True) -> str:
        """
        Generate a cryptographically secure random password
        
        Args:
            length: Length of the password (8-64)
            use_special: Include special characters
            use_digits: Include digits
            use_upper: Include uppercase letters
            
        Returns:
            Randomly generated secure password
        """
        charset = string.ascii_lowercase
        
        if use_upper:
            charset += string.ascii_uppercase
        if use_digits:
            charset += string.digits
        if use_special:
            charset += string.punctuation
        
        # Ensure at least one character from each selected category
        password = []
        if use_upper:
            password.append(secrets.choice(string.ascii_uppercase))
        if use_digits:
            password.append(secrets.choice(string.digits))
        if use_special:
            password.append(secrets.choice(string.punctuation))
        password.append(secrets.choice(string.ascii_lowercase))
        
        # Fill the rest randomly
        password.extend(secrets.choice(charset) for _ in range(length - len(password)))
        
        # Shuffle to avoid predictable patterns
        password_list = list(password)
        for i in range(len(password_list) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            password_list[i], password_list[j] = password_list[j], password_list[i]
        
        return ''.join(password_list)