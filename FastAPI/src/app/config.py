import os


class Settings:
    PROJECT_NAME: str = "Spatial Data"
    PROJECT_VERSION: str = "1.0.0.0"
    CONTACT: dict = {
        "name": "Priyansh Bordia",
        "url": "https://priyanshbordia.github.io",
        "email": "",
    }

    POSTGRES_USER: str = str(os.getenv("DB_USERNAME"))
    POSTGRES_PASSWORD: str = str(os.getenv("DB_PASSWORD"))
    POSTGRES_SERVER: str = str(os.getenv("DB_HOST"))
    POSTGRES_PORT: int = int(os.getenv("DB_PORT", 5432))
    POSTGRES_DB: str = str(os.getenv("DB_NAME"))
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    MODEL_NAME = "countries_country"


settings = Settings()
