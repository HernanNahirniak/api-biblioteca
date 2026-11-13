from fastapi import FastAPI, HTTPException
from schema import LibroEntrada, LibroSalida

app = FastAPI()

libros_db = []
proximo_id=1

@app.get("/")
def inicio():
    return {"mensaje": "API de la biblioteca"}

@app.get("/libros", response_model=list[LibroSalida])
def listar_libros(autor: str | None = None, desde: int = 0, limite: int = 100, disponible: bool | None = None):
    resultado = libros_db
    if autor is not None :
        resultado = [libro for libro in resultado if libro["autor"].lower() == autor.lower()]
    if disponible is not None:
        resultado = [libro for libro in resultado if libro["disponible"] == disponible]
    resultado = resultado[desde: desde + limite]
    return resultado
    
    
@app.post("/libros", response_model=LibroSalida, status_code=201)
def crear_libro(libro: LibroEntrada) :
    global proximo_id
    
    nuevo = {"id" : proximo_id, **libro.model_dump()}
    libros_db.append(nuevo)
    proximo_id +=1
    
    return nuevo

@app.get("/libros/{libro_id}", response_model= LibroSalida)
def obtener_libro(libro_id: int) :
    for libro in libros_db:
        if libro["id"] == libro_id:
            return libro
    raise HTTPException(status_code=404, detail= "Libro no encontrado")

@app.delete("/libros/{libro_id}", status_code=204)
def borrar_libro(libro_id: int):
    for libro in libros_db:
        if libro["id"] == libro_id:
            libros_db.remove(libro)
            return
    raise HTTPException(status_code=404, detail="Libro no encontrado") 

@app.put("libros/{libro_id}", response_model= LibroSalida)
def reemplazar_libro(libro_id: int, libro: LibroEntrada):
    for posicion, existente in enumerate(libros_db):
        if existente["id"] == libro_id :
            actualizado = {"id": libros_db, **libro.model.dump()}
            libros_db[posicion] = actualizado
            return actualizado
    raise HTTPException(status_code=404, detail="Libro no encontrado")