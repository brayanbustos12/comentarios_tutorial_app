from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, Identity, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from aplicacion.base_datos.base import Base

if TYPE_CHECKING:
    from aplicacion.modelo.comentario import Comentario


class Tutorial(Base):
    __tablename__ = "tutoriales"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(),
        primary_key=True,
    )

    titulo: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    descripcion: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    fecha_publicacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    comentarios: Mapped[list["Comentario"]] = relationship(
        back_populates="tutorial",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )