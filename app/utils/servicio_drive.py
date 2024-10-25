from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
from fastapi import UploadFile
import shutil
import os
from ..config import configuracion

class ServicioGoogleDrive:
    def __init__(self):
        if configuracion.ARCHIVO_CREDENCIALES_SERVICIO and os.path.exists(configuracion.ARCHIVO_CREDENCIALES_SERVICIO):
            self.credenciales = service_account.Credentials.from_service_account_file(
                configuracion.ARCHIVO_CREDENCIALES_SERVICIO, scopes=configuracion.ALCANCES
            )
            self.servicio = build("drive", "v3", credentials=self.credenciales)
        else:
            self.servicio = None
            print("Google Drive no está configurado. Solo el almacenamiento local está disponible.")

    def subir_archivo(self, archivo: UploadFile) -> str:
        if not self.servicio:
            raise Exception("Google Drive no está configurado.")
        
        ruta_temporal = configuracion.RUTA_ALMACENAMIENTO_LOCAL / archivo.filename
        with open(ruta_temporal, "wb") as buffer:
            shutil.copyfileobj(archivo.file, buffer)

        metadata_archivo = {
            "name": archivo.filename,
            "parents": [configuracion.GOOGLE_DRIVE_ID_CARPETA]
        }
        media = MediaFileUpload(ruta_temporal, mimetype=archivo.content_type)
        archivo_subido = self.servicio.files().create(
            body=metadata_archivo, media_body=media, fields="id"
        ).execute()

        os.remove(ruta_temporal)

        id_archivo = archivo_subido.get("id")
        return f"https://drive.google.com/uc?id={id_archivo}"

# Crear una instancia del servicio de Google Drive
servicio_drive = ServicioGoogleDrive()