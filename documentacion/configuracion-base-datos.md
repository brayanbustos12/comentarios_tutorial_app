# Configuración de la base de datos

## Objetivo

Configurar PostgreSQL como sistema de persistencia para la API REST de
tutoriales y comentarios. La aplicación utiliza SQLAlchemy para representar las
tablas mediante clases de Python, Psycopg para conectarse con PostgreSQL y
Alembic para controlar los cambios del esquema.

## Tecnologías utilizadas

- PostgreSQL 18.
- SQLAlchemy 2.0.51.
- Psycopg 3.3.4.
- Alembic 1.18.4.
- Pydantic Settings 2.14.1.

## Arquitectura

```mermaid
flowchart LR
    A["API FastAPI"] --> B["Servicios"]
    B --> C["Repositorios"]
    C --> D["Modelos SQLAlchemy"]
    D --> E["Sesión SQLAlchemy"]
    E --> F["PostgreSQL"]
```

Las responsabilidades se distribuyen de la siguiente manera:

- `aplicacion/modelo`: estructuras de las tablas y sus relaciones.
- `aplicacion/base_datos`: motor, fábrica de sesiones y dependencia de sesión.
- `aplicacion/nucleo/configuracion.py`: lectura de variables de entorno.
- `migraciones`: historial de cambios del esquema administrado por Alembic.
- `aplicacion/repositorio`: operaciones de consulta y persistencia.

## Requisitos previos

1. Tener PostgreSQL instalado y ejecutándose en el puerto `5432`.
2. Tener Python 3.13 y el entorno virtual del servidor.
3. Ejecutar los comandos de Python y Alembic desde la carpeta `servidor`.

Para comprobar PostgreSQL en Windows:

```powershell
Get-Service -Name "postgresql*"
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" --version
```

## Creación del usuario y la base de datos

Abrir PostgreSQL con el usuario administrador:

```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" `
    -U postgres `
    -h 127.0.0.1 `
    -p 5432 `
    -d postgres
```

Ejecutar las siguientes instrucciones dentro de `psql`:

```sql
CREATE USER tutoriales_usuario
WITH LOGIN PASSWORD 'TU_CLAVE_LOCAL';

CREATE DATABASE tutoriales_comentarios
WITH
    OWNER = tutoriales_usuario
    ENCODING = 'UTF8';

GRANT ALL PRIVILEGES
ON DATABASE tutoriales_comentarios
TO tutoriales_usuario;
```

Salir de PostgreSQL:

```sql
\q
```

## Variables de entorno

El archivo `.env.example` documenta la variable requerida sin publicar una
contraseña real:

```env
BASE_DATOS_URL=postgresql+psycopg://tutoriales_usuario:CAMBIAR_CLAVE@127.0.0.1:5432/tutoriales_comentarios
```

Cada desarrollador debe crear un archivo `.env` en la raíz del repositorio:

```powershell
Copy-Item .env.example .env
```

Después debe reemplazar `CAMBIAR_CLAVE` por su contraseña local. El archivo
`.env` está excluido de Git y no debe subirse al repositorio.

## Dependencias del servidor

Las dependencias de persistencia están declaradas en
`servidor/dependencias.txt`:

```text
SQLAlchemy==2.0.51
psycopg[binary]==3.3.4
pydantic-settings==2.14.1
alembic==1.18.4
```

Para instalarlas:

```powershell
cd servidor
.\.venv\Scripts\Activate.ps1
python -m pip install -r dependencias-desarrollo.txt
```

## Modelo de datos

La aplicación contiene dos tablas relacionadas:

```mermaid
erDiagram
    TUTORIALES ||--o{ COMENTARIOS : contiene

    TUTORIALES {
        bigint id PK
        varchar titulo
        text descripcion
        timestamptz fecha_publicacion
    }

    COMENTARIOS {
        bigint id PK
        text contenido
        bigint tutorial_id FK
        timestamptz fecha_creacion
        timestamptz fecha_actualizacion
    }
```

La llave foránea `comentarios.tutorial_id` utiliza eliminación en cascada. Al
eliminar un tutorial, PostgreSQL elimina también sus comentarios asociados.

## Migraciones con Alembic

Alembic se inicializó en la carpeta `servidor/migraciones`. La configuración de
`migraciones/env.py` obtiene la conexión desde `.env` y carga los modelos de
`aplicacion/modelo`.

Para generar una migración después de cambiar los modelos:

```powershell
cd servidor
python -m alembic revision --autogenerate -m "descripcion del cambio"
```

Para aplicar las migraciones pendientes:

```powershell
python -m alembic upgrade head
```

Para consultar la migración aplicada:

```powershell
python -m alembic current
```

La primera migración del proyecto crea las tablas `tutoriales` y `comentarios`.

## Verificación de la conexión

Desde la carpeta `servidor`:

```powershell
python -c "from aplicacion.base_datos.sesion import motor; conexion = motor.connect(); print('Conexión correcta'); conexion.close()"
```

Para consultar las tablas directamente en PostgreSQL:

```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" `
    -U tutoriales_usuario `
    -h 127.0.0.1 `
    -p 5432 `
    -d tutoriales_comentarios `
    -W `
    -c "\dt"
```

El resultado debe incluir:

```text
alembic_version
tutoriales
comentarios
```

## Errores frecuentes

### La autenticación falló

```text
FATAL: la autenticación password falló para el usuario tutoriales_usuario
```

La contraseña de `.env` no coincide con la registrada en PostgreSQL. Se puede
restablecer desde una sesión administrativa:

```sql
ALTER USER tutoriales_usuario
WITH PASSWORD 'TU_NUEVA_CLAVE_LOCAL';
```

Después debe actualizarse el archivo `.env` con la misma contraseña.

### No se encuentra el módulo `aplicacion`

Los comandos de Uvicorn y Alembic deben ejecutarse dentro de `servidor`:

```powershell
cd C:\Users\SpeedLogic\comentarios_tutorial_app\servidor
python -m alembic current
```

### PostgreSQL no está disponible

Comprobar el servicio:

```powershell
Get-Service -Name "postgresql*"
```

Si está detenido, iniciar el servicio desde una terminal con permisos de
administrador:

```powershell
Start-Service postgresql-x64-18
```

## Consideraciones de seguridad

- No publicar `.env` ni contraseñas reales.
- Utilizar un usuario exclusivo para la aplicación.
- No conectar la API con el usuario administrador `postgres`.
- Mantener `.env.example` únicamente con valores de referencia.
- Gestionar los cambios de tablas mediante Alembic, no manualmente.

## Resultado

Al finalizar esta configuración, la API puede abrir sesiones SQLAlchemy,
consultar PostgreSQL y administrar las tablas mediante migraciones reproducibles.
