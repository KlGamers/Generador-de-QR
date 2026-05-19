"""
Generador de QR Codes con diseño bonito
Estilo: módulos redondeados, gradiente de color, fondo suave con estrellas decorativas
"""

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask, SolidFillColorMask
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math
import random


DATOS_URL = "direccion a sacar el qr"  
NOMBRE_ARCHIVO = "Direccion a guardar" 


COLOR_OSCURO   = (101, 33, 110)    
COLOR_CLARO    = (166, 117, 211)    
FONDO_COLOR    = (237, 220, 252)   
FONDO_TARJETA  = (247, 235, 255)    


def crear_fondo(ancho: int, alto: int) -> Image.Image:
    """Crea el fondo lavanda con círculos difusos y estrellas decorativas."""
    fondo = Image.new("RGBA", (ancho, alto), FONDO_COLOR + (255,))
    draw = ImageDraw.Draw(fondo)

    blobs = [
        (ancho * 0.85, alto * 0.75, ancho * 0.45, (100, 70, 160, 60)),
        (ancho * 0.0,  alto * 0.0,  ancho * 0.4,  (180, 150, 220, 40)),
        (ancho * 0.5,  alto * 0.9,  ancho * 0.35, (130, 100, 190, 50)),
    ]
    for bx, by, br, color in blobs:
        blob_layer = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
        bd = ImageDraw.Draw(blob_layer)
        bd.ellipse([bx - br, by - br, bx + br, by + br], fill=color)
        blob_layer = blob_layer.filter(ImageFilter.GaussianBlur(radius=br * 0.6))
        fondo = Image.alpha_composite(fondo, blob_layer)

    draw = ImageDraw.Draw(fondo)
    puntos_curva = [
        (ancho * 0.6, alto * 0.3),
        (ancho * 0.8, alto * 0.5),
        (ancho * 0.95, alto * 0.7),
        (ancho * 0.9, alto * 0.95),
    ]
    draw.line(puntos_curva, fill=(200, 80, 120, 160), width=4)

    puntos_curva2 = [
        (ancho * 0.65, alto * 0.25),
        (ancho * 0.85, alto * 0.45),
        (ancho * 1.0,  alto * 0.65),
    ]
    draw.line(puntos_curva2, fill=(200, 80, 120, 100), width=2)

    estrellas = [
        (ancho * 0.78, alto * 0.18, 18, 180),
        (ancho * 0.88, alto * 0.24, 12, 140),
        (ancho * 0.82, alto * 0.30, 8,  160),
        (ancho * 0.10, alto * 0.82, 22, 180),
        (ancho * 0.92, alto * 0.85, 26, 200),
    ]
    for sx, sy, sr, alpha in estrellas:
        dibujar_estrella(draw, sx, sy, sr, alpha)

    return fondo


def dibujar_estrella(draw: ImageDraw.Draw, cx: float, cy: float,
                     r: float, alpha: int = 200) -> None:
    """Dibuja una estrella de 4 puntas estilo sparkle."""
    color = COLOR_OSCURO + (alpha,)
    puntos = []
    for i in range(8):
        angulo = math.radians(i * 45 - 90)
        radio  = r if i % 2 == 0 else r * 0.25
        puntos.append((cx + radio * math.cos(angulo),
                       cy + radio * math.sin(angulo)))
    draw.polygon(puntos, fill=color)


def generar_qr_imagen(datos: str) -> Image.Image:
    """Genera el QR con módulos redondeados y gradiente radial."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=14,
        border=2,
    )
    qr.add_data(datos)
    qr.make(fit=True)

    img_qr = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(radius_ratio=1.0),
        color_mask=RadialGradiantColorMask(
            back_color=(255, 255, 255),
            center_color=COLOR_CLARO,
            edge_color=COLOR_OSCURO,
        ),
    ).convert("RGBA")

    return img_qr


def componer_imagen_final(datos: str, nombre_archivo: str) -> None:
    """Compone la imagen final: fondo + tarjeta + QR."""
    img_qr = generar_qr_imagen(datos)
    qr_w, qr_h = img_qr.size

    pad = 36
    tarjeta_w = qr_w + pad * 2
    tarjeta_h = qr_h + pad * 2
    tarjeta = Image.new("RGBA", (tarjeta_w, tarjeta_h), (0, 0, 0, 0))
    draw_t = ImageDraw.Draw(tarjeta)
    radio_esquina = 28
    draw_t.rounded_rectangle(
        [0, 0, tarjeta_w - 1, tarjeta_h - 1],
        radius=radio_esquina,
        fill=(255, 255, 255, 245),
    )
    tarjeta.paste(img_qr, (pad, pad), img_qr)

    margen = 60
    canvas_w = tarjeta_w + margen * 2
    canvas_h = tarjeta_h + margen * 2

    fondo = crear_fondo(canvas_w, canvas_h)
    fondo.paste(tarjeta, (margen, margen), tarjeta)

    fondo_rgb = fondo.convert("RGB")
    fondo_rgb.save(nombre_archivo, "PNG", quality=95)
    print(f"✅  QR guardado en: {nombre_archivo}")
    print(f"   Tamaño: {canvas_w} × {canvas_h} px")


if __name__ == "__main__":
    componer_imagen_final(DATOS_URL, NOMBRE_ARCHIVO)
