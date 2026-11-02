
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    NEON_DATABASE_URL: str | None = None
    USE_NEON: bool = False
    CORS_ORIGINS: str = "http://localhost:5174"

    model_config = {"env_file": ".env", "extra": "ignore"}

    @property
    def database_url(self) -> str:
        if self.USE_NEON:
            if not self.NEON_DATABASE_URL:
                raise ValueError("NEON_DATABASE_URL is required when USE_NEON is enabled")
            return self.NEON_DATABASE_URL.replace(
                "postgresql://", "postgresql+psycopg://", 1
            )
        return self.DATABASE_URL

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]


settings = Settings()
