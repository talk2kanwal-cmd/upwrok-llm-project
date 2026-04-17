import os
from .security import security

class Settings:
    PROJECT_NAME: str = "AI Customer Support API"
    
    @property
    def GROQ_API_KEY(self) -> str:
        """Get Groq API key securely."""
        api_key = security.get_api_key("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment or secure storage")
        return api_key
    
    @property
    def OPENAI_API_KEY(self) -> str:
        """Get OpenAI API key securely (optional)."""
        return security.get_api_key("OPENAI_API_KEY")
    
    @property
    def ENVIRONMENT(self) -> str:
        """Get environment (development/production)."""
        return os.getenv("ENVIRONMENT", "development").lower()
    
    @property
    def DEBUG(self) -> bool:
        """Debug mode based on environment."""
        return self.ENVIRONMENT == "development"
    
    @property
    def LOG_LEVEL(self) -> str:
        """Log level based on environment."""
        return os.getenv("LOG_LEVEL", "DEBUG" if self.DEBUG else "INFO")

settings = Settings()
