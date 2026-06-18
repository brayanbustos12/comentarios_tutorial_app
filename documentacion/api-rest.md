# Documentación de la API REST

## Información general

- URL local: `http://127.0.0.1:8000`.
- Prefijo de la API: `/api/v1`.
- Documentación Swagger: `http://127.0.0.1:8000/docs`.
- Formato de intercambio: JSON.

Todas las solicitudes que envían datos deben incluir:

```text
Content-Type: application/json
Accept: application/json
```

## Estado de la API

### Consultar estado

```http
GET /api/v1/salud
```

Respuesta `200 OK`:

```json
{
  "estado": "correcto",
  "mensaje": "La API está funcionando"
}
```

## Tutoriales

### Registrar un tutorial

```http
POST /api/v1/tutoriales
```

Cuerpo:

```json
{
  "titulo": "Introducción a FastAPI",
  "descripcion": "Tutorial para aprender los fundamentos de FastAPI.",
  "fecha_publicacion": "2026-06-18T10:00:00-05:00"
}
```

Respuesta: `201 Created`.

### Listar tutoriales

```http
GET /api/v1/tutoriales
```

Respuesta: `200 OK` con una lista de tutoriales.

### Consultar un tutorial

```http
GET /api/v1/tutoriales/{tutorial_id}
```

Respuestas:

- `200 OK`: tutorial encontrado.
- `404 Not Found`: el tutorial no existe.

## Comentarios

### Registrar un comentario

```http
POST /api/v1/tutoriales/{tutorial_id}/comentarios
```

Cuerpo:

```json
{
  "contenido": "El tutorial fue claro y útil."
}
```

Respuestas:

- `201 Created`: comentario registrado.
- `404 Not Found`: el tutorial no existe.
- `422 Unprocessable Content`: el cuerpo no cumple las validaciones.

### Listar los comentarios de un tutorial

```http
GET /api/v1/tutoriales/{tutorial_id}/comentarios
```

Respuestas:

- `200 OK`: lista de comentarios.
- `404 Not Found`: el tutorial no existe.

### Reemplazar un comentario

```http
PUT /api/v1/comentarios/{comentario_id}
```

Cuerpo completo del recurso editable:

```json
{
  "contenido": "Contenido actualizado del comentario."
}
```

Se utiliza `PUT` porque la operación reemplaza todos los campos editables del
comentario. Actualmente el único campo editable es `contenido`.

Respuestas:

- `200 OK`: comentario actualizado.
- `404 Not Found`: el comentario no existe.
- `422 Unprocessable Content`: el contenido es inválido.

### Eliminar un comentario

```http
DELETE /api/v1/comentarios/{comentario_id}
```

Respuestas:

- `204 No Content`: comentario eliminado.
- `404 Not Found`: el comentario no existe.

## Resumen de endpoints

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

## Uso desde Postman

1. Seleccionar el método correspondiente.
2. Usar la URL exacta, sin agregar una barra final.
3. Seleccionar `Body`, luego `raw` y finalmente `JSON`.
4. Agregar el cuerpo indicado para operaciones `POST` y `PUT`.
5. Comprobar el código HTTP de la respuesta.

También es posible importar automáticamente el contrato desde:

```text
http://127.0.0.1:8000/openapi.json
```

## Consumo desde Angular

La API utiliza el middleware CORS de FastAPI para aceptar solicitudes desde el
servidor local de Angular. Los orígenes permitidos durante el desarrollo son:

```text
http://localhost:4200
http://127.0.0.1:4200
```

Los métodos permitidos son `GET`, `POST`, `PUT`, `DELETE` y `OPTIONS`. Los
orígenes se configuran mediante la variable `ORIGENES_PERMITIDOS` del archivo
`.env` y se documentan sin secretos en `.env.example`.

## Códigos de respuesta

| Código | Significado |
|---|---|
| `200` | Operación ejecutada correctamente |
| `201` | Recurso creado correctamente |
| `204` | Recurso eliminado correctamente |
| `404` | Recurso no encontrado |
| `405` | Método HTTP no permitido para la ruta |
| `422` | Datos de entrada inválidos |
| `500` | Error interno del servidor |
