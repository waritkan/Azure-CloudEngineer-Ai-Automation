"""
Configuration Management
Loads settings from environment variables
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "Azure AI Automation"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # Azure Credentials (required for real Azure operations)
    AZURE_SUBSCRIPTION_ID: Optional[str] = None
    AZURE_CLIENT_ID: Optional[str] = None
    AZURE_CLIENT_SECRET: Optional[str] = None
    AZURE_TENANT_ID: Optional[str] = None

    # Azure Settings
    AZURE_RESOURCE_GROUP: str = "rg-ai-automation"
    AZURE_REGION: str = "southeastasia"

    # AI Configuration (OpenRouter)
    OPENAI_API_KEY: Optional[str] = None  # Use OpenRouter API key here
    OPENAI_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENAI_MODEL: str = "openai/gpt-4-turbo"  # OpenRouter model format

    # Optional: Your app info for OpenRouter
    APP_URL: str = "https://github.com/your-username/azure-ai-automation"
    APP_TITLE: str = "Azure AI Automation"

    # Budget Control
    MONTHLY_BUDGET_LIMIT: float = 10.0  # $10 USD
    ENABLE_MOCK_MODE: bool = True  # Start with mock mode for safety

    # VM Settings
    ALLOWED_VM_SIZES: list = ["B1s"]  # Only allow cheapest VM
    ALLOWED_REGIONS: list = ["southeastasia", "eastasia"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings"""
    return settings


def is_azure_configured() -> bool:
    """Check if Azure credentials are configured"""
    required = [
        settings.AZURE_SUBSCRIPTION_ID,
        settings.AZURE_CLIENT_ID,
        settings.AZURE_CLIENT_SECRET,
        settings.AZURE_TENANT_ID,
    ]
    return all(required)


def is_openai_configured() -> bool:
    """Check if OpenAI API key is configured"""
    return settings.OPENAI_API_KEY is not None


def get_mode() -> str:
    """Get current operation mode"""
    if settings.ENABLE_MOCK_MODE:
        return "mock"
    elif is_azure_configured():
        return "azure"
    else:
        return "unconfigured"


# Print configuration status on import
if __name__ != "__main__":
    print(f"\n{'='*50}")
    print(f">> {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"{'='*50}")
    print(f"Mode: {get_mode().upper()}")
    print(f"Azure Configured: {'OK' if is_azure_configured() else 'NO'}")
    print(f"OpenAI Configured: {'OK' if is_openai_configured() else 'NO'}")
    print(f"Budget Limit: ${settings.MONTHLY_BUDGET_LIMIT:.2f}/month")
    print(f"Allowed VM Sizes: {', '.join(settings.ALLOWED_VM_SIZES)}")
    print(f"{'='*50}\n")
