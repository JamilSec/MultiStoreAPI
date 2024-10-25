import os
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno desde .env
load_dotenv()

class Configuracion:
    # Almacenamiento local
    RUTA_ALMACENAMIENTO_LOCAL = Path("./archivos_subidos")
    RUTA_ALMACENAMIENTO_LOCAL.mkdir(parents=True, exist_ok=True)
    
    # Configuración opcional de Google Drive
    GOOGLE_DRIVE_ID_CARPETA = os.getenv("GOOGLE_DRIVE_ID_CARPETA", None)
    ARCHIVO_CREDENCIALES_SERVICIO = os.getenv("ARCHIVO_CREDENCIALES_SERVICIO", None)
    ALCANCES = ["https://www.googleapis.com/auth/drive"]

    # Configuración opcional de AWS S3
    AWS_ID_CLAVE_ACCESO = os.getenv("AWS_ID_CLAVE_ACCESO", None)
    AWS_CLAVE_ACCESO_SECRETA = os.getenv("AWS_CLAVE_ACCESO_SECRETA", None)
    AWS_NOMBRE_BUCKET = os.getenv("AWS_NOMBRE_BUCKET", None)

configuracion = Configuracion()