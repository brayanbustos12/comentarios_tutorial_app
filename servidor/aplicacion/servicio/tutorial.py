from collections.abc import Sequence

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from aplicacion.esquema.tutorial import TutorialCrear
from aplicacion.modelo.tutorial import Tutorial
from aplicacion.repositorio import tutorial as repositorio_tutorial


class TutorialNoEncontradoError(Exception):
    pass


def crear_tutorial(
    sesion: Session,
    datos: TutorialCrear,
) -> Tutorial:
    tutorial = repositorio_tutorial.crear_tutorial(
        sesion=sesion,
        datos=datos,
    )

    try:
        sesion.commit()
        sesion.refresh(tutorial)
    except SQLAlchemyError:
        sesion.rollback()
        raise

    return tutorial


def listar_tutoriales(
    sesion: Session,
) -> Sequence[Tutorial]:
    return repositorio_tutorial.listar_tutoriales(sesion)


def obtener_tutorial(
    sesion: Session,
    tutorial_id: int,
) -> Tutorial:
    tutorial = repositorio_tutorial.obtener_tutorial_por_id(
        sesion=sesion,
        tutorial_id=tutorial_id,
    )

    if tutorial is None:
        raise TutorialNoEncontradoError

    return tutorial