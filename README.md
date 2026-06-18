# Aplicación de tutoriales y comentarios

Aplicación web desarrollada como prueba técnica para gestionar tutoriales de
aprendizaje virtual y los comentarios realizados por los estudiantes.

El proyecto está separado en una API REST construida con FastAPI y una interfaz
web desarrollada con Angular. La información se almacena en PostgreSQL.

## Funcionalidades

- Registrar tutoriales con título, descripción y fecha de publicación.
- Listar los tutoriales registrados.
- Consultar un tutorial por su identificador.
- Registrar comentarios asociados a un tutorial.
- Listar los comentarios de un tutorial.
- Reemplazar el contenido de un comentario mediante `PUT`.
- Eliminar comentarios.
- Consultar y ejecutar los endpoints desde Swagger.

## Tecnologías y versiones

### Backend

| Tecnología | Versión | Uso |
|---|---:|---|
| Python | 3.13.5 | Lenguaje del servidor |
| FastAPI | 0.137.2 | Framework para construir la API REST |
| Uvicorn | 0.49.0 | Servidor ASGI |
| SQLAlchemy | 2.0.51 | ORM y acceso a PostgreSQL |
| Psycopg | 3.3.4 | Controlador de PostgreSQL |
| Pydantic Settings | 2.14.1 | Variables de entorno |
| Alembic | 1.18.4 | Migraciones de base de datos |
| Ruff | 0.15.17 | Revisión estática del código |

### Base de datos

| Tecnología | Versión | Uso |
|---|---:|---|
| PostgreSQL | 18.4 | Persistencia relacional |

### Frontend

| Tecnología | Versión | Uso |
|---|---:|---|
| Node.js | 24.16.0 LTS | Entorno de ejecución del frontend |
| npm | 11.13.0 | Administración de dependencias |
| Angular | 22.0.x | Framework de la interfaz web |
| Angular CLI | 22.0.3 | Construcción y ejecución de Angular |
| TypeScript | 6.0.x | Lenguaje del frontend |
| RxJS | 7.8.x | Manejo de solicitudes asíncronas |

## Arquitectura

```mermaid
flowchart LR
    A["Angular"] -->|"HTTP / JSON"| B["Rutas FastAPI"]
    B --> C["Servicios"]
    C --> D["Repositorios"]
    D --> E["Modelos SQLAlchemy"]
    E --> F["PostgreSQL"]
```

El backend separa las siguientes responsabilidades:

- `api/v1/rutas`: endpoints y respuestas HTTP.
- `esquema`: validación de entrada y serialización con Pydantic.
- `servicio`: reglas del negocio y manejo de transacciones.
- `repositorio`: consultas y operaciones de persistencia.
- `modelo`: representación de las tablas con SQLAlchemy.
- `base_datos`: motor, sesiones y dependencias de conexión.
- `nucleo`: configuración general y variables de entorno.

## Estructura del repositorio

```text
comentarios_tutorial_app/
├── servidor/
│   ├── aplicacion/
│   │   ├── api/v1/rutas/
│   │   ├── base_datos/
│   │   ├── esquema/
│   │   ├── modelo/
│   │   ├── nucleo/
│   │   ├── repositorio/
│   │   ├── servicio/
│   │   └── main.py
│   ├── migraciones/
│   ├── alembic.ini
│   ├── dependencias.txt
│   └── dependencias-desarrollo.txt
├── interfaz/
│   ├── src/app/
│   │   ├── modelos/
│   │   ├── servicios/
│   │   ├── app.ts
│   │   ├── app.html
│   │   └── app.scss
│   ├── angular.json
│   └── package.json
├── documentacion/
├── .env.example
└── README.md
```

## Requisitos previos

Para ejecutar el proyecto en Windows se necesita:

1. Git.
2. Python 3.13 o compatible.
3. PostgreSQL 18 o compatible.
4. Node.js 24 LTS o una versión compatible con Angular 22.
5. PowerShell.

Verificar las instalaciones:

```powershell
git --version
python --version
node --version
npm.cmd --version
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" --version
```

## Instalación y ejecución

Los siguientes comandos están escritos para PowerShell.

### 1. Clonar el repositorio

```powershell
git clone https://github.com/brayanbustos12/comentarios_tutorial_app.git
cd comentarios_tutorial_app
```

### 2. Crear el usuario y la base de datos

Abrir PostgreSQL con el usuario administrador:

```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" `
    -U postgres `
    -h 127.0.0.1 `
    -p 5432 `
    -d postgres
```

PostgreSQL solicitará la contraseña definida durante su instalación.

Ejecutar dentro de `psql`:

```sql
CREATE USER tutoriales_usuario
WITH LOGIN PASSWORD 'TU_CLAVE_LOCAL';

CREATE DATABASE tutoriales_comentarios
WITH
    OWNER = postgres
    ENCODING = 'UTF8';

GRANT ALL PRIVILEGES
ON DATABASE tutoriales_comentarios
TO postgres;
```

Salir de PostgreSQL:

```sql
\q
```

Comprobar la conexión:

```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" `
    -U postgres `
    -h 127.0.0.1 `
    -p 5432 `
    -d tutoriales_comentarios `
    -W
```

### 3. Crear las variables de entorno

Desde la raíz del repositorio:

```powershell
Copy-Item .env.example .env
```

Editar `.env` y reemplazar `CAMBIAR_CLAVE` por la contraseña creada en
PostgreSQL:

```env
BASE_DATOS_URL=postgresql+psycopg://tutoriales_usuario:TU_CLAVE_LOCAL@127.0.0.1:5432/tutoriales_comentarios
ORIGENES_PERMITIDOS=["http://localhost:4200","http://127.0.0.1:4200"]
```

El archivo `.env` contiene información privada y está excluido mediante
`.gitignore`.

### 4. Preparar el backend

```powershell
cd servidor
python -m venv .venv
```

Si PowerShell bloquea la activación del entorno virtual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Activar el entorno e instalar las dependencias:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r dependencias-desarrollo.txt
```

### 5. Crear las tablas mediante Alembic

Desde `servidor`, con el entorno virtual activo:

```powershell
python -m alembic upgrade head
```

Comprobar la migración aplicada:

```powershell
python -m alembic current
```

La base debe contener las tablas:

```text
alembic_version
tutoriales
comentarios
```

### 6. Ejecutar el backend

```powershell
python -m uvicorn aplicacion.main:aplicacion --reload
```

El backend queda disponible en:

- API: `http://127.0.0.1:8000`.
- Swagger: `http://127.0.0.1:8000/docs`.
- OpenAPI: `http://127.0.0.1:8000/openapi.json`.

La terminal del backend debe permanecer abierta.

### 7. Preparar el frontend

Abrir una segunda terminal en la raíz del repositorio:

```powershell
cd interfaz
npm install
```

El archivo `package-lock.json` garantiza que se instalen las versiones
compatibles utilizadas durante el desarrollo.

### 8. Ejecutar el frontend

```powershell
npm start
```

La interfaz queda disponible en:

```text
http://localhost:4200
```

La terminal del frontend también debe permanecer abierta.

## Orden recomendado de ejecución

1. Comprobar que PostgreSQL esté ejecutándose.
2. Iniciar FastAPI desde `servidor`.
3. Iniciar Angular desde `interfaz`.
4. Abrir `http://localhost:4200`.

Comprobar el servicio PostgreSQL:

```powershell
Get-Service -Name "postgresql*"
```

## Endpoints principales

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/v1/salud` | Consultar el estado de la API |
| `POST` | `/api/v1/tutoriales` | Registrar un tutorial |
| `GET` | `/api/v1/tutoriales` | Listar tutoriales |
| `GET` | `/api/v1/tutoriales/{tutorial_id}` | Consultar un tutorial |
| `POST` | `/api/v1/tutoriales/{tutorial_id}/comentarios` | Registrar un comentario |
| `GET` | `/api/v1/tutoriales/{tutorial_id}/comentarios` | Listar comentarios |
| `PUT` | `/api/v1/comentarios/{comentario_id}` | Reemplazar un comentario |
| `DELETE` | `/api/v1/comentarios/{comentario_id}` | Eliminar un comentario |

## Revisión del backend

Para ejecutar Ruff:

```powershell
cd servidor
.\.venv\Scripts\Activate.ps1
python -m ruff check aplicacion migraciones
```

## Errores frecuentes

### `npx`, `npm` o `node` no son reconocidos

Cerrar y abrir nuevamente PowerShell después de instalar Node.js. Para la
terminal actual también se puede ejecutar:

```powershell
$env:Path = "C:\Program Files\nodejs;$env:Path"
```

### La autenticación de PostgreSQL falla

La contraseña del archivo `.env` debe coincidir con la del usuario
`postgres`. 


### Angular no puede consumir la API

Comprobar que:

1. FastAPI esté ejecutándose en `http://127.0.0.1:8000`.
2. Angular esté ejecutándose en `http://localhost:4200`.
3. `.env` incluya el origen de Angular en `ORIGENES_PERMITIDOS`.

## Documentación adicional

- [Requerimientos](documentacion/requisitos.md).
- [Hoja de ruta](documentacion/hoja-ruta.md).
- [Configuración de la base de datos](documentacion/configuracion-base-datos.md).
- [Documentación de la API REST](documentacion/api-rest.md).
