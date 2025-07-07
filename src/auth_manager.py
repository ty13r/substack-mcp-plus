# ABOUTME: AuthManager class for secure token storage and automatic refresh
# ABOUTME: Handles encryption, keyring storage, and token lifecycle management

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import keyring
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

logger = logging.getLogger(__name__)


class AuthManager:
    """Manages authentication tokens with secure storage and automatic refresh"""
    
    SERVICE_NAME = "SubstackMCPPlus"
    TOKEN_KEY = "session_token"
    METADATA_KEY = "token_metadata"
    ENCRYPTION_KEY = "encryption_key"
    
    def __init__(self, publication_url: str):
        """Initialize the auth manager
        
        Args:
            publication_url: The Substack publication URL
        """
        self.publication_url = publication_url
        self.cipher = self._get_or_create_cipher()
    
    def _get_or_create_cipher(self) -> Fernet:
        """Get or create an encryption cipher for secure storage"""
        # Try to get existing encryption key from keyring
        key_data = keyring.get_password(self.SERVICE_NAME, self.ENCRYPTION_KEY)
        
        if key_data:
            key = base64.b64decode(key_data.encode())
        else:
            # Generate a new encryption key
            key = Fernet.generate_key()
            # Store it in keyring
            keyring.set_password(
                self.SERVICE_NAME, 
                self.ENCRYPTION_KEY, 
                base64.b64encode(key).decode()
            )
        
        return Fernet(key)
    
    def store_token(self, token: str, email: str, expires_in_days: int = 30) -> None:
        """Store an authentication token securely
        
        Args:
            token: The session token to store
            email: The email associated with the token
            expires_in_days: Number of days until token expires
        """
        # Encrypt the token
        encrypted_token = self.cipher.encrypt(token.encode())
        
        # Store encrypted token in keyring
        keyring.set_password(
            self.SERVICE_NAME,
            f"{self.TOKEN_KEY}:{self.publication_url}",
            base64.b64encode(encrypted_token).decode()
        )
        
        # Store metadata (unencrypted but in keyring)
        metadata = {
            "email": email,
            "stored_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(days=expires_in_days)).isoformat(),
            "publication_url": self.publication_url
        }
        
        keyring.set_password(
            self.SERVICE_NAME,
            f"{self.METADATA_KEY}:{self.publication_url}",
            json.dumps(metadata)
        )
        
        logger.info(f"Token stored securely for {email} at {self.publication_url}")
    
    def get_token(self) -> Optional[str]:
        """Retrieve the stored token if valid
        
        Returns:
            The decrypted token if valid, None otherwise
        """
        # Get encrypted token
        encrypted_data = keyring.get_password(
            self.SERVICE_NAME,
            f"{self.TOKEN_KEY}:{self.publication_url}"
        )
        
        if not encrypted_data:
            logger.debug("No stored token found")
            return None
        
        # Get metadata
        metadata_str = keyring.get_password(
            self.SERVICE_NAME,
            f"{self.METADATA_KEY}:{self.publication_url}"
        )
        
        if not metadata_str:
            logger.warning("Token found but no metadata")
            return None
        
        try:
            metadata = json.loads(metadata_str)
            expires_at = datetime.fromisoformat(metadata["expires_at"])
            
            # Check if token is expired
            if datetime.utcnow() > expires_at:
                logger.info("Stored token has expired")
                self.clear_token()
                return None
            
            # Decrypt and return token
            encrypted_token = base64.b64decode(encrypted_data.encode())
            token = self.cipher.decrypt(encrypted_token).decode()
            
            logger.info(f"Retrieved valid token for {metadata['email']}")
            return token
            
        except Exception as e:
            logger.error(f"Error retrieving token: {e}")
            return None
    
    def clear_token(self) -> None:
        """Clear stored token and metadata"""
        try:
            keyring.delete_password(
                self.SERVICE_NAME,
                f"{self.TOKEN_KEY}:{self.publication_url}"
            )
        except keyring.errors.PasswordDeleteError:
            pass
        
        try:
            keyring.delete_password(
                self.SERVICE_NAME,
                f"{self.METADATA_KEY}:{self.publication_url}"
            )
        except keyring.errors.PasswordDeleteError:
            pass
        
        logger.info("Cleared stored authentication data")
    
    def get_metadata(self) -> Optional[Dict[str, Any]]:
        """Get token metadata
        
        Returns:
            Token metadata dict or None
        """
        metadata_str = keyring.get_password(
            self.SERVICE_NAME,
            f"{self.METADATA_KEY}:{self.publication_url}"
        )
        
        if metadata_str:
            try:
                return json.loads(metadata_str)
            except:
                return None
        return None
    
    def needs_refresh(self, days_before_expiry: int = 7) -> bool:
        """Check if token needs refresh
        
        Args:
            days_before_expiry: Days before expiry to trigger refresh
            
        Returns:
            True if token needs refresh or doesn't exist
        """
        metadata = self.get_metadata()
        if not metadata:
            return True
        
        try:
            expires_at = datetime.fromisoformat(metadata["expires_at"])
            refresh_threshold = expires_at - timedelta(days=days_before_expiry)
            return datetime.utcnow() > refresh_threshold
        except:
            return True
    
    @staticmethod
    def list_stored_publications() -> list[str]:
        """List all publications with stored tokens
        
        Returns:
            List of publication URLs
        """
        publications = []
        try:
            # This is a workaround since keyring doesn't have a list function
            # We'll check common publication patterns
            import keyring.backends
            backend = keyring.get_keyring()
            
            # Try to get all stored items (implementation-specific)
            # For now, return empty list - users will need to know their publication URL
            return publications
        except:
            return publications