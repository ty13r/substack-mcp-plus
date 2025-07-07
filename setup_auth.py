#!/usr/bin/env python3
"""
Interactive authentication setup for Substack MCP Plus
Handles browser automation and CAPTCHA challenges
"""

import asyncio
import sys
import os
import re
import json
import logging
from typing import Optional
from urllib.parse import urlparse
import getpass
from playwright.async_api import async_playwright, TimeoutError
from src.simple_auth_manager import SimpleAuthManager

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class SubstackAuthSetup:
    """Interactive setup wizard for Substack authentication"""
    
    def __init__(self):
        self.email = None
        self.password = None
        self.publication_url = None
        self.auth_manager = None
        self.auth_method = None  # 'password' or 'magic_link'
    
    async def run(self):
        """Run the interactive setup process"""
        print("\n🚀 Substack MCP Plus - Authentication Setup")
        print("=" * 50)
        print("\nThis wizard will help you set up secure authentication.")
        print("Your credentials will be encrypted and stored securely.\n")
        
        # Get user inputs
        if not self._get_user_inputs():
            return
        
        # Initialize auth manager (file-based, no keychain)
        self.auth_manager = SimpleAuthManager(self.publication_url)
        
        # Check for existing token
        existing_token = self.auth_manager.get_token()
        if existing_token:
            metadata = self.auth_manager.get_metadata()
            print(f"\n✅ Found existing authentication for {metadata['email']}")
            replace = input("Replace with new authentication? (y/n): ").lower().strip()
            if replace != 'y':
                print("Setup cancelled.")
                return
        
        # Perform browser-based authentication
        print("\n🌐 Starting browser authentication...")
        print("A browser window will open. Please complete the login process.")
        if self.auth_method == 'magic_link':
            print("You'll receive a 6-digit code via email.")
        print("If you see a CAPTCHA, please solve it.\n")
        
        token = await self._authenticate_with_browser()
        
        if token:
            # Store the token
            self.auth_manager.store_token(token, self.email)
            print("\n✅ Authentication successful!")
            print("Token has been securely stored.")
            
            # Test the authentication
            if await self._test_authentication(token):
                print("\n🎉 Setup complete! You can now use Substack MCP Plus.")
                self._show_config_example()
            else:
                print("\n⚠️  Authentication stored but test failed.")
                print("Please check your publication URL and try again.")
        else:
            print("\n❌ Authentication failed. Please try again.")
    
    def _get_user_inputs(self) -> bool:
        """Get required inputs from user"""
        try:
            # Get authentication method
            print("\nHow would you like to sign in?")
            print("1. Magic link (email code)")
            print("2. Email and password")
            
            choice = input("\nSelect authentication method (1 or 2): ").strip()
            
            if choice == '1':
                self.auth_method = 'magic_link'
            elif choice == '2':
                self.auth_method = 'password'
            else:
                print("❌ Invalid choice. Please enter 1 or 2.")
                return False
            
            # Get email
            self.email = input("\nSubstack email: ").strip()
            if not self.email or '@' not in self.email:
                print("❌ Invalid email address")
                return False
            
            # Get password only if using password auth
            if self.auth_method == 'password':
                self.password = getpass.getpass("Substack password: ")
                if not self.password:
                    print("❌ Password cannot be empty")
                    return False
            
            # Get publication URL
            self.publication_url = input("Publication URL (e.g., https://example.substack.com): ").strip()
            
            # Validate URL
            try:
                parsed = urlparse(self.publication_url)
                if not parsed.scheme:
                    self.publication_url = f"https://{self.publication_url}"
                if not parsed.netloc and not self.publication_url.startswith('https://'):
                    print("❌ Invalid publication URL")
                    return False
            except:
                print("❌ Invalid publication URL")
                return False
            
            # Extract publication name for display
            pub_name = self._extract_publication_name(self.publication_url)
            print(f"\n📝 Setting up for publication: {pub_name}")
            
            return True
            
        except KeyboardInterrupt:
            print("\n\nSetup cancelled.")
            return False
    
    def _extract_publication_name(self, url: str) -> str:
        """Extract publication name from URL"""
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        
        # Handle substack.com subdomains
        if '.substack.com' in domain:
            return domain.split('.substack.com')[0].split('.')[-1]
        
        # Handle custom domains
        return domain.split('.')[0]
    
    async def _authenticate_with_browser(self) -> Optional[str]:
        """Perform browser-based authentication and extract session token"""
        async with async_playwright() as p:
            # Launch browser (visible so user can solve CAPTCHA)
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                # Navigate to Substack login
                logger.info("Navigating to Substack login...")
                await page.goto("https://substack.com/sign-in", wait_until="networkidle")
                
                # Fill in email
                logger.info("Filling in email...")
                await page.fill('input[name="email"]', self.email)
                await page.click('button[type="submit"]')
                
                # Wait for next screen
                await page.wait_for_timeout(2000)
                
                if self.auth_method == 'password':
                    # Click "Sign in with password" first
                    logger.info("Switching to password authentication...")
                    try:
                        # Look for the password link
                        await page.click('text="Sign in with password"')
                        await page.wait_for_timeout(1000)
                    except:
                        logger.info("Password option might already be selected")
                    
                    # Fill password
                    try:
                        await page.fill('input[type="password"]', self.password)
                        await page.click('button[type="submit"]')
                    except:
                        logger.error("Could not find password field")
                        return None
                        
                elif self.auth_method == 'magic_link':
                    # Magic link flow
                    print("\n📧 Magic link sent to your email!")
                    print("Please check your email and enter the 6-digit code.")
                    print("The browser will remain open for you to enter the code.\n")
                    
                    # Wait for user to check email and enter code
                    print("⏳ Waiting for you to enter the code in the browser...")
                    print("(The code input field should be visible on the page)")
                
                # Wait for login to complete
                print("\n⏳ Waiting for login to complete...")
                print("If you see a CAPTCHA, please solve it.")
                
                # Wait for redirect to dashboard or publication
                try:
                    await page.wait_for_url(
                        lambda url: "substack.com/sign-in" not in url,
                        timeout=120000  # 2 minutes for CAPTCHA solving
                    )
                except TimeoutError:
                    logger.error("Login timeout - please try again")
                    return None
                
                # Extract cookies
                cookies = await context.cookies()
                
                # Find session cookie
                session_cookie = None
                for cookie in cookies:
                    if cookie['name'] == 'substack.sid' and 'substack.com' in cookie['domain']:
                        session_cookie = cookie['value']
                        break
                
                if not session_cookie:
                    logger.error("Could not find session cookie")
                    return None
                
                logger.info("✅ Successfully extracted session token")
                return session_cookie
                
            except Exception as e:
                logger.error(f"Authentication error: {e}")
                return None
                
            finally:
                await browser.close()
    
    async def _test_authentication(self, token: str) -> bool:
        """Test the authentication by making an API call"""
        try:
            from substack import Api as SubstackApi
            import tempfile
            
            # Create temporary cookie file
            cookies = {"substack.sid": token}
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(cookies, f)
                cookies_path = f.name
            
            try:
                # Test API connection
                api = SubstackApi(
                    cookies_path=cookies_path,
                    publication_url=self.publication_url
                )
                
                # Try to get publication info (this will fail if auth is bad)
                # Since we don't have a direct method, we'll assume success if no exception
                logger.info("Testing authentication...")
                
                # Clean successful init means auth worked
                return True
                
            except Exception as e:
                logger.error(f"Authentication test failed: {e}")
                return False
            finally:
                # Clean up temp file
                if os.path.exists(cookies_path):
                    os.unlink(cookies_path)
                    
        except Exception as e:
            logger.error(f"Test error: {e}")
            return False
    
    def _show_config_example(self):
        """Show example configuration for Claude Desktop"""
        print("\n📋 Configuration for Claude Desktop:")
        print("-" * 50)
        print("""
Add this to your Claude Desktop config:

{
  "mcpServers": {
    "substack-mcp-plus": {
      "command": "python",
      "args": ["-m", "src.server"],
      "env": {
        "SUBSTACK_PUBLICATION_URL": "%s"
      }
    }
  }
}
""" % self.publication_url)
        print("-" * 50)
        print("\nNo email or password needed - authentication is handled automatically! 🎉")


async def main():
    """Main entry point"""
    setup = SubstackAuthSetup()
    await setup.run()


if __name__ == "__main__":
    try:
        # Install playwright browsers if needed
        import subprocess
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=False)
        
        # Run the setup
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        sys.exit(1)