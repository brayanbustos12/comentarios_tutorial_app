from collections.abc import Sequence

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from aplicacion.esquema.comentario import (
    ComentarioActualizar,
    ComentarioCrear,
)
from aplicacion.modelo.comentario import Comentario
from aplicacion.repositorio import comentario as repositorio_comentario
from aplicacion.repositorio import tutorial as repositorio_tutorial
from aplicacion.servicio.tutorial import TutorialNoEncontradoError


class ComentarioNoEncontradoError(Exception):
    pass


def crear_comentario(
    sesion: Session,
    tutorial_id: int,
    datos: ComentarioCrear,
) -> Comentario:
    tutorial = repositorio_tutorial.obtener_tutorial_por_id(
        sesion=sesion,
        tutorial_id=tutorial_id,
    )

    if tutorial is None:
        raise TutorialNoEncontradoError

    comentario = repositorio_comentario.crear_comentario(
        sesion=sesion,
        tutorial_id=tutorial_id,
        datos=datos,
    )

    try:
        sesion.commit()
        sesion.refresh(comentario)
    except SQLAlchemyError:
        sesion.rollback()
        raise

    return comentario


def listar_comentarios(
    sesion: Session,
    tutorial_id: int,
) -> Sequence[Comentario]:
    tutorial = repositorio_tutorial.obtener_tutorial_por_id(
        sesion=sesion,
        tutorial_id=tutorial_id,
    )

    if tutorial is None:
        raise TutorialNoEncontradoError

    return repositorio_comentario.listar_comentarios_por_tutorial(
        sesion=sesion,
        tutorial_id=tutorial_id,
    )


def actualizar_comentario(
    sesion: Session,
    comentario_id: int,
    datos: ComentarioActualizar,
) -> Comentario:
    comentario = repositorio_comentario.obtener_comentario_por_id(
        sesion=sesion,
        comentario_id=comentario_id,
    )

    if comentario is None:
        raise ComentarioNoEncontradoError

    comentario = repositorio_comentario.actualizar_comentario(
        comentario=comentario,
        datos=datos,
    )

    try:
        sesion.commit()
        sesion.refresh(comentario)
    except SQLAlchemyError:
        sesion.rollback()
        raise

    return comentario


def eliminar_comentario(
    sesion: Session,
    comentario_id: int,
) -> None:
    comentario = repositorio_comentario.obtener_comentario_por_id(
        sesion=sesion,
        comentario_id=comentario_id,
    )

    if comentario is None:
        raise ComentarioNoEncontradoError

    repositorio_comentario.eliminar_comentario(
        sesion=sesion,
        comentario=comentario,
    )

    try:
        sesion.commit()
    except SQLAlchemyError:
        sesion.rollback()
        raise