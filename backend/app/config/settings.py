from functools import lru_cache
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CloudLab Edu"
    app_env: str = "development"
    app_version: str = "1.3.3"
    app_secret: SecretStr = SecretStr("change-this-secret")
    database_url: str = "sqlite:///./practicum.db"
    cors_origins: str = "http://localhost:8000,http://127.0.0.1:8000,http://localhost:8080,http://127.0.0.1:8080"
    frontend_dir: str = "../frontend"
    simulate_health_failure: bool = False
    enable_failure_demo: bool = False
    # Default kredensial kelas harus tetap sama walaupun .env lama belum memiliki variabel ini.
    demo_admin_password: SecretStr = SecretStr("Admin@123")
    demo_dosen_password: SecretStr = SecretStr("Dosen@123")
    demo_mahasiswa_password: SecretStr = SecretStr("Mhs@12345")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_list(self) -> list[str]:
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

    @property
    def app_secret_value(self) -> str:
        return self.app_secret.get_secret_value()

    @property
    def demo_admin_password_value(self) -> str:
        return self.demo_admin_password.get_secret_value()

    @property
    def demo_dosen_password_value(self) -> str:
        return self.demo_dosen_password.get_secret_value()

    @property
    def demo_mahasiswa_password_value(self) -> str:
        return self.demo_mahasiswa_password.get_secret_value()


@lru_cache
def get_settings():
    return Settings()
