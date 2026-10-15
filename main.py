#!/usr/bin/env python3
"""
SecureVault - Advanced Password Manager CLI
Main Entry Point

A sophisticated command-line password manager with military-grade encryption
Author: B.Tech 4th Year Project
Date: November 2025
"""

import sys
from cli import SecureVaultCLI
from utils import ColorCodes


def main():
    """
    Application entry point
    Initializes and runs the SecureVault CLI
    """
    try:
        cli = SecureVaultCLI()
        cli.run()
    except KeyboardInterrupt:
        print(f"\n\n{ColorCodes.YELLOW}Interrupted by user. Exiting...{ColorCodes.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{ColorCodes.RED}Fatal error: {e}{ColorCodes.END}")
        sys.exit(1)


if __name__ == "__main__":
    main()