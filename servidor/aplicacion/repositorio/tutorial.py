from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from aplicacion.esquema.tutorial import TutorialCrear
from aplicacion.modelo.tutorial import Tutorial


def crear_tutorial(
    sesion: Session,
    datos: TutorialCrear,
) -> Tutorial:
    tutorial = Tutorial(
        titulo=datos.titulo,
        descripcion=datos.descripcion,
        fecha_publicacion=datos.fecha_publicacion,
    )

    sesion.add(tutorial)

    return tutorial


def listar_tutoriales(
    sesion: Session,
) -> Sequence[Tutorial]:
    consulta = select(Tutorial).order_by(
        Tutorial.fecha_publicacion.desc(),
        Tutorial.id.desc(),
    )

    return sesion.scalars(consulta).all()


def obtener_tutorial_por_id(
    sesion: Session,
    tutorial_id: int,
) -> Tutorial | None:
    return sesion.get(Tutorial, tutorial_id)