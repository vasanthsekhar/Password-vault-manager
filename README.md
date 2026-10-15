SecureVault - Advanced Password Manager CLI
Show Image
Show Image
Show Image
A sophisticated command-line password manager with military-grade encryption built for B.Tech 4th Year Capstone Project.
📁 Project Structure
SecureVault/
├── main.py                    # Application entry point
├── cli.py                     # Command-line interface
├── vault.py                   # Password vault storage
├── crypto.py                  # Encryption module
├── password_generator.py      # Secure password generator
├── strength_checker.py        # Password strength analyzer
├── utils.py                   # Utility functions and constants
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── .securevault/             # Auto-created vault storage (hidden)
    ├── vault.enc             # Encrypted password database
    ├── salt.key              # Encryption salt
    └── master.hash           # Master password hash
🚀 Features
Core Functionality

🔐 Military-Grade Encryption: AES-128 encryption via Fernet (cryptography library)
🔑 Master Password Protection: PBKDF2 key derivation with 100,000 iterations
📝 Password Management: Add, retrieve, update, and delete password entries
🔍 Smart Search: Fast search functionality across all stored services
📊 Password Strength Analyzer: Real-time entropy calculation and strength assessment
🎲 Secure Password Generator: Cryptographically secure random password generation
💾 Local Storage: All data stored locally with zero cloud dependency

Security Features

Salt-based encryption for enhanced security
Master password hashing (SHA-256)
No plaintext storage - all passwords encrypted at rest
Secure password input (hidden input using getpass)
Strong password enforcement with real-time feedback

Technical Highlights

Modular Architecture: Clean separation of concerns across 7 modules
Object-Oriented Design: Professional OOP patterns
Type Hints: Full type annotation for better code quality
Error Handling: Comprehensive exception handling
Beautiful CLI: ANSI color-coded output for enhanced UX
Cross-Platform: Works on Windows, macOS, and Linux

📦 Installation
Prerequisites

Python 3.8 or higher
pip package manager

Setup

Download/Clone the project

bash# Create project directory
mkdir SecureVault
cd SecureVault

# Copy all project files here:
# main.py, cli.py, vault.py, crypto.py, 
# password_generator.py, strength_checker.py, utils.py

Install dependencies

bashpip install -r requirements.txt
# or
pip install cryptography

Run the application

bashpython main.py
🎯 Usage Guide
First Time Setup
When you run the application for the first time:
bashpython main.py
You'll be prompted to create a master password:
No vault found. Let's create one!
Master password requirements:
  • Minimum 8 characters
  • Mix of uppercase, lowercase, digits, and special characters

Create master password: ********
Confirm master password: ********
✓ Vault initialized successfully!
Main Menu Options
Main Menu:
1. Add New Password
2. Retrieve Password
3. Update Password
4. Delete Password
5. List All Services
6. Search Passwords
7. Generate Secure Password
8. Check Password Strength
9. Lock Vault & Exit
Example Workflows
Adding a New Password
Choose an option (1-9): 1

Add New Password
Service/Website name: github.com
Username/Email: user@example.com

Password options:
1. Enter manually
2. Generate secure password
Choose (1/2): 2
Password length (default 16): 20
Generated password: Kj9#mP2$xL4@nQ8&wR5!

Notes (optional): Personal GitHub account
✓ Password added for 'github.com'!
Retrieving a Password
Choose an option (1-9): 2

Retrieve Password
Service/Website name: github.com

==================================================
Service: github.com
Username: user@example.com
Password: Kj9#mP2$xL4@nQ8&wR5!
Notes: Personal GitHub account
Created: 2025-11-06
Modified: 2025-11-06
==================================================
Generating Secure Password
Choose an option (1-9): 7

Generate Secure Password
Password length (8-64, default 16): 24
Include special characters? (Y/n): Y
Include digits? (Y/n): Y
Include uppercase? (Y/n): Y

Generated Password:
==================================================
Kj9#mP2$xL4@nQ8&wR5!tY6^
==================================================

Strength: STRONG (95/100)
Entropy: 158.4 bits
🏗️ Module Documentation
1. main.py - Application Entry Point

Initializes the CLI application
Handles global exceptions
Entry point for execution

2. cli.py - Command Line Interface

SecureVaultCLI class: Main interface controller
Menu system and user interactions
Input validation and error handling
All interactive workflows

3. vault.py - Password Vault Storage

PasswordVault class: Core password management
CRUD operations (Create, Read, Update, Delete)
Search functionality
Encrypted file I/O operations
Master password verification

4. crypto.py - Encryption Module

EncryptionManager class: Fernet encryption wrapper
PBKDF2 key derivation
Encrypt/decrypt operations
Password hashing functions

5. password_generator.py - Password Generator

SecurePasswordGenerator class: Cryptographic password generation
Customizable character sets
Ensures character diversity
Uses secrets module for cryptographic randomness

6. strength_checker.py - Strength Analyzer

PasswordStrengthChecker class: Password analysis engine
Entropy calculation (information theory)
Character diversity checking
Pattern detection
Comprehensive feedback generation

7. utils.py - Utilities

ColorCodes class: ANSI color constants
Banner and menu printing functions
Password entry formatting
Common utility functions

🔒 Security Implementation
Encryption Specifications
pythonAlgorithm: AES-128 (via Fernet)
Key Derivation: PBKDF2-HMAC-SHA256
Iterations: 100,000
Salt Length: 256 bits (32 bytes)
Random Generation: secrets module (CSPRNG)
Data Flow

Initialization

Generate random salt (32 bytes)
Derive encryption key using PBKDF2
Hash master password (SHA-256)


Encryption

Convert password data to JSON
Encrypt JSON using Fernet (AES-128)
Encode to Base64
Write to file


Decryption

Read encrypted file
Decode Base64
Decrypt using Fernet
Parse JSON



Security Best Practices
✅ No hardcoded credentials
✅ Cryptographically secure random generation
✅ Salt-based encryption (prevents rainbow tables)
✅ High iteration count (100,000 for PBKDF2)
✅ No plaintext storage
✅ Secure password input (getpass)
✅ Master password hashing
✅ Comprehensive error handling
📊 Technical Specifications
Performance

Encryption/Decryption: < 10ms for typical vault sizes
Password Generation: < 1ms
Search: O(n) linear search
Storage Format: JSON (human-readable when decrypted)

Dependencies

cryptography (41.0.0+): Industrial-strength encryption
Python Standard Library: pathlib, json, secrets, hashlib, getpass

Compatibility

Python: 3.8, 3.9, 3.10, 3.11, 3.12+
OS: Windows, macOS, Linux
Terminal: Any ANSI-compatible terminal

🎓 B.Tech Project Highlights
This project demonstrates:
1. Cryptography & Security

Practical implementation of industry-standard encryption
Understanding of key derivation functions
Secure random number generation
Password hashing and verification

2. Software Engineering

Modular architecture (7 separate modules)
Object-oriented design patterns
Separation of concerns
Code reusability

3. Python Programming

Advanced OOP concepts
Type hints and annotations
Exception handling
File I/O operations
JSON serialization

4. User Experience

Intuitive command-line interface
Color-coded output
Clear error messages
Interactive workflows

5. Documentation

Professional README
Inline code documentation
Docstrings for all functions
Clear module structure

🛠️ Extension Ideas
Future enhancements:

Multi-user support with separate vaults
Cloud synchronization (encrypted)
Password expiry notifications
Two-factor authentication
Import/export (CSV, JSON)
Browser extension integration
GUI version (tkinter/PyQt)
Audit logging
Biometric authentication

🐛 Troubleshooting
Installation Issues
"No module named 'cryptography'"
bashpip install cryptography
# or
pip3 install cryptography
"Permission denied"
bash# Ensure write permissions in home directory
chmod +w ~/.securevault
Usage Issues
"Incorrect master password"

Master password is case-sensitive
Cannot be recovered if forgotten

"Vault already exists"

Delete existing vault to start fresh (use with caution):

bashrm -rf ~/.securevault
Platform-Specific
Windows: Use Command Prompt or PowerShell
macOS/Linux: Use Terminal
📄 License
MIT License - Free for educational and commercial use
👨‍💻 Author
B.Tech 4th Year Capstone Project
Computer Science & Engineering
Submitted: November 2025
🤝 Contributing
This is an academic project. Contributions welcome for:

Bug fixes
Feature enhancements
Documentation improvements
Security improvements

⚠️ Disclaimer
This is an educational project. While it implements strong security practices:

Has not undergone professional security audit
Not intended for production critical systems
For production use, consider: 1Password, Bitwarden, LastPass

For personal use:

Regular backups recommended
Keep master password secure
Don't share vault files

📚 References

Cryptography Library Documentation
OWASP Password Storage
NIST Password Guidelines
Python Security Best Practices
AES Encryption Standard


⚠️ Important: Always keep your master password safe. There is no password recovery mechanism. If you forget your master password, all stored passwords will be permanently inaccessible.
For educational purposes only. Use at your own risk.