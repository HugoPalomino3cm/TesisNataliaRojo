"""
Script de ejemplo para procesar una sola imagen.

Este script muestra cómo usar el sistema para procesar
una imagen individual de forma manual.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.image_processing import ImageProcessor
from src.statistical_analysis import StatisticalAnalyzer
from src.visualization import DataVisualizer

# Ejemplo de uso
if __name__ == "__main__":
    # Ruta a tu imagen (CAMBIAR por tu imagen real)
    image_path = "data/raw_images/tu_imagen.jpg"
    
    # Factor de calibración (CAMBIAR por tu valor real)
    pixels_to_um = 0.5  # Ejemplo: 0.5 μm por píxel
    
    # Inicializar procesador
    processor = ImageProcessor(pixels_to_um=pixels_to_um)
    
    # Procesar imagen
    print("Procesando imagen...")
    particles, labeled = processor.process_image(
        image_path,
        save_processed=True,
        output_dir="data/processed_images"
    )
    
    print(f"Detectadas {len(particles)} partículas")
    
    # Crear DataFrame
    analyzer = StatisticalAnalyzer()
    df = analyzer.particles_to_dataframe(particles, sample_id="Ejemplo")
    
    # Mostrar primeras filas
    print("\nPrimeras partículas detectadas:")
    print(df[['label', 'area_um2', 'equivalent_diameter_um', 'aspect_ratio']].head())
    
    # Generar visualización
    visualizer = DataVisualizer()
    visualizer.plot_size_distribution(df, sample_id="Ejemplo", 
                                     save_path="results/graphs/ejemplo.png")
    
    print("\n✓ Análisis completado. Ver resultados en results/graphs/")
