from fastapi import FastAPI
from schema import LibroEntrada, LibroSalida

app = FastAPI()

libros_db = []

@app.get("/")
def inicio():
    return {"mensaje": "API de la biblioteca"}

@app.get("/libros", response_model=list[LibroSalida])
def listar_libros():
    return libros_db