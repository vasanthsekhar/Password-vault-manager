"""
strength_checker.py - Password Strength Analysis Module
Advanced password strength evaluation with entropy calculation
"""

import math
import string
from typing import Dict, List


class PasswordStrengthChecker:
    """Advanced password strength analysis engine"""
    
    @staticmethod
    def calculate_entropy(password: str) -> float:
        """
        Calculate password entropy in bits
        
        Entropy measures the randomness/unpredictability of a password.
        Higher entropy = more secure password
        
        Args:
            password: Password to analyze
            
        Returns:
            Entropy value in bits
        """
        charset_size = 0
        if any(c.islower() for c in password):
            charset_size += 26
        if any(c.isupper() for c in password):
            charset_size += 26
        if any(c.isdigit() for c in password):
            charset_size += 10
        if any(c in string.punctuation for c in password):
            charset_size += 32
        
        if charset_size == 0:
            return 0
        
        return len(password) * math.log2(charset_size)
    
    @staticmethod
    def check_strength(password: str) -> Dict:
        """
        Comprehensive password strength analysis
        
        Args:
            password: Password to analyze
            
        Returns:
            Dictionary containing:
                - score: Numerical score (0-100)
                - strength: Text rating (WEAK, MODERATE, GOOD, STRONG)
                - color: ANSI color code for display
                - feedback: List of feedback messages
                - entropy: Entropy value in bits
        """
        from utils import ColorCodes
        
        score = 0
        feedback = []
        
        # Length check
        length = len(password)
        if length >= 16:
            score += 30
            feedback.append("✓ Excellent length")
        elif length >= 12:
            score += 20
            feedback.append("✓ Good length")
        elif length >= 8:
            score += 10
            feedback.append("⚠ Minimum length met")
        else:
            feedback.append("✗ Too short (min 8 characters)")
        
        # Character diversity
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        
        diversity_score = sum([has_lower, has_upper, has_digit, has_special])
        score += diversity_score * 15
        
        if diversity_score == 4:
            feedback.append("✓ Excellent character diversity")
        elif diversity_score >= 3:
            feedback.append("✓ Good character mix")
        else:
            feedback.append("⚠ Add more character types")
        
        # Common patterns check
        common_patterns = ['123', 'abc', 'password', 'qwerty', '111']
        if any(pattern in password.lower() for pattern in common_patterns):
            score -= 20
            feedback.append("✗ Contains common patterns")
        
        # Entropy calculation
        entropy = PasswordStrengthChecker.calculate_entropy(password)
        if entropy >= 60:
            score += 25
            feedback.append(f"✓ High entropy ({entropy:.1f} bits)")
        elif entropy >= 40:
            feedback.append(f"⚠ Moderate entropy ({entropy:.1f} bits)")
        else:
            feedback.append(f"✗ Low entropy ({entropy:.1f} bits)")
        
        # Final score normalization
        score = max(0, min(100, score))
        
        if score >= 80:
            strength = "STRONG"
            color = ColorCodes.GREEN
        elif score >= 60:
            strength = "GOOD"
            color = ColorCodes.CYAN
        elif score >= 40:
            strength = "MODERATE"
            color = ColorCodes.YELLOW
        else:
            strength = "WEAK"
            color = ColorCodes.RED
        
        return {
            'score': score,
            'strength': strength,
            'color': color,
            'feedback': feedback,
            'entropy': entropy
        }