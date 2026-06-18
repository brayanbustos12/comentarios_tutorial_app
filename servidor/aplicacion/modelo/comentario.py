from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, ForeignKey, Identity, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from aplicacion.base_datos.base import Base

if TYPE_CHECKING:
    from aplicacion.modelo.tutorial import Tutorial


class Comentario(Base):
    __tablename__ = "comentarios"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(),
        primary_key=True,
    )

    contenido: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    tutorial_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "tutoriales.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    tutorial: Mapped["Tutorial"] = relationship(
        back_populates="comentarios",
    )