from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Research Assistant"
    app_env: str = "development"

    secret_key: str = "supersecretkey"
    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"

    # Firebase
    firebase_key_path: str = "firebase_key.json"
    firebase_project_id: str = "researchassistant-ca18e"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Models
    llm_model: str = "llama2"
    embedding_model: str = "sentence-transformers/all-mpnet-base-v2"
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"

    vector_db_path: str = "./vectorstore/index.faiss"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
