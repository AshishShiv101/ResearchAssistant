from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Research Assistant"
    app_env: str = "development"

    secret_key: str = "supersecretkey"
    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"

    # Firebase
    firebase_key_path: str = "firebase_key.json"
    project_id: str = "researchassistant-ca18e"

    llm_model: str = "llama2"
    embedding_model: str = "sentence-transformers/all-mpnet-base-v2"
    vector_db_path: str = "./vectorstore/index.faiss"

    log_level: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
