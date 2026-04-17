import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import secrets
from typing import Optional

class SecureConfig:
    """Secure configuration management with API key encryption."""
    
    def __init__(self):
        self.key_file = os.getenv("ENCRYPTION_KEY_FILE", ".encryption_key")
        self.fernet = self._get_or_create_encryption_key()
    
    def _get_or_create_encryption_key(self) -> Fernet:
        """Get existing encryption key or create new one."""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                key = f.read()
        else:
            # Generate new encryption key
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            # Set file permissions (read/write only for owner)
            os.chmod(self.key_file, 0o600)
        
        return Fernet(key)
    
    def encrypt_api_key(self, api_key: str) -> str:
        """Encrypt API key for secure storage."""
        encrypted = self.fernet.encrypt(api_key.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt_api_key(self, encrypted_key: str) -> str:
        """Decrypt API key from secure storage."""
        encrypted_bytes = base64.b64decode(encrypted_key.encode())
        decrypted = self.fernet.decrypt(encrypted_bytes)
        return decrypted.decode()
    
    def get_api_key(self, env_var: str = "GROQ_API_KEY") -> Optional[str]:
        """Get API key from environment with fallback to encrypted storage."""
        # First try environment variable
        api_key = os.getenv(env_var)
        if api_key and api_key.strip():
            return api_key.strip()
        
        # Fallback to encrypted storage
        encrypted_key_file = f".{env_var.lower()}_encrypted"
        if os.path.exists(encrypted_key_file):
            try:
                with open(encrypted_key_file, 'r') as f:
                    encrypted_key = f.read().strip()
                return self.decrypt_api_key(encrypted_key)
            except Exception:
                pass
        
        return None
    
    def store_api_key(self, api_key: str, env_var: str = "GROQ_API_KEY"):
        """Store API key in encrypted format."""
        encrypted_key = self.encrypt_api_key(api_key)
        encrypted_key_file = f".{env_var.lower()}_encrypted"
        with open(encrypted_key_file, 'w') as f:
            f.write(encrypted_key)
        os.chmod(encrypted_key_file, 0o600)
    
    def generate_session_token(self) -> str:
        """Generate secure session token."""
        return secrets.token_urlsafe(32)

# Global security instance
security = SecureConfig()
