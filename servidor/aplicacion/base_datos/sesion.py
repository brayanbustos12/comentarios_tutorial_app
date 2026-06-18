from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from aplicacion.nucleo.configuracion import obtener_configuracion

configuracion = obtener_configuracion()

motor = create_engine(
    configuracion.base_datos_url,
    pool_pre_ping=True,
)

fabrica_sesiones = sessionmaker(
    bind=motor,
    class_=Session,
    autoflush=False,
    expire_on_commit=False,
)