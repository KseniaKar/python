from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Прямо указываем параметры
    db_host: str = "127.0.0.1"
    db_port: int = 5445
    db_name: str = "fastapi_project_db"
    db_username: str = "postgres_user"
    db_password: str = "postgres_pass"
    db_test_name: str = "fastapi_project_test_db"
    max_connection_count: int = 10

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def database_test_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_test_name}"


# Создаем настройки
settings = Settings()
