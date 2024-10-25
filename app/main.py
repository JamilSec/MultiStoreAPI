from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
from .utils.manejador_archivos import guardar_archivo_localmente
from .utils.servicio_drive import servicio_drive
from .utils.servicio_s3 import servicio_s3
from .models.respuestas import RespuestaArchivoSubido, RespuestaMultiplesArchivos

app = FastAPI(
    title="API de Subida de Archivos",
    description="API para subir archivos a almacenamiento local, Google Drive o AWS S3",
    version="2.0.0"
)

# Tipos MIME permitidos
TIPOS_PERMITIDOS = [
    "image/jpeg", "image/png", "image/gif",
    "application/pdf", "application/xml", "text/xml",
    "application/zip", "application/x-rar-compressed",
    "application/x-sqlite3", "application/sql",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # .xlsx
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # .docx
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",  # .pptx
    "application/vnd.ms-excel", "application/msword", "application/vnd.ms-powerpoint",
    "text/csv", "application/json", "text/plain"
]

@app.post("/subir_archivos/", response_model=RespuestaMultiplesArchivos)
async def subir_archivos(
    archivos: List[UploadFile] = File(...),
    tipo_almacenamiento: str = "local"
):
    """
    Endpoint para subir múltiples archivos y almacenarlos localmente, en Google Drive o en AWS S3.
    """
    respuestas = []
    for archivo in archivos:
        # Mover el puntero del archivo subyacente para obtener su tamaño sin consumir el archivo
        archivo.file.seek(0, 2)  # Mueve el puntero al final del archivo
        tamaño_archivo = archivo.file.tell()  # Obtener la posición actual del puntero (tamaño del archivo)
        
        # Volver el puntero al inicio para que se lea correctamente
        archivo.file.seek(0)

        # Validar tipo de archivo y tamaño
        if archivo.content_type not in TIPOS_PERMITIDOS:
            raise HTTPException(status_code=400, detail=f"Tipo de archivo no compatible: {archivo.content_type}")
        
        if tamaño_archivo > 10 * 1024 * 1024:  # Limitar a 10MB
            raise HTTPException(status_code=400, detail=f"Archivo demasiado grande: {archivo.filename}")

        try:
            # Guardar el archivo en el almacenamiento seleccionado
            if tipo_almacenamiento == "local":
                ruta_archivo = await guardar_archivo_localmente(archivo)
            elif tipo_almacenamiento == "drive" and servicio_drive.servicio:
                ruta_archivo = servicio_drive.subir_archivo(archivo)
            elif tipo_almacenamiento == "s3" and servicio_s3.cliente_s3:
                ruta_archivo = servicio_s3.subir_archivo(archivo)
            else:
                raise HTTPException(status_code=400, detail="Tipo de almacenamiento inválido o no configurado")
            
            respuestas.append(RespuestaArchivoSubido(nombre_archivo=archivo.filename, ruta=ruta_archivo))

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error subiendo {archivo.filename}: {str(e)}")

    return RespuestaMultiplesArchivos(archivos=respuestas)

# uvicorn app.main:app --reload