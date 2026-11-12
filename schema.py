from pydantic import BaseModel, Field

class LibroEntrada(BaseModel):
    
    titulo: str = Field(min_length=3, max_length=100)
    autor: str = Field(min_length=3, max_length=60)
    anio: int = Field(ge= 1000, le= 2100)
    disponible: bool = True    
    

class LibroSalida(LibroEntrada):
    id: int