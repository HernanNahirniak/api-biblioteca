# API de la Biblioteca

API REST hecha con FastAPI para gestionar los libros de una biblioteca: crear, listar, actualizar, borrar, filtrar, paginar y buscar. Los datos se guardan en un archivo JSON y sobreviven al reinicio del servidor.

Proyecto del Módulo 3 · Bootcamp Python Backend · Silicon Misiones.

## Requisitos

- Python 3.13 (funciona también con versiones recientes de Python 3)
- Git

## Instalación

1. Clonar el repositorio y entrar a la carpeta:

   git clone https://github.com/HernanNahirniak/api-biblioteca
   cd api-biblioteca

2. Crear y activar el entorno virtual (Windows):

   python -m venv .venv
   .venv\Scripts\activate

3. Instalar las dependencias:

   pip install -r requirements.txt

## Cómo correr la API

fastapi dev main.py

También se puede levantar con uvicorn:

uvicorn main:app --reload

La API queda disponible en http://127.0.0.1:8000. La documentación interactiva está en http://127.0.0.1:8000/docs.

## Endpoints

| Método | Ruta                     | Descripción                                                                    |
| ------ | ------------------------ | ------------------------------------------------------------------------------ |
| GET    | /                        | Mensaje de bienvenida                                                          |
| GET    | /libros                  | Lista libros. Filtros opcionales: autor, disponible. Paginación: desde, limite |
| GET    | /libros/buscar?texto=... | Busca el texto en título o autor (sin distinguir mayúsculas)                   |
| POST   | /libros                  | Crea un libro (201). Devuelve 409 si el título y el autor ya existen           |
| GET    | /libros/{id}             | Devuelve un libro (404 si no existe)                                           |
| PUT    | /libros/{id}             | Reemplaza todos los campos del libro                                           |
| PATCH  | /libros/{id}             | Actualiza solo los campos enviados                                             |
| DELETE | /libros/{id}             | Borra el libro (204 sin cuerpo)                                                |

## El recurso libro

| Campo      | Tipo     | Reglas                                                |
| ---------- | -------- | ----------------------------------------------------- |
| id         | entero   | Lo asigna el servidor. Empieza en 1 y no se reutiliza |
| titulo     | texto    | De 3 a 100 caracteres                                 |
| autor      | texto    | De 3 a 60 caracteres                                  |
| anio       | entero   | Entre 1000 y 2100                                     |
| disponible | booleano | Por defecto true                                      |

Ejemplo de pedido POST /libros:

json
{
"titulo": "Rayuela",
"autor": "Julio Cortázar",
"anio": 1963
}

## Persistencia

Los libros se guardan en datos/libros.json después de cada cambio (crear, reemplazar, actualizar y borrar) y se cargan al iniciar la API. Si el archivo no existe, está vacío o está dañado, la API arranca con la lista vacía. Tras reiniciar, el siguiente id es el mayor id guardado más 1.

## Estructura del proyecto

api-biblioteca/
├─ main.py # app FastAPI y endpoints
├─ schemas.py # modelos de Pydantic
├─ requirements.txt
├─ README.md
├─ .gitignore
└─ datos/ # acá se crea libros.json
