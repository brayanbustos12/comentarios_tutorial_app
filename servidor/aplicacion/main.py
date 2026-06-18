from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from aplicacion.api.v1.enrutador import enrutador_api
from aplicacion.nucleo.configuracion import obtener_configuracion


def crear_aplicacion() -> FastAPI:
    configuracion = obtener_configuracion()

    aplicacion = FastAPI(
        title="API de tutoriales y comentarios",
        description=(
            "API REST para registrar tutoriales y administrar sus comentarios."
        ),
        version="1.0.0",
    )

    aplicacion.add_middleware(
        CORSMiddleware,
        allow_origins=configuracion.origenes_permitidos,
        allow_credentials=True,
        allow_methods=[
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "OPTIONS",
        ],
        allow_headers=["*"],
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