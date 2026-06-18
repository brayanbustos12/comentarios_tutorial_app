from fastapi import APIRouter

from aplicacion.api.v1.rutas import salud

enrutador_api = APIRouter()

enrutador_api.include_router(salud.enrutador)