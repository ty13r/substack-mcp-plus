# ABOUTME: SimpleAuthManager class for file-based token storage without keychain
# ABOUTME: Uses encrypted local file storage to avoid macOS keychain password prompts

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from pathlib import Path
from cryptography.fernet import Fernet
import base64

logger = logging.getLogger(__name__)


class SimpleAuthManager:
    """Manages authentication tokens with local file storage (no keychain)"""

    def __init__(self, publication_url: str):
        """Initialize the auth manager

        Args:
            publication_url: The Substack publication URL
        """
        self.publication_url = publication_url

        # Use a consistent location in user's home directory
        self.config_dir = Path.home() / ".substack-mcp-plus"
        self.config_dir.mkdir(exist_ok=True)

        self.auth_file = self.config_dir / "auth.json"
        self.key_file = self.config_dir / ".key"

        self.cipher = self._get_or_create_cipher()

    def _get_or_create_cipher(self) -> Fernet:
        """Get or create an encryption cipher for secure storage"""
        if self.key_file.exists():
            key = self.key_file.read_bytes()
        else:
            key = Fernet.generate_key()
            self.key_file.write_bytes(key)
            # Set restrictive permissions on key file
            os.chmod(self.key_file, 0o600)

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

        # Store auth data
        auth_data = {
            "token": base64.b64encode(encrypted_token).decode(),
            "email": email,
            "stored_at": datetime.utcnow().isoformat(),
            "expires_at": (
                datetime.utcnow() + timedelta(days=expires_in_days)
            ).isoformat(),
            "publication_url": self.publication_url,
        }

        # Write to file with restrictive permissions
        self.auth_file.write_text(json.dumps(auth_data, indent=2))
        os.chmod(self.auth_file, 0o600)

        logger.info(f"Token stored securely for {email} at {self.publication_url}")

    def get_token(self) -> Optional[str]:
        """Retrieve the stored token if valid

        Returns:
            The decrypted token if valid, None otherwise
        """
        if not self.auth_file.exists():
            logger.debug("No stored token found")
            return None

        try:
            auth_data = json.loads(self.auth_file.read_text())

            # Check if it's for the right publication
            if auth_data.get("publication_url") != self.publication_url:
                logger.debug("Token is for different publication")
                return None

            expires_at = datetime.fromisoformat(auth_data["expires_at"])

            # Check if token is expired
            if datetime.utcnow() > expires_at:
                logger.info("Stored token has expired")
                self.clear_token()
                return None

            # Decrypt and return token
            encrypted_token = base64.b64decode(auth_data["token"].encode())
            token = self.cipher.decrypt(encrypted_token).decode()

            logger.info(f"Retrieved valid token for {auth_data['email']}")
            return token

        except Exception as e:
            logger.error(f"Error retrieving token: {e}")
            return None

    def clear_token(self) -> None:
        """Clear stored token"""
        if self.auth_file.exists():
            self.auth_file.unlink()
        logger.info("Cleared stored authentication data")

    def get_metadata(self) -> Optional[Dict[str, Any]]:
        """Get token metadata

        Returns:
            Token metadata dict or None
        """
        if not self.auth_file.exists():
            return None

        try:
            auth_data = json.loads(self.auth_file.read_text())
            return {
                "email": auth_data.get("email"),
                "stored_at": auth_data.get("stored_at"),
                "expires_at": auth_data.get("expires_at"),
                "publication_url": auth_data.get("publication_url"),
            }
        except:
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
