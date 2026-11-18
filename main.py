from fastapi import FastAPI, HTTPException
from schema import LibroEntrada, LibroSalida, LibroParcial
from pathlib import Path 
import json
import sys 


sys.stdout.reconfigure(encoding="utf-8")

CARPETA= Path(__file__).parent/ "datos"
ARCHIVO= CARPETA/"libros.json"


    
app = FastAPI()

def guardar():
    CARPETA.mkdir(exist_ok=True)
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(libros_db, f, ensure_ascii=False, indent=2)

def cargar():
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            datos = json.load(f)
        if isinstance(datos, list) and all(isinstance(libro, dict) and isinstance(libro.get("id"), int) for libro in datos ):
            return datos
    except(OSError, ValueError):
        pass
    return []
    

libros_db = cargar()
proximo_id = max((libro["id"] for libro in libros_db), default=0) + 1

@app.get("/", summary="Inicio de la API")
def inicio():
    return {"mensaje": "API de la biblioteca"}

@app.get("/libros", response_model=list[LibroSalida], summary="Obtener libros")
def listar_libros(autor: str | None = None, desde: int = 0, limite: int = 100, disponible: bool | None = None):
    """Devuelve la lista de los libros con un status 200,
        si no hay retorna [](lista vacia). 
        Filtado: filta los nombre del autor cuyo nombre que coincidan con el texto buscado
        Páginacion: muestran los libro desde: N hasta el limite: X, sin tener en cuenta N y hasta máximo X.
        """
        
    resultado = libros_db
    if autor is not None :
        resultado = [libro for libro in resultado if libro["autor"].lower() == autor.lower()]
    if disponible is not None:
        resultado = [libro for libro in resultado if libro["disponible"] == disponible]
    resultado = resultado[desde: desde + limite]
    return resultado
    

@app.get("/libros/buscar", response_model= list[LibroSalida])
def buscar_libros(texto: str):
    """Retorna la lista de libros cuyo título o autor contenga el texto, status 422 si falta texto 
        y [] si no hay coincidencias."""
    texto = texto.lower()
    return[libro for libro in libros_db if texto in libro["titulo"].lower() 
           or texto in libro["autor"].lower()]


@app.get("/libros/{libro_id}", response_model= LibroSalida, summary="Obtener un libro por ID")
def obtener_libro(libro_id: int) :
    """Busca el libro segun su ID, status 422 si el ID no es del tipo numerico 
        y un 404 si no se encuentra el libro con ese ID."""
    for libro in libros_db:
        if libro["id"] == libro_id:
            return libro
    raise HTTPException(status_code=404, detail= "Libro no encontrado")


@app.post("/libros", response_model= LibroSalida, status_code=201, summary="Agregar un libro nuevo")
def crear_libro(libro: LibroEntrada) :
    """Agrega un libro nuevo, con los nuevos datos 'titulo', 'autor', 'anio', 'disponible'con un status 201,
            status 409 si el libro ya existe con esos datos y 422 si los datos ingresados
            no coinciden con las reglas de negocio."""
    
    global proximo_id
    
    for existente in libros_db:
        if(existente["titulo"].lower() == libro.titulo.lower() and existente["autor"].lower() == libro.autor.lower()):
            raise HTTPException(status_code=409, detail="El libro ya existe")
        
    nuevo = {"id" : proximo_id, **libro.model_dump()}
    libros_db.append(nuevo)
    proximo_id +=1
    guardar()
    return nuevo



@app.delete("/libros/{libro_id}", status_code=204, summary="Eliminar un libro")
def borrar_libro(libro_id: int):
    """Eliminamos un libro con todos sus datos existentes, sin devolucion de un body,
        status 404 si el ID del libro no coincide con el ID solicitado."""
    for libro in libros_db:
        if libro["id"] == libro_id:
            libros_db.remove(libro)
            guardar()
            return
    raise HTTPException(status_code=404, detail="Libro no encontrado") 


@app.put("/libros/{libro_id}", response_model= LibroSalida, summary="Modificar un libro")
def reemplazar_libro(libro_id: int, libro: LibroEntrada) :
    """Modificacion de todo el contenido de un libro status 200 si sale todo bien,
         404 si el ID del libro no existe, 422 si los datos son inválidos."""
    for posicion, existente in enumerate(libros_db):
        if existente["id"] == libro_id :
            actualizado = {"id": libro_id, **libro.model_dump() }
            libros_db[posicion] = actualizado
            guardar()
            return actualizado
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.patch("/libros/{libro_id}", response_model= LibroSalida, summary="Modificacion parcial de un libro")
def actualizar_libro(libro_id: int, cambios: LibroParcial):
    for libro in libros_db:
        if libro["id"] == libro_id:
            libro.update(cambios.model_dump(exclude_unset=True))
            guardar()
            return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")