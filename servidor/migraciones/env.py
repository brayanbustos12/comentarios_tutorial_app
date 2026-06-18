from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

import aplicacion.modelo  # noqa: F401
from aplicacion.base_datos.base import Base
from aplicacion.nucleo.configuracion import obtener_configuracion

configuracion_alembic = context.config

if configuracion_alembic.config_file_name is not None:
    fileConfig(configuracion_alembic.config_file_name)

configuracion = obtener_configuracion()

configuracion_alembic.set_main_option(
    "sqlalchemy.url",
    configuracion.base_datos_url.replace("%", "%%"),
)

target_metadata = Base.metadata


def ejecutar_migraciones_sin_conexion() -> None:
    url = configuracion_alembic.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def ejecutar_migraciones_con_conexion() -> None:
    configuracion_motor = configuracion_alembic.get_section(
        configuracion_alembic.config_ini_section,
        {},
    )

    motor = engine_from_config(
        configuracion_motor,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with motor.connect() as conexion:
        context.configure(
            connection=conexion,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    ejecutar_migraciones_sin_conexion()
else:
    ejecutar_migraciones_con_conexion()