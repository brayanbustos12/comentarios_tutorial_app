from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from aplicacion.base_datos.dependencias import obtener_sesion
from aplicacion.esquema.tutorial import TutorialCrear, TutorialRespuesta
from aplicacion.servicio import tutorial as servicio_tutorial

enrutador = APIRouter(
    prefix="/tutoriales",
    tags=["Tutoriales"],
)

SesionBaseDatos = Annotated[Session, Depends(obtener_sesion)]


@enrutador.post(
    "",
    response_model=TutorialRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un tutorial",
)
def crear_tutorial(
    datos: TutorialCrear,
    sesion: SesionBaseDatos,
) -> TutorialRespuesta:
    return servicio_tutorial.crear_tutorial(
        sesion=sesion,
        datos=datos,
    )


@enrutador.get(
    "",
    response_model=list[TutorialRespuesta],
    summary="Listar los tutoriales",
)
def listar_tutoriales(
    sesion: SesionBaseDatos,
) -> list[TutorialRespuesta]:
    return list(servicio_tutorial.listar_tutoriales(sesion))


@enrutador.get(
    "/{tutorial_id}",
    response_model=TutorialRespuesta,
    summary="Consultar un tutorial",
)
def obtener_tutorial(
    tutorial_id: int,
    sesion: SesionBaseDatos,
) -> TutorialRespuesta:
    try:
        return servicio_tutorial.obtener_tutorial(
            sesion=sesion,
            tutorial_id=tutorial_id,
        )
    except servicio_tutorial.TutorialNoEncontradoError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El tutorial solicitado no existe",
        ) from error