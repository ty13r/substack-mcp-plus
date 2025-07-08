# ABOUTME: Unit tests for AuthHandler class that manages Substack authentication
# ABOUTME: Tests both email/password and session token authentication methods

import pytest
import os
from unittest.mock import Mock, patch, AsyncMock
from src.handlers.auth_handler import AuthHandler
from src.utils.api_wrapper import APIWrapper


class TestAuthHandler:
    """Test suite for AuthHandler class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        # Clear any existing env vars
        for key in ['SUBSTACK_EMAIL', 'SUBSTACK_PASSWORD', 'SUBSTACK_SESSION_TOKEN', 
                    'SUBSTACK_PUBLICATION_URL']:
            if key in os.environ:
                del os.environ[key]
    
    def test_init_with_email_password(self):
        """Test initialization with email and password"""
        with patch.dict(os.environ, {
            'SUBSTACK_EMAIL': 'test@example.com',
            'SUBSTACK_PASSWORD': 'testpass123',
            'SUBSTACK_PUBLICATION_URL': 'https://test.substack.com'
        }):
            handler = AuthHandler()
            assert handler.email == 'test@example.com'
            assert handler.password == 'testpass123'
            assert handler.publication_url == 'https://test.substack.com'
            assert handler.env_session_token is None
    
    def test_init_with_session_token(self):
        """Test initialization with session token"""
        with patch.dict(os.environ, {
            'SUBSTACK_SESSION_TOKEN': 'test-session-token',
            'SUBSTACK_PUBLICATION_URL': 'https://test.substack.com'
        }):
            handler = AuthHandler()
            assert handler.email is None
            assert handler.password is None
            assert handler.env_session_token == 'test-session-token'
            assert handler.publication_url == 'https://test.substack.com'
    
    def test_init_missing_credentials(self):
        """Test initialization with missing credentials raises error"""
        with patch.dict(os.environ, {
            'SUBSTACK_PUBLICATION_URL': 'https://test.substack.com'
        }):
            with pytest.raises(ValueError, match="No authentication found"):
                AuthHandler()
    
    def test_init_missing_publication_url(self):
        """Test initialization without publication URL raises error"""
        with patch.dict(os.environ, {
            'SUBSTACK_EMAIL': 'test@example.com',
            'SUBSTACK_PASSWORD': 'testpass123'
        }):
            with pytest.raises(ValueError, match="SUBSTACK_PUBLICATION_URL must be provided"):
                AuthHandler()
    
    @pytest.mark.asyncio
    async def test_authenticate_with_email_password(self):
        """Test authentication using email and password"""
        with patch.dict(os.environ, {
            'SUBSTACK_EMAIL': 'test@example.com',
            'SUBSTACK_PASSWORD': 'testpass123',
            'SUBSTACK_PUBLICATION_URL': 'https://test.substack.com'
        }):
            handler = AuthHandler()
            
            # Mock the Substack client
            mock_client = Mock()
            
            with patch('src.handlers.auth_handler.SubstackApi', return_value=mock_client) as mock_api:
                client = await handler.authenticate()
                
                assert isinstance(client, APIWrapper)
                mock_api.assert_called_once_with(
                    email='test@example.com',
                    password='testpass123',
                    publication_url='https://test.substack.com'
                )
    
    @pytest.mark.asyncio
    async def test_authenticate_with_session_token(self):
        """Test authentication using session token"""
        with patch.dict(os.environ, {
            'SUBSTACK_SESSION_TOKEN': 'test-session-token',
            'SUBSTACK_PUBLICATION_URL': 'https://test.substack.com'
        }):
            handler = AuthHandler()
            
            # Mock creating a client with session
            mock_client = Mock()
            
            with patch.object(handler, '_create_session_client', return_value=mock_client):
                client = await handler.authenticate()
                
                assert isinstance(client, APIWrapper)
    
    @pytest.mark.asyncio
    async def test_authenticate_email_fallback_to_session(self):
        """Test fallback to session token when email auth fails"""
        with patch.dict(os.environ, {
            'SUBSTACK_EMAIL': 'test@example.com',
            'SUBSTACK_PASSWORD': 'wrongpass',
            'SUBSTACK_SESSION_TOKEN': 'fallback-token',
            'SUBSTACK_PUBLICATION_URL': 'https://test.substack.com'
        }):
            handler = AuthHandler()
            
            # Mock failed email auth and successful session auth
            mock_session_client = Mock()
            
            with patch('src.handlers.auth_handler.SubstackApi', side_effect=Exception("Invalid credentials")):
                with patch.object(handler, '_create_session_client', return_value=mock_session_client):
                    client = await handler.authenticate()
                    
                    assert isinstance(client, APIWrapper)
    
    @pytest.mark.asyncio
    async def test_authenticate_all_methods_fail(self):
        """Test when all authentication methods fail"""
        # Mock the auth manager to prevent loading real tokens
        with patch('src.handlers.auth_handler.SimpleAuthManager') as mock_auth_manager:
            mock_auth_manager.return_value.get_token.return_value = None
            
            # First create the handler with required env vars
            with patch.dict(os.environ, {
                'SUBSTACK_EMAIL': 'test@example.com',
                'SUBSTACK_PASSWORD': 'wrongpass',
                'SUBSTACK_PUBLICATION_URL': 'https://test.substack.com'
            }, clear=True):  # Clear all env vars to ensure no session token
                handler = AuthHandler()
                # Clear the client cache that might be populated from other tests
                handler._client_cache.clear()
                
                # Mock failed email auth
                with patch('src.handlers.auth_handler.SubstackApi', side_effect=Exception("Invalid credentials")):
                    with pytest.raises(Exception, match="Invalid credentials"):
                        await handler.authenticate()
    
    def test_get_headers_with_session(self):
        """Test getting headers for session-based authentication"""
        with patch.dict(os.environ, {
            'SUBSTACK_SESSION_TOKEN': 'test-session-token',
            'SUBSTACK_PUBLICATION_URL': 'https://test.substack.com'
        }):
            handler = AuthHandler()
            headers = handler.get_headers()
            
            assert headers['Cookie'] == 'substack.sid=test-session-token'
            assert headers['User-Agent'].startswith('substack-mcp-plus/')
            assert 'Content-Type' in headers
    
    def test_create_session_client(self):
        """Test creating a session-based client"""
        with patch.dict(os.environ, {
            'SUBSTACK_SESSION_TOKEN': 'test-session-token',
            'SUBSTACK_PUBLICATION_URL': 'https://test.substack.com'
        }):
            handler = AuthHandler()
            
            # This would typically create a custom client
            # For now, we'll just verify the method exists
            assert hasattr(handler, '_create_session_client')
    
    def test_publication_name_extraction(self):
        """Test extracting publication name from URL"""
        test_cases = [
            ('https://test.substack.com', 'test'),
            ('https://example.substack.com/', 'example'),
            ('https://my-publication.substack.com/about', 'my-publication'),
        ]
        
        for url, expected_name in test_cases:
            with patch.dict(os.environ, {
                'SUBSTACK_EMAIL': 'test@example.com',
                'SUBSTACK_PASSWORD': 'testpass',
                'SUBSTACK_PUBLICATION_URL': url
            }):
                handler = AuthHandler()
                assert handler.publication_name == expected_name