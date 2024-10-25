from pathlib import Path
from fastapi import UploadFile
import shutil
from ..config import configuracion

async def guardar_archivo_localmente(archivo: UploadFile) -> str:
    """
    Guarda el archivo en almacenamiento local y devuelve la ruta.
    """
    ruta_archivo = configuracion.RUTA_ALMACENAMIENTO_LOCAL / archivo.filename
    with open(ruta_archivo, "wb") as buffer:
        shutil.copyfileobj(archivo.file, buffer)
    return str(ruta_archivo)