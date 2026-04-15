from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME : str = "Auth Service"

    DB_HOST: str
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()