from fastapi import FastAPI

from aplicacion.api.v1.enrutador import enrutador_api
from fastapi.responses import RedirectResponse


def crear_aplicacion() -> FastAPI:
    aplicacion = FastAPI(
        title="API de tutoriales y comentarios",
        description=(
            "API REST para registrar tutoriales y administrar sus comentarios."
        ),
        version="0.1.0",
    )

    aplicacion.include_router(
        enrutador_api,
        prefix="/api/v1",
    )    

    return aplicacion

aplicacion = crear_aplicacion()

@aplicacion.get("/", include_in_schema=False)
def mostrar_documentacion() -> RedirectResponse:
    return RedirectResponse(url="/docs")