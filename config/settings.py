from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    base_url: str = "https://petstore3.swagger.io/api/v3"
    api_key: str = ""
    timeout: float = 10
    retry_count: int = 2


settings = Settings()
