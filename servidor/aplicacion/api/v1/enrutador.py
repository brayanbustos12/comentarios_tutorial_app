from fastapi import APIRouter

from aplicacion.api.v1.rutas import comentarios, salud, tutoriales

enrutador_api = APIRouter()

enrutador_api.include_router(salud.enrutador)
enrutador_api.include_router(tutoriales.enrutador)
enrutador_api.include_router(comentarios.enrutador)