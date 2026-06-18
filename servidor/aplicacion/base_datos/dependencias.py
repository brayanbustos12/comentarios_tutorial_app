from collections.abc import Generator

from sqlalchemy.orm import Session

from aplicacion.base_datos.sesion import fabrica_sesiones


def obtener_sesion() -> Generator[Session, None, None]:
    sesion = fabrica_sesiones()

    try:
        yield sesion
    finally:
        sesion.close()