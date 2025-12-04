"""
Script de ejemplo para ajustar parámetros de procesamiento.

Este script permite experimentar con diferentes parámetros
de umbralización y segmentación.
"""

import sys
from pathlib import Path
import cv2
import matplotlib.pyplot as plt
sys.path.append(str(Path(__file__).parent.parent))

from src.image_processing import ImageProcessor

def test_different_thresholds(image_path, thresholds=[100, 127, 150, 180]):
    """
    Prueba diferentes valores de umbral para ver cuál funciona mejor.
    
    Args:
        image_path: Ruta a la imagen de prueba
        thresholds: Lista de valores de umbral a probar
    """
    processor = ImageProcessor()
    
    # Cargar y preprocesar imagen
    image = processor.load_image(image_path)
    preprocessed = processor.preprocess_image(image)
    
    # Crear figura con subplots
    fig, axes = plt.subplots(2, len(thresholds), figsize=(16, 8))
    
    for i, threshold in enumerate(thresholds):
        # Segmentar con este umbral
        binary, labeled = processor.segment_particles(preprocessed, threshold)
        particles = processor.extract_particles(labeled)
        
        # Mostrar imagen binaria
        axes[0, i].imshow(binary, cmap='gray')
        axes[0, i].set_title(f'Umbral: {threshold}')
        axes[0, i].axis('off')
        
        # Mostrar partículas detectadas sobre imagen original
        overlay = processor.create_overlay(image, labeled, particles)
        axes[1, i].imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
        axes[1, i].set_title(f'{len(particles)} partículas')
        axes[1, i].axis('off')
    
    plt.tight_layout()
    plt.savefig('results/graphs/threshold_comparison.png', dpi=300)
    print(f"✓ Comparación guardada en: results/graphs/threshold_comparison.png")
    plt.show()

def test_area_filters(image_path, min_areas=[5, 10, 20, 50]):
    """
    Prueba diferentes áreas mínimas para filtrado de partículas.
    
    Args:
        image_path: Ruta a la imagen de prueba
        min_areas: Lista de áreas mínimas (en píxeles) a probar
    """
    processor = ImageProcessor()
    
    # Cargar y procesar
    image = processor.load_image(image_path)
    preprocessed = processor.preprocess_image(image)
    binary, labeled = processor.segment_particles(preprocessed)
    
    # Crear figura
    fig, axes = plt.subplots(1, len(min_areas), figsize=(16, 4))
    
    for i, min_area in enumerate(min_areas):
        # Extraer con diferente área mínima
        particles = processor.extract_particles(labeled, min_area=min_area)
        overlay = processor.create_overlay(image, labeled, particles)
        
        axes[i].imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
        axes[i].set_title(f'Área mín: {min_area}px\n{len(particles)} partículas')
        axes[i].axis('off')
    
    plt.tight_layout()
    plt.savefig('results/graphs/area_filter_comparison.png', dpi=300)
    print(f"✓ Comparación guardada en: results/graphs/area_filter_comparison.png")
    plt.show()

if __name__ == "__main__":
    # CAMBIAR por tu imagen de prueba
    test_image = "data/raw_images/tu_imagen.jpg"
    
    print("Probando diferentes umbrales...")
    test_different_thresholds(test_image)
    
    print("\nProbando diferentes filtros de área...")
    test_area_filters(test_image)
    
    print("\n✓ Pruebas completadas. Revisa las imágenes para elegir los mejores parámetros.")
    print("Luego, actualiza config/config.py con los valores óptimos.")
