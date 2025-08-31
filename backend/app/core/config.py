from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Research Assistant"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    database_url: str = "sqlite:///./research_assistant.db"
    redis_url: str = "redis://localhost:6379/0"

    secret_key: str = "supersecretkey"   # load from .env in production
    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"

    llm_model: str = "llama2"
    embedding_model: str = "sentence-transformers/all-mpnet-base-v2"
    vector_db_path: str = "./vectorstore/index.faiss"

    log_level: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
