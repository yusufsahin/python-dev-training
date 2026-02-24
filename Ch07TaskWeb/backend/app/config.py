"""Uygulama ayarları (DB path, env)."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Ortam değişkenleri ve varsayılanlar."""

    database_url: str = "sqlite:///./tasks.db"
    # Ch07TaskWeb/backend'den çalıştırılıyorsa ./tasks.db proje içinde oluşur

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    def get_engine_url(self) -> str:
        """SQLite için check_same_thread=False gerekir; URL döndürülür."""
        return self.database_url


settings = Settings()
