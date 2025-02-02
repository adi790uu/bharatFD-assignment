import os


from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_PREFIX: str = "/api"
    DATABASE_URL: str
    REDIS_URL: str
    TEST_DATABASE_URL: str = None


class DevelopmentSettings(Settings):
    model_config = SettingsConfigDict(env_file=".env.development")


class TestSettings(Settings):
    model_config = SettingsConfigDict(env_file=".env.test")


class ProductionSettings(Settings):
    model_config = SettingsConfigDict(env_file=".env.production")


def get_settings() -> Settings:
    if os.getenv("APP_ENV", "development") == "production":
        return ProductionSettings()
    elif os.getenv("APP_ENV", "development") == "test":
        return TestSettings()
    else:
        return DevelopmentSettings()


settings = get_settings()
