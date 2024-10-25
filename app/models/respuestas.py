from pydantic import BaseModel
from typing import List


class RespuestaArchivoSubido(BaseModel):
    nombre_archivo: str
    ruta: str


class RespuestaMultiplesArchivos(BaseModel):
    archivos: List[RespuestaArchivoSubido]