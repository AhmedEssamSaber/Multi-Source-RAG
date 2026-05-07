from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # APIs
    GROQ_API_KEY: str

    # Models
    EMBEDDING_MODEL: str
    GENERATION_MODEL: str

    # DB
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_MAIN_DATABASE: str

    DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()