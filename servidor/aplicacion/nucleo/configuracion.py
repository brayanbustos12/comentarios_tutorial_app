from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

RUTA_PROYECTO = Path(__file__).resolve().parents[3]


class Configuracion(BaseSettings):
    base_datos_url: str

    model_config = SettingsConfigDict(
        env_file=RUTA_PROYECTO / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def obtener_configuracion() -> Configuracion:
    return Configuracion()