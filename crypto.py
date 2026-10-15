"""
crypto.py - Encryption and Security Module
Handles all cryptographic operations for SecureVault
"""

import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class EncryptionManager:
    """Military-grade encryption manager using Fernet (AES-128)"""
    
    def __init__(self, master_password: str, salt: bytes):
        """
        Initialize encryption with master password
        
        Args:
            master_password: The master password for key derivation
            salt: Cryptographic salt for PBKDF2
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        self.cipher = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """
        Encrypt data and return base64 encoded string
        
        Args:
            data: Plaintext string to encrypt
            
        Returns:
            Base64 encoded encrypted string
        """
        encrypted = self.cipher.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt base64 encoded encrypted data
        
        Args:
            encrypted_data: Base64 encoded encrypted string
            
        Returns:
            Decrypted plaintext string
        """
        decoded = base64.b64decode(encrypted_data.encode())
        decrypted = self.cipher.decrypt(decoded)
        return decrypted.decode()


def hash_password(password: str) -> str:
    """
    Create a SHA-256 hash of a password for verification
    
    Args:
        password: Password to hash
        
    Returns:
        Hexadecimal hash string
    """
    return hashlib.sha256(password.encode()).hexdigest()