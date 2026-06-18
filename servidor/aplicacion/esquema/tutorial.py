from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TutorialBase(BaseModel):
    titulo: str = Field(
        min_length=3,
        max_length=200,
        examples=["Introducción a FastAPI"],
    )

    descripcion: str = Field(
        min_length=10,
        examples=["Tutorial para aprender los fundamentos de FastAPI."],
    )

    fecha_publicacion: datetime = Field(
        examples=["2026-06-18T10:00:00-05:00"],
    )

    @field_validator("titulo", "descripcion")
    @classmethod
    def eliminar_espacios_externos(cls, valor: str) -> str:
        valor_limpio = valor.strip()

        if not valor_limpio:
            raise ValueError("El campo no puede contener solamente espacios")

        return valor_limpio


class TutorialCrear(TutorialBase):
    pass


class TutorialRespuesta(TutorialBase):
    id: int

    model_config = ConfigDict(from_attributes=True)