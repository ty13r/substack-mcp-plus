# ABOUTME: AuthHandler class for managing Substack authentication
# ABOUTME: Supports automatic token management, refresh, and multiple auth methods

import os
import json
import logging
import tempfile
import asyncio
from typing import Optional, Dict, Any
from urllib.parse import urlparse
from datetime import datetime, timedelta
from substack import Api as SubstackApi
from src.simple_auth_manager import SimpleAuthManager
from src.utils.api_wrapper import APIWrapper

logger = logging.getLogger(__name__)


class AuthHandler:
    """Handles authentication for Substack API access with automatic token management"""
    
    # Cache for authenticated clients (in-memory for session)
    _client_cache: Dict[str, tuple[SubstackApi, datetime]] = {}
    _cache_duration = timedelta(minutes=30)  # Cache clients for 30 minutes
    
    def __init__(self):
        """Initialize the auth handler with automatic token management"""
        # Get publication URL (required)
        self.publication_url = os.getenv('SUBSTACK_PUBLICATION_URL')
        if not self.publication_url:
            raise ValueError("SUBSTACK_PUBLICATION_URL must be provided")
        
        # Validate URL format
        if not isinstance(self.publication_url, str):
            raise ValueError("Publication URL must be a string")
        
        try:
            parsed = urlparse(self.publication_url)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError("Invalid publication URL format")
        except Exception:
            raise ValueError("Invalid publication URL format")
        
        # Initialize auth manager for secure token storage (file-based, no keychain)
        self.auth_manager = SimpleAuthManager(self.publication_url)
        
        # Get credentials from environment (fallback)
        self.email = os.getenv('SUBSTACK_EMAIL')
        self.password = os.getenv('SUBSTACK_PASSWORD')
        self.env_session_token = os.getenv('SUBSTACK_SESSION_TOKEN')
        
        # Extract publication name from URL
        self.publication_name = self._extract_publication_name(self.publication_url)
        
        # Check if we have any valid auth method
        stored_token = self.auth_manager.get_token()
        has_env_auth = (self.email and self.password) or self.env_session_token
        
        if not stored_token and not has_env_auth:
            raise ValueError(
                "No authentication found. Please run 'python setup_auth.py' to configure authentication, "
                "or provide SUBSTACK_EMAIL/SUBSTACK_PASSWORD or SUBSTACK_SESSION_TOKEN environment variables."
            )
        
        logger.info(f"AuthHandler initialized for {self.publication_name}")
    
    def _extract_publication_name(self, url: str) -> str:
        """Extract the publication name from the Substack URL
        
        Args:
            url: The publication URL (e.g., https://example.substack.com)
            
        Returns:
            The publication name (e.g., 'example')
            
        Raises:
            ValueError: If URL parsing fails
        """
        if not url or not isinstance(url, str):
            raise ValueError("URL must be a non-empty string")
        parsed = urlparse(url)
        hostname = parsed.hostname or parsed.path
        
        # Remove .substack.com suffix if present
        if hostname.endswith('.substack.com'):
            return hostname[:-13]  # Remove '.substack.com'
        
        # Handle custom domains or other formats
        return hostname.split('.')[0]
    
    async def authenticate(self) -> SubstackApi:
        """Authenticate and return a Substack client with automatic token management
        
        Returns:
            An authenticated Substack client
            
        Raises:
            Exception: If all authentication methods fail
        """
        # Check cache first
        cache_key = self.publication_url
        if cache_key in self._client_cache:
            client, cached_at = self._client_cache[cache_key]
            if datetime.utcnow() - cached_at < self._cache_duration:
                logger.debug("Using cached client")
                return client
            else:
                # Remove expired cache
                del self._client_cache[cache_key]
        
        # Try stored token first (from AuthManager)
        stored_token = self.auth_manager.get_token()
        if stored_token:
            try:
                logger.info("Authenticating with stored token")
                client = self._create_session_client(stored_token)
                
                # Wrap the client for better error handling
                wrapped_client = APIWrapper(client)
                
                # Cache the wrapped client
                self._client_cache[cache_key] = (wrapped_client, datetime.utcnow())
                
                # Check if token needs refresh
                if self.auth_manager.needs_refresh():
                    logger.info("Token approaching expiry, scheduling refresh")
                    asyncio.create_task(self._refresh_token_background())
                
                return wrapped_client
                
            except Exception as e:
                logger.warning(f"Stored token authentication failed: {e}")
                # Clear invalid token
                self.auth_manager.clear_token()
        
        # Try environment variable session token
        if self.env_session_token:
            try:
                logger.info("Authenticating with environment session token")
                client = self._create_session_client(self.env_session_token)
                
                # Wrap the client for better error handling
                wrapped_client = APIWrapper(client)
                
                # Cache the wrapped client
                self._client_cache[cache_key] = (wrapped_client, datetime.utcnow())
                
                # Optionally store this token for future use
                if self.email:  # Only if we know the email
                    self.auth_manager.store_token(self.env_session_token, self.email)
                
                return wrapped_client
                
            except Exception as e:
                logger.warning(f"Environment session token failed: {e}")
        
        # Try email/password authentication
        if self.email and self.password:
            try:
                logger.info("Authenticating with email/password")
                client = SubstackApi(
                    email=self.email, 
                    password=self.password,
                    publication_url=self.publication_url
                )
                
                # Wrap the client for better error handling
                wrapped_client = APIWrapper(client)
                
                # Cache the wrapped client
                self._client_cache[cache_key] = (wrapped_client, datetime.utcnow())
                
                # Try to extract and store the session token for future use
                # This would require inspecting the client's session, which may not be exposed
                # For now, we just use the client as-is
                
                return wrapped_client
                
            except Exception as e:
                logger.error(f"Email/password authentication failed: {e}")
                if "captcha" in str(e).lower():
                    raise Exception(
                        "CAPTCHA detected. Please run 'python setup_auth.py' to authenticate "
                        "through the browser and set up automatic token management."
                    )
                raise
        
        raise Exception(
            "No valid authentication method available. "
            "Please run 'python setup_auth.py' to configure authentication."
        )
    
    def _create_session_client(self, session_token: str) -> SubstackApi:
        """Create a client using session token authentication
        
        Args:
            session_token: The session token to use
            
        Returns:
            A Substack client configured with session authentication
        """
        # Create simple cookie format that works
        cookies = {
            "substack.sid": session_token
        }
        
        # Save cookies to temporary file with secure permissions
        fd, cookies_path = tempfile.mkstemp(suffix='.json', text=True)
        try:
            # Set secure permissions (readable/writable by owner only)
            os.chmod(cookies_path, 0o600)
            
            # Write cookies to the file
            with os.fdopen(fd, 'w') as f:
                json.dump(cookies, f)
        except Exception:
            os.close(fd)
            os.unlink(cookies_path)
            raise
        
        try:
            # Create client with cookies
            client = SubstackApi(
                cookies_path=cookies_path,
                publication_url=self.publication_url
            )
            return client
        finally:
            # Clean up temporary file
            if os.path.exists(cookies_path):
                os.unlink(cookies_path)
    
    async def _refresh_token_background(self):
        """Background task to refresh token before expiry"""
        try:
            # This would require re-authenticating through the browser
            # For now, we just log that refresh is needed
            logger.info("Token refresh needed - user should run setup_auth.py again")
            
            # In a future enhancement, we could:
            # 1. Notify the user through the MCP interface
            # 2. Attempt automatic re-authentication if we have stored credentials
            # 3. Use a refresh token if Substack provides one
            
        except Exception as e:
            logger.error(f"Error in token refresh: {e}")
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers for session-based authentication
        
        Returns:
            Headers dict with authentication cookies
        """
        headers = {
            'User-Agent': 'substack-mcp-plus/2.0.0',
            'Content-Type': 'application/json',
        }
        
        # Try to get token from storage or environment
        token = self.auth_manager.get_token() or self.env_session_token
        
        if token:
            headers['Cookie'] = f'substack.sid={token}'
        
        return headers
    
    def clear_cache(self):
        """Clear the client cache"""
        self._client_cache.clear()
        logger.info("Client cache cleared")