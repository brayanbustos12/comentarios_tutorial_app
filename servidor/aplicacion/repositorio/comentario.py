from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from aplicacion.esquema.comentario import (
    ComentarioActualizar,
    ComentarioCrear,
)
from aplicacion.modelo.comentario import Comentario


def crear_comentario(
    sesion: Session,
    tutorial_id: int,
    datos: ComentarioCrear,
) -> Comentario:
    comentario = Comentario(
        contenido=datos.contenido,
        tutorial_id=tutorial_id,
    )

    sesion.add(comentario)

    return comentario


def listar_comentarios_por_tutorial(
    sesion: Session,
    tutorial_id: int,
) -> Sequence[Comentario]:
    consulta = (
        select(Comentario)
        .where(Comentario.tutorial_id == tutorial_id)
        .order_by(
            Comentario.fecha_creacion.asc(),
            Comentario.id.asc(),
        )
    )

    return sesion.scalars(consulta).all()


def obtener_comentario_por_id(
    sesion: Session,
    comentario_id: int,
) -> Comentario | None:
    return sesion.get(Comentario, comentario_id)


def actualizar_comentario(
    comentario: Comentario,
    datos: ComentarioActualizar,
) -> Comentario:
    comentario.contenido = datos.contenido

    return comentario


def eliminar_comentario(
    sesion: Session,
    comentario: Comentario,
) -> None:
    sesion.delete(comentario)