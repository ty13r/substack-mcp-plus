# ABOUTME: Unit tests for SimpleAuthManager - safe coverage boost
# ABOUTME: Tests auth token storage without actual authentication

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from src.simple_auth_manager import SimpleAuthManager


class TestSimpleAuthManager:
    """Test SimpleAuthManager for secure token storage"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir
    
    @pytest.fixture
    def auth_manager(self, temp_dir):
        """Create auth manager with temporary directory"""
        with patch('src.simple_auth_manager.Path.home', return_value=Path(temp_dir)):
            return SimpleAuthManager("https://test.substack.com")
    
    def test_init_creates_directories(self, temp_dir):
        """Test that initialization creates necessary directories"""
        with patch('src.simple_auth_manager.Path.home', return_value=Path(temp_dir)):
            manager = SimpleAuthManager("https://test.substack.com")
            
            assert manager.config_dir.exists()
            assert manager.config_dir.name == '.substack-mcp-plus'
    
    def test_store_and_retrieve_token(self, auth_manager):
        """Test storing and retrieving a token"""
        # Store a token
        test_token = "test-session-token-123"
        test_email = "test@example.com"
        
        auth_manager.store_token(test_token, test_email, expires_in_days=30)
        
        # Retrieve the token
        retrieved = auth_manager.get_token()
        assert retrieved == test_token
    
    def test_clear_token(self, auth_manager):
        """Test clearing stored token"""
        # Store a token first
        auth_manager.store_token("test-token", "test@example.com")
        assert auth_manager.get_token() is not None
        
        # Clear it
        auth_manager.clear_token()
        assert auth_manager.get_token() is None
        assert not auth_manager.auth_file.exists()
    
    def test_get_metadata(self, auth_manager):
        """Test retrieving token metadata"""
        # Store a token
        auth_manager.store_token("test-token", "test@example.com", expires_in_days=7)
        
        # Get metadata
        metadata = auth_manager.get_metadata()
        assert metadata is not None
        assert metadata["email"] == "test@example.com"
        assert metadata["publication_url"] == "https://test.substack.com"
        assert "stored_at" in metadata
        assert "expires_at" in metadata
    
    def test_get_metadata_no_token(self, auth_manager):
        """Test getting metadata when no token exists"""
        metadata = auth_manager.get_metadata()
        assert metadata is None
    
    def test_needs_refresh_no_token(self, auth_manager):
        """Test needs_refresh when no token exists"""
        assert auth_manager.needs_refresh() is True
    
    def test_needs_refresh_fresh_token(self, auth_manager):
        """Test needs_refresh with fresh token"""
        # Store a token that expires in 30 days
        auth_manager.store_token("test-token", "test@example.com", expires_in_days=30)
        
        # Should not need refresh (expires in 30 days, threshold is 7)
        assert auth_manager.needs_refresh(days_before_expiry=7) is False
    
    def test_needs_refresh_expiring_soon(self, auth_manager):
        """Test needs_refresh with token expiring soon"""
        # Store a token that expires in 5 days
        auth_manager.store_token("test-token", "test@example.com", expires_in_days=5)
        
        # Should need refresh (expires in 5 days, threshold is 7)
        assert auth_manager.needs_refresh(days_before_expiry=7) is True
    
    def test_expired_token_returns_none(self, auth_manager):
        """Test that expired tokens return None"""
        # Store a token that expired 1 day ago
        auth_manager.store_token("test-token", "test@example.com", expires_in_days=-1)
        
        # Manually adjust the expiration date
        import json
        auth_data = json.loads(auth_manager.auth_file.read_text())
        auth_data["expires_at"] = (datetime.utcnow() - timedelta(days=1)).isoformat()
        auth_manager.auth_file.write_text(json.dumps(auth_data))
        
        # Should return None
        assert auth_manager.get_token() is None
    
    def test_token_for_different_publication(self, auth_manager):
        """Test token for different publication returns None"""
        # Store a token
        auth_manager.store_token("test-token", "test@example.com")
        
        # Manually change the publication URL in stored data
        import json
        auth_data = json.loads(auth_manager.auth_file.read_text())
        auth_data["publication_url"] = "https://different.substack.com"
        auth_manager.auth_file.write_text(json.dumps(auth_data))
        
        # Should return None (different publication)
        assert auth_manager.get_token() is None
    
    def test_file_permissions(self, auth_manager):
        """Test that files are created with secure permissions"""
        auth_manager.store_token("test-token", "test@example.com")
        
        # Check file permissions (should be 0o600 = readable/writable by owner only)
        auth_file_stat = auth_manager.auth_file.stat()
        auth_file_mode = auth_file_stat.st_mode & 0o777
        assert auth_file_mode == 0o600
        
        key_file_stat = auth_manager.key_file.stat()
        key_file_mode = key_file_stat.st_mode & 0o777
        assert key_file_mode == 0o600
    
    def test_encryption_works(self, auth_manager):
        """Test that encryption/decryption works correctly"""
        # Test that we can store and retrieve different tokens
        tokens = ["token1", "token2", "token3"]
        
        for token in tokens:
            auth_manager.store_token(token, f"test{token}@example.com")
            retrieved = auth_manager.get_token()
            assert retrieved == token
            auth_manager.clear_token()
        
        # Ensure no token remains
        assert auth_manager.get_token() is None