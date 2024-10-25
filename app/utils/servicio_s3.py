import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile
from ..config import configuracion

class ServicioS3:
    def __init__(self):
        if (configuracion.AWS_ID_CLAVE_ACCESO and 
            configuracion.AWS_CLAVE_ACCESO_SECRETA and 
            configuracion.AWS_NOMBRE_BUCKET):
            
            self.cliente_s3 = boto3.client(
                's3',
                aws_access_key_id=configuracion.AWS_ID_CLAVE_ACCESO,
                aws_secret_access_key=configuracion.AWS_CLAVE_ACCESO_SECRETA
            )
        else:
            self.cliente_s3 = None
            print("AWS S3 no está configurado. Solo el almacenamiento local está disponible.")

    def subir_archivo(self, archivo: UploadFile) -> str:
        if not self.cliente_s3:
            raise Exception("AWS S3 no está configurado.")

        clave_archivo = archivo.filename
        self.cliente_s3.upload_fileobj(archivo.file, configuracion.AWS_NOMBRE_BUCKET, clave_archivo)
        return f"https://{configuracion.AWS_NOMBRE_BUCKET}.s3.amazonaws.com/{clave_archivo}"

# Crear una instancia del servicio de AWS S3
servicio_s3 = ServicioS3()