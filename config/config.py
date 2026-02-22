"""
Configuración del proyecto de análisis de microplásticos en máscaras de pestañas.
"""

import os
from pathlib import Path

# Rutas del proyecto
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_IMAGES_DIR = DATA_DIR / "raw_images"  # Para entrenamiento (con XML)
ANALYSIS_IMAGES_DIR = DATA_DIR / "analysis_images"  # Para análisis (sin XML)
PROCESSED_IMAGES_DIR = DATA_DIR / "processed_images"
# LabelImg guarda los XML junto a las imágenes por defecto
ANNOTATIONS_DIR = RAW_IMAGES_DIR
RESULTS_DIR = PROJECT_ROOT / "results"
GRAPHS_DIR = RESULTS_DIR / "graphs"
REPORTS_DIR = RESULTS_DIR / "reports"

# Parámetros de procesamiento de imágenes
IMAGE_PARAMS = {
    # Factor de conversión píxeles a micrómetros (μm)
    # AJUSTAR según la calibración de tu microscopio
    'pixels_to_um': 1.0,  # TODO: Calibrar con imagen de referencia
    
    # Umbral de segmentación (0-255)
    'threshold': 127,
    
    # Área mínima de partícula (píxeles)
    'min_particle_area': 10,
    
    # Área máxima de partícula (píxeles)
    'max_particle_area': 50000,
}

# Parámetros de análisis morfológico
MORPHOLOGY_PARAMS = {
    # Rangos de clasificación por tamaño (en μm)
    'size_categories': {
        'pequeño': (0, 50),
        'mediano': (50, 200),
        'grande': (200, float('inf'))
    },
    
    # Rangos de relación de aspecto
    'aspect_ratio_categories': {
        'esférico': (0.8, 1.2),
        'alargado': (1.2, 3.0),
        'fibra': (3.0, float('inf'))
    }
}

# Parámetros de visualización
PLOT_PARAMS = {
    'figure_size': (12, 8),
    'dpi': 300,
    'font_size': 12,
    'color_palette': 'Set2',
}

# Información de las muestras según el documento
SAMPLES_INFO = {
    'M1': {
        'nombre': 'Máscara 1',
        'descripcion': 'Primera muestra analizada',
        'color': '#1f77b4'
    },
    'M2': {
        'nombre': 'Máscara 2',
        'descripcion': 'Segunda muestra analizada',
        'color': '#ff7f0e'
    },
    'M3': {
        'nombre': 'Máscara 3',
        'descripcion': 'Tercera muestra analizada',
        'color': '#2ca02c'
    },
    # Agregar más muestras según sea necesario
}

# Crear directorios si no existen
for directory in [DATA_DIR, RAW_IMAGES_DIR, PROCESSED_IMAGES_DIR, 
                  RESULTS_DIR, GRAPHS_DIR, REPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
