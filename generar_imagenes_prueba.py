"""
Script para generar imágenes de prueba de microplásticos
Crea imágenes sintéticas que simulan microplásticos bajo microscopio
"""
import cv2
import numpy as np
import os

def crear_fondo_microscopio():
    """Crea un fondo que simula una imagen de microscopio"""
    fondo = np.random.normal(230, 15, (800, 1000, 3)).astype(np.uint8)
    # Añadir textura
    ruido = np.random.normal(0, 5, (800, 1000, 3)).astype(np.uint8)
    fondo = cv2.add(fondo, ruido)
    return fondo

def dibujar_fibra(img, x, y, longitud, grosor, angulo, color):
    """Dibuja una fibra (microplástico alargado)"""
    x2 = int(x + longitud * np.cos(np.radians(angulo)))
    y2 = int(y + longitud * np.sin(np.radians(angulo)))
    cv2.line(img, (x, y), (x2, y2), color, grosor)
    # Añadir pequeñas irregularidades
    segmentos = 5
    for i in range(segmentos):
        factor = i / segmentos
        px = int(x + factor * (x2 - x) + np.random.randint(-3, 3))
        py = int(y + factor * (y2 - y) + np.random.randint(-3, 3))
        cv2.circle(img, (px, py), grosor//2, color, -1)
    return [(x, y, x2, y2)]

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
    
    # Retornar bounding box
    x_min, y_min = np.min(puntos, axis=0)
    x_max, y_max = np.max(puntos, axis=0)
    return [(x_min, y_min, x_max, y_max)]

def dibujar_esfera(img, x, y, radio, color):
    """Dibuja una esfera/partícula circular"""
    cv2.circle(img, (x, y), radio, color, -1)
    # Añadir brillo para simular volumen
    brillo = tuple([min(255, c + 40) for c in color])
    cv2.circle(img, (x - radio//3, y - radio//3), radio//3, brillo, -1)
    return [(x - radio, y - radio, x + radio, y + radio)]

def dibujar_pelicula(img, x, y, ancho, alto, color):
    """Dibuja una película/lámina irregular"""
    # Crear forma irregular
    puntos = []
    num_puntos = 8
    for i in range(num_puntos):
        angulo = 2 * np.pi * i / num_puntos
        rx = ancho * (0.7 + np.random.random() * 0.3)
        ry = alto * (0.7 + np.random.random() * 0.3)
        px = int(x + rx * np.cos(angulo))
        py = int(y + ry * np.sin(angulo))
        puntos.append([px, py])
    
    puntos = np.array(puntos, dtype=np.int32)
    # Hacer semitransparente
    overlay = img.copy()
    cv2.fillPoly(overlay, [puntos], color)
    cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)
    cv2.polylines(img, [puntos], True, tuple([c-30 for c in color]), 1)
    
    x_min, y_min = np.min(puntos, axis=0)
    x_max, y_max = np.max(puntos, axis=0)
    return [(x_min, y_min, x_max, y_max)]

def generar_imagen_fibras(nombre_archivo):
    """Genera imagen con fibras largas (tipo textil)"""
    img = crear_fondo_microscopio()
    anotaciones = []
    
    # Generar 5-10 fibras
    num_fibras = np.random.randint(5, 10)
    for _ in range(num_fibras):
        x = np.random.randint(50, 950)
        y = np.random.randint(50, 750)
        longitud = np.random.randint(100, 300)
        grosor = np.random.randint(3, 8)
        angulo = np.random.randint(0, 180)
        color = (np.random.randint(20, 120), np.random.randint(30, 150), np.random.randint(80, 200))
        bbox = dibujar_fibra(img, x, y, longitud, grosor, angulo, color)
        anotaciones.append(('fibra', bbox[0]))
    
    cv2.imwrite(nombre_archivo, img)
    return anotaciones

def generar_imagen_particulas(nombre_archivo):
    """Genera imagen con partículas uniformes (tipo cosmético)"""
    img = crear_fondo_microscopio()
    anotaciones = []
    
    # Generar 15-25 esferas
    num_esferas = np.random.randint(15, 25)
    for _ in range(num_esferas):
        x = np.random.randint(30, 970)
        y = np.random.randint(30, 770)
        radio = np.random.randint(8, 25)
        color = (np.random.randint(100, 180), np.random.randint(50, 120), np.random.randint(100, 200))
        bbox = dibujar_esfera(img, x, y, radio, color)
        anotaciones.append(('esfera', bbox[0]))
    
    cv2.imwrite(nombre_archivo, img)
    return anotaciones

def generar_imagen_mixta(nombre_archivo):
    """Genera imagen con diferentes tipos (ambiental)"""
    img = crear_fondo_microscopio()
    anotaciones = []
    
    # Mezcla de diferentes tipos
    # Algunas fibras
    for _ in range(3):
        x = np.random.randint(50, 950)
        y = np.random.randint(50, 750)
        longitud = np.random.randint(80, 200)
        grosor = np.random.randint(2, 6)
        angulo = np.random.randint(0, 180)
        color = (np.random.randint(40, 100), np.random.randint(60, 140), np.random.randint(100, 180))
        bbox = dibujar_fibra(img, x, y, longitud, grosor, angulo, color)
        anotaciones.append(('fibra', bbox[0]))
    
    # Algunos fragmentos
    for _ in range(5):
        x = np.random.randint(100, 900)
        y = np.random.randint(100, 700)
        tamaño = np.random.randint(20, 60)
        color = (np.random.randint(60, 140), np.random.randint(80, 160), np.random.randint(40, 120))
        bbox = dibujar_fragmento(img, x, y, tamaño, tamaño, color)
        anotaciones.append(('fragmento', bbox[0]))
    
    # Algunas esferas
    for _ in range(8):
        x = np.random.randint(30, 970)
        y = np.random.randint(30, 770)
        radio = np.random.randint(5, 15)
        color = (np.random.randint(120, 200), np.random.randint(80, 140), np.random.randint(160, 220))
        bbox = dibujar_esfera(img, x, y, radio, color)
        anotaciones.append(('esfera', bbox[0]))
    
    # Algunas películas
    for _ in range(2):
        x = np.random.randint(150, 850)
        y = np.random.randint(150, 650)
        ancho = np.random.randint(60, 120)
        alto = np.random.randint(40, 80)
        color = (np.random.randint(140, 200), np.random.randint(140, 200), np.random.randint(100, 160))
        bbox = dibujar_pelicula(img, x, y, ancho, alto, color)
        anotaciones.append(('pelicula', bbox[0]))
    
    cv2.imwrite(nombre_archivo, img)
    return anotaciones

def main():
    """Genera todas las imágenes de prueba"""
    output_dir = "data/raw_images"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generando imágenes de prueba...")
    print("=" * 60)
    
    # Imagen 1: Fibras textiles
    print("\n1. Generando: Textil_A_fibras_largas.jpg")
    anotaciones = generar_imagen_fibras(os.path.join(output_dir, "Textil_A_fibras_largas.jpg"))
    print(f"   ✓ Creada con {len(anotaciones)} fibras")
    
    # Imagen 2: Partículas cosméticas
    print("\n2. Generando: Cosmetico_B_particulas_uniformes.jpg")
    anotaciones = generar_imagen_particulas(os.path.join(output_dir, "Cosmetico_B_particulas_uniformes.jpg"))
    print(f"   ✓ Creada con {len(anotaciones)} partículas esféricas")
    
    # Imagen 3: Muestra ambiental mixta
    print("\n3. Generando: Ambiental_C_muestra_real.jpg")
    anotaciones = generar_imagen_mixta(os.path.join(output_dir, "Ambiental_C_muestra_real.jpg"))
    print(f"   ✓ Creada con {len(anotaciones)} microplásticos de varios tipos")
    
    # Imágenes adicionales de prueba
    print("\n4. Generando: muestra_prueba_1.jpg")
    anotaciones = generar_imagen_fibras(os.path.join(output_dir, "muestra_prueba_1.jpg"))
    print(f"   ✓ Creada con {len(anotaciones)} fibras")
    
    print("\n5. Generando: muestra_prueba_2.jpg")
    anotaciones = generar_imagen_mixta(os.path.join(output_dir, "muestra_prueba_2.jpg"))
    print(f"   ✓ Creada con {len(anotaciones)} microplásticos mixtos")
    
    print("\n6. Generando: muestra_prueba_4.jpg")
    anotaciones = generar_imagen_particulas(os.path.join(output_dir, "muestra_prueba_4.jpg"))
    print(f"   ✓ Creada con {len(anotaciones)} partículas")
    
    print("\n" + "=" * 60)
    print("✓ Todas las imágenes de prueba fueron generadas exitosamente!")
    print(f"\nUbicación: {os.path.abspath(output_dir)}")
    print("\nPuedes usar estas imágenes para:")
    print("  • Probar el procesamiento de imágenes")
    print("  • Anotar con LabelImg")
    print("  • Entrenar modelos YOLO")
    print("  • Generar estadísticas y gráficos")

if __name__ == "__main__":
    main()
