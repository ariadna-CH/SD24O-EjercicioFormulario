import os
import uuid
from fastapi import FastAPI, UploadFile, File, Form
from pathlib import Path

#Creación del servidor
app = FastAPI()

@app.post("/usuarios")
async def registro_usuario(nombre: str = Form(...),direccion: str = Form(...),foto: UploadFile = File(...),vip: bool = Form(False)):
    print(f"Nombre: {nombre}")
    print(f"Dirección: {direccion}")
    print(f"Es VIP: {vip}")

    #Es el directorio base del usuario
    home_usuario = Path.home()
    #Se define las carpetas para VIP y no VIP
    usuario_vip = home_usuario / "fotos-usuarios-vip"
    usuario_no_vip = home_usuario / "fotos-usuarios"

    #Crea las carpetas si no existen
    #usuario_vip.mkdir(parents=True, exist_ok=True)
    #usuario_no_vip.mkdir(parents=True, exist_ok=True)

    #Genera nombre único para el archivo
    nombre_archivo = f"{uuid.uuid4()}{Path(foto.filename).suffix}"
    #Selecciona la ruta de la imagen si es VIP o no
    ruta_carpeta_fotos = usuario_vip if vip else usuario_no_vip
    ruta_imagen = ruta_carpeta_fotos / nombre_archivo

    #Guarda el archivo fotos
    print(f"Guardando la foto en: {ruta_imagen}")
    contenido = await foto.read()  # Leer el contenido del archivo
    with ruta_imagen.open("wb") as imagen:
        imagen.write(contenido)

    respuesta = {
        "Nombre": nombre,
        "Dirección": direccion,
        "VIP": vip,
        "Ruta": str(ruta_imagen),
    }
    return respuesta
