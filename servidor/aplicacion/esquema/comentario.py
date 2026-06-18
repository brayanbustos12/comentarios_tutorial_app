from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ComentarioBase(BaseModel):
    contenido: str = Field(
        min_length=1,
        max_length=5000,
        examples=["El tutorial fue claro y útil."],
    )

    @field_validator("contenido")
    @classmethod
    def validar_contenido(cls, valor: str) -> str:
        valor_limpio = valor.strip()

        if not valor_limpio:
            raise ValueError(
                "El contenido no puede contener solamente espacios"
            )

        return valor_limpio


class ComentarioCrear(ComentarioBase):
    pass


class ComentarioActualizar(ComentarioBase):
    pass


class ComentarioRespuesta(ComentarioBase):
    id: int
    tutorial_id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)