"""
vault.py - Password Vault Storage Module
Manages encrypted password storage and retrieval
"""

import json
import secrets
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

from crypto import EncryptionManager, hash_password
from utils import ColorCodes


class PasswordVault:
    """Main password vault manager"""
    
    def __init__(self, vault_path: str = None):
        """
        Initialize the password vault
        
        Args:
            vault_path: Custom path for vault storage (optional)
        """
        if vault_path is None:
            home = Path.home()
            vault_path = home / '.securevault'
        
        self.vault_dir = Path(vault_path)
        self.vault_dir.mkdir(exist_ok=True)
        
        self.vault_file = self.vault_dir / 'vault.enc'
        self.salt_file = self.vault_dir / 'salt.key'
        self.hash_file = self.vault_dir / 'master.hash'
        
        self.encryption_manager = None
        self.passwords = {}
    
    def initialize_vault(self, master_password: str) -> bool:
        """
        Initialize a new vault with master password
        
        Args:
            master_password: Master password for vault encryption
            
        Returns:
            True if successful, False otherwise
        """
        if self.vault_file.exists():
            print(f"{ColorCodes.RED}✗ Vault already exists!{ColorCodes.END}")
            return False
        
        # Generate and save salt
        salt = secrets.token_bytes(32)
        with open(self.salt_file, 'wb') as f:
            f.write(salt)
        
        # Save master password hash
        password_hash = hash_password(master_password)
        with open(self.hash_file, 'w') as f:
            f.write(password_hash)
        
        # Initialize encryption
        self.encryption_manager = EncryptionManager(master_password, salt)
        
        # Create empty vault
        self.passwords = {}
        self._save_vault()
        
        print(f"{ColorCodes.GREEN}✓ Vault initialized successfully!{ColorCodes.END}")
        return True
    
    def unlock_vault(self, master_password: str) -> bool:
        """
        Unlock the vault with master password
        
        Args:
            master_password: Master password for vault decryption
            
        Returns:
            True if successful, False otherwise
        """
        if not self.vault_file.exists():
            print(f"{ColorCodes.RED}✗ No vault found! Please initialize first.{ColorCodes.END}")
            return False
        
        # Verify master password
        password_hash = hash_password(master_password)
        with open(self.hash_file, 'r') as f:
            stored_hash = f.read().strip()
        
        if password_hash != stored_hash:
            print(f"{ColorCodes.RED}✗ Incorrect master password!{ColorCodes.END}")
            return False
        
        # Load salt and initialize encryption
        with open(self.salt_file, 'rb') as f:
            salt = f.read()
        
        self.encryption_manager = EncryptionManager(master_password, salt)
        
        # Load vault
        self._load_vault()
        
        print(f"{ColorCodes.GREEN}✓ Vault unlocked successfully!{ColorCodes.END}")
        return True
    
    def _save_vault(self):
        """Save encrypted vault to disk"""
        vault_data = json.dumps(self.passwords, indent=2)
        encrypted_data = self.encryption_manager.encrypt(vault_data)
        
        with open(self.vault_file, 'w') as f:
            f.write(encrypted_data)
    
    def _load_vault(self):
        """Load and decrypt vault from disk"""
        try:
            with open(self.vault_file, 'r') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.encryption_manager.decrypt(encrypted_data)
            self.passwords = json.loads(decrypted_data)
        except Exception as e:
            print(f"{ColorCodes.RED}✗ Error loading vault: {e}{ColorCodes.END}")
            self.passwords = {}
    
    def add_password(self, service: str, username: str, password: str, notes: str = "") -> bool:
        """
        Add a new password entry
        
        Args:
            service: Service/website name
            username: Username or email
            password: Password to store
            notes: Optional notes
            
        Returns:
            True if successful, False otherwise
        """
        if service in self.passwords:
            print(f"{ColorCodes.YELLOW}⚠ Entry for '{service}' already exists. Use update to modify.{ColorCodes.END}")
            return False
        
        self.passwords[service] = {
            'username': username,
            'password': password,
            'notes': notes,
            'created': datetime.now().isoformat(),
            'modified': datetime.now().isoformat()
        }
        
        self._save_vault()
        print(f"{ColorCodes.GREEN}✓ Password added for '{service}'!{ColorCodes.END}")
        return True
    
    def get_password(self, service: str) -> Optional[Dict]:
        """
        Retrieve a password entry
        
        Args:
            service: Service/website name
            
        Returns:
            Dictionary containing password entry or None
        """
        return self.passwords.get(service)
    
    def update_password(self, service: str, username: str = None, 
                       password: str = None, notes: str = None) -> bool:
        """
        Update an existing password entry
        
        Args:
            service: Service/website name
            username: New username (optional)
            password: New password (optional)
            notes: New notes (optional)
            
        Returns:
            True if successful, False otherwise
        """
        if service not in self.passwords:
            print(f"{ColorCodes.RED}✗ No entry found for '{service}'!{ColorCodes.END}")
            return False
        
        entry = self.passwords[service]
        
        if username:
            entry['username'] = username
        if password:
            entry['password'] = password
        if notes is not None:
            entry['notes'] = notes
        
        entry['modified'] = datetime.now().isoformat()
        
        self._save_vault()
        print(f"{ColorCodes.GREEN}✓ Password updated for '{service}'!{ColorCodes.END}")
        return True
    
    def delete_password(self, service: str) -> bool:
        """
        Delete a password entry
        
        Args:
            service: Service/website name
            
        Returns:
            True if successful, False otherwise
        """
        if service not in self.passwords:
            print(f"{ColorCodes.RED}✗ No entry found for '{service}'!{ColorCodes.END}")
            return False
        
        del self.passwords[service]
        self._save_vault()
        print(f"{ColorCodes.GREEN}✓ Password deleted for '{service}'!{ColorCodes.END}")
        return True
    
    def list_services(self) -> List[str]:
        """
        List all stored services
        
        Returns:
            Sorted list of service names
        """
        return sorted(self.passwords.keys())
    
    def search_passwords(self, query: str) -> List[str]:
        """
        Search for services matching query
        
        Args:
            query: Search query string
            
        Returns:
            List of matching service names
        """
        query_lower = query.lower()
        return [s for s in self.passwords.keys() if query_lower in s.lower()]