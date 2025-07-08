#!/usr/bin/env python3
"""
Check what methods are available on the Substack client
"""

import pytest
import sys
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.handlers.auth_handler import AuthHandler

async def check_client_methods():
    auth = AuthHandler()
    client = await auth.authenticate()
    
    print("Available methods on client:")
    methods = [method for method in dir(client) if not method.startswith('_')]
    for method in sorted(methods):
        print(f"  - {method}")
    
    # Check specifically for image upload methods
    image_methods = [method for method in methods if 'image' in method.lower() or 'upload' in method.lower()]
    print(f"\nImage/upload related methods:")
    for method in image_methods:
        print(f"  - {method}")

if __name__ == "__main__":
    asyncio.run(check_client_methods())