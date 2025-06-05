from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./drumschool.db"
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    admin_email: str = "admin@drumschool.com"
    admin_password: str = "admin123"
    
    class Config:
        env_file = ".env"

settings = Settings()
