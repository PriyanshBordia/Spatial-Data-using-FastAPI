import os


class Settings:
    PROJECT_NAME: str = "Spatial Data"
    PROJECT_VERSION: str = "1.0.0.0"

    POSTGRES_USER: str = str(os.getenv("DB_USER"))
    POSTGRES_PASSWORD: str = str(os.getenv("DB_PASSWORD"))
    POSTGRES_SERVER: str = str(os.getenv("DB_HOST"))
    POSTGRES_PORT: int = int(os.getenv("DB_PORT"))  # type: ignore
    POSTGRES_DB: str = str(os.getenv("DB_NAME"))
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


settings = Settings()
