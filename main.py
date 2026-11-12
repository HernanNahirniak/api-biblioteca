from fastapi import FastAPI, HTTPException
from schema import LibroEntrada, LibroSalida

app = FastAPI()

libros_db = []
proximo_id=1

@app.get("/")
def inicio():
    return {"mensaje": "API de la biblioteca"}

@app.get("/libros", response_model=list[LibroSalida])
def listar_libros():
    return libros_db

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