"""
Script para generar imagen de TEST (no para entrenamiento)
"""
import cv2
import numpy as np
import os

def crear_fondo_microscopio():
    """Crea un fondo que simula una imagen de microscopio"""
    fondo = np.random.normal(230, 15, (800, 1000, 3)).astype(np.uint8)
    ruido = np.random.normal(0, 5, (800, 1000, 3)).astype(np.uint8)
    fondo = cv2.add(fondo, ruido)
    return fondo

def dibujar_fibra(img, x, y, longitud, grosor, angulo, color):
    """Dibuja una fibra"""
    x2 = int(x + longitud * np.cos(np.radians(angulo)))
    y2 = int(y + longitud * np.sin(np.radians(angulo)))
    cv2.line(img, (x, y), (x2, y2), color, grosor)
    segmentos = 5
    for i in range(segmentos):
        factor = i / segmentos
        px = int(x + factor * (x2 - x) + np.random.randint(-3, 3))
        py = int(y + factor * (y2 - y) + np.random.randint(-3, 3))
        cv2.circle(img, (px, py), grosor//2, color, -1)

def dibujar_fragmento(img, x, y, ancho, alto, color):
    """Dibuja un fragmento irregular"""
    puntos = []
    num_lados = np.random.randint(4, 8)
    for i in range(num_lados):
        angulo = 2 * np.pi * i / num_lados + np.random.uniform(-0.3, 0.3)
        radio = np.random.randint(ancho//2, ancho)
        px = int(x + radio * np.cos(angulo))
        py = int(y + radio * np.sin(angulo))
        puntos.append([px, py])
    
    puntos = np.array(puntos, dtype=np.int32)
    cv2.fillPoly(img, [puntos], color)
    cv2.polylines(img, [puntos], True, tuple([c-20 for c in color]), 2)

def dibujar_esfera(img, x, y, radio, color):
    """Dibuja una esfera"""
    cv2.circle(img, (x, y), radio, color, -1)
    brillo = tuple([min(255, c + 40) for c in color])
    cv2.circle(img, (x - radio//3, y - radio//3), radio//3, brillo, -1)

def generar_imagen_test_mixta(nombre_archivo):
    """Genera imagen de TEST con mezcla de microplásticos"""
    img = crear_fondo_microscopio()
    
    print("Generando imagen de TEST con:")
    
    # 4 fibras
    num_fibras = 4
    for _ in range(num_fibras):
        x = np.random.randint(50, 950)
        y = np.random.randint(50, 750)
        longitud = np.random.randint(90, 250)
        grosor = np.random.randint(3, 7)
        angulo = np.random.randint(0, 180)
        color = (np.random.randint(30, 110), np.random.randint(50, 150), np.random.randint(90, 200))
        dibujar_fibra(img, x, y, longitud, grosor, angulo, color)
    print(f"  • {num_fibras} fibras")
    
    # 6 fragmentos
    num_fragmentos = 6
    for _ in range(num_fragmentos):
        x = np.random.randint(100, 900)
        y = np.random.randint(100, 700)
        tamaño = np.random.randint(25, 55)
        color = (np.random.randint(70, 140), np.random.randint(90, 160), np.random.randint(50, 130))
        dibujar_fragmento(img, x, y, tamaño, tamaño, color)
    print(f"  • {num_fragmentos} fragmentos")
    
    # 10 esferas
    num_esferas = 10
    for _ in range(num_esferas):
        x = np.random.randint(40, 960)
        y = np.random.randint(40, 760)
        radio = np.random.randint(6, 20)
        color = (np.random.randint(110, 190), np.random.randint(70, 130), np.random.randint(150, 220))
        dibujar_esfera(img, x, y, radio, color)
    print(f"  • {num_esferas} esferas")
    
    total = num_fibras + num_fragmentos + num_esferas
    print(f"\n  TOTAL: {total} microplásticos")
    
    cv2.imwrite(nombre_archivo, img)
    print(f"\n✓ Imagen guardada: {nombre_archivo}")

def main():
    output_dir = "data/test_images"
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("GENERANDO IMAGEN DE VERIFICACIÓN (NO para entrenamiento)")
    print("=" * 60)
    print()
    
    nombre = os.path.join(output_dir, "imagen_test_verificacion.jpg")
    generar_imagen_test_mixta(nombre)
    
    print("\n" + "=" * 60)
    print("Esta imagen NO debe anotarse ni entrenarse.")
    print("Úsala SOLO para verificar el modelo después del entrenamiento.")
    print("=" * 60)

if __name__ == "__main__":
    main()
