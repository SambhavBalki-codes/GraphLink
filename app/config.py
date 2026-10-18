from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: str

    model_config = {"env_file": ".env"}


settings = Settings()