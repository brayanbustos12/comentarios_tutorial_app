from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from aplicacion.base_datos.dependencias import obtener_sesion
from aplicacion.esquema.comentario import (
    ComentarioActualizar,
    ComentarioCrear,
    ComentarioRespuesta,
)
from aplicacion.servicio import comentario as servicio_comentario
from aplicacion.servicio.tutorial import TutorialNoEncontradoError

enrutador = APIRouter(tags=["Comentarios"])

SesionBaseDatos = Annotated[Session, Depends(obtener_sesion)]


@enrutador.post(
    "/tutoriales/{tutorial_id}/comentarios",
    response_model=ComentarioRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un comentario",
)
def crear_comentario(
    tutorial_id: int,
    datos: ComentarioCrear,
    sesion: SesionBaseDatos,
) -> ComentarioRespuesta:
    try:
        return servicio_comentario.crear_comentario(
            sesion=sesion,
            tutorial_id=tutorial_id,
            datos=datos,
        )
    except TutorialNoEncontradoError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El tutorial solicitado no existe",
        ) from error


@enrutador.get(
    "/tutoriales/{tutorial_id}/comentarios",
    response_model=list[ComentarioRespuesta],
    summary="Listar los comentarios de un tutorial",
)
def listar_comentarios(
    tutorial_id: int,
    sesion: SesionBaseDatos,
) -> list[ComentarioRespuesta]:
    try:
        return list(
            servicio_comentario.listar_comentarios(
                sesion=sesion,
                tutorial_id=tutorial_id,
            )
        )
    except TutorialNoEncontradoError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El tutorial solicitado no existe",
        ) from error


@enrutador.put(
    "/comentarios/{comentario_id}",
    response_model=ComentarioRespuesta,
    summary="Reemplazar un comentario",
)
def actualizar_comentario(
    comentario_id: int,
    datos: ComentarioActualizar,
    sesion: SesionBaseDatos,
) -> ComentarioRespuesta:
    try:
        return servicio_comentario.actualizar_comentario(
            sesion=sesion,
            comentario_id=comentario_id,
            datos=datos,
        )
    except servicio_comentario.ComentarioNoEncontradoError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El comentario solicitado no existe",
        ) from error


@enrutador.delete(
    "/comentarios/{comentario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un comentario",
)
def eliminar_comentario(
    comentario_id: int,
    sesion: SesionBaseDatos,
) -> None:
    try:
        servicio_comentario.eliminar_comentario(
            sesion=sesion,
            comentario_id=comentario_id,
        )
    except servicio_comentario.ComentarioNoEncontradoError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El comentario solicitado no existe",
        ) from error