from fastapi import APIRouter

enrutador = APIRouter(tags=["Estado"])


@enrutador.get(
    "/salud",
    summary="Consultar el estado de la API",
    response_model=dict[str, str],
)
def consultar_salud() -> dict[str, str]:
    return {
        "estado": "correcto",
        "mensaje": "La API está funcionando",
    }