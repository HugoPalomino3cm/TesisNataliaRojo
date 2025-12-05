"""
Módulo de procesamiento de imágenes para análisis de microplásticos.

Este módulo utiliza YOLOv8 para detección automática de microplásticos
en imágenes microscópicas de máscaras de pestañas.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Tuple, List, Dict, Optional
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config.config import IMAGE_PARAMS

# Importar detector YOLO
try:
    from src.yolo_detector import YOLODetector, YOLO_AVAILABLE
except ImportError:
    YOLO_AVAILABLE = False
    YOLODetector = None


class ImageProcessor:
    """Clase para procesar imágenes microscópicas de microplásticos con YOLOv8."""
    
    def __init__(self, 
                 pixels_to_um: float = None,
                 yolo_model_path: Optional[str] = None):
        """
        Inicializa el procesador de imágenes con YOLOv8.
        
        Args:
            pixels_to_um: Factor de conversión de píxeles a micrómetros.
            yolo_model_path: Ruta al modelo YOLO entrenado (.pt). Requerido.
        """
        self.pixels_to_um = pixels_to_um or IMAGE_PARAMS['pixels_to_um']
        
        if not YOLO_AVAILABLE:
            raise ImportError(
                "❌ YOLOv8 no está disponible.\n"
                "Instala ultralytics: pip install ultralytics torch torchvision"
            )
        
        if not yolo_model_path:
            raise ValueError(
                "❌ Debes proporcionar un modelo YOLO entrenado (.pt).\n"
                "Entrena uno en la pestaña 'Entrenar YOLOv8' primero."
            )
        
        # Inicializar detector YOLO
        try:
            self.yolo_detector = YOLODetector(
                model_path=yolo_model_path,
                pixels_to_um=self.pixels_to_um
            )
            print("✅ Detector YOLOv8 inicializado correctamente")
        except Exception as e:
            raise RuntimeError(f"❌ Error al inicializar YOLOv8: {e}")
        
    def load_image(self, image_path: str) -> np.ndarray:
        """
        Carga una imagen desde el disco.
        
        Args:
            image_path: Ruta a la imagen.
            
        Returns:
            Imagen como array de numpy.
        """
        image = cv2.imread(str(image_path))
        if image is None:
            raise FileNotFoundError(f"No se pudo cargar la imagen: {image_path}")
        return image
    
    def process_image(self, image_path: str, 
                     save_processed: bool = True,
                     output_dir: str = None) -> Tuple[List[Dict], np.ndarray]:
        """
        Procesa una imagen completa con YOLOv8 y extrae partículas.
        
        Args:
            image_path: Ruta a la imagen de entrada.
            save_processed: Si True, guarda la imagen anotada.
            output_dir: Directorio donde guardar imágenes procesadas.
            
        Returns:
            Tupla con (lista de partículas, imagen anotada).
        """
        # Cargar imagen
        image = self.load_image(image_path)
        
        # Detectar con YOLO
        particles, annotated = self.yolo_detector.detect_particles(
            image, 
            return_annotated=True
        )
        
        # Guardar imagen anotada si se solicita
        if save_processed and output_dir and annotated is not None:
            output_path = Path(output_dir) / f"yolo_{Path(image_path).name}"
            self.yolo_detector.save_annotated_image(annotated, output_path)
        
        return particles, annotated
    
    def create_overlay(self, original_image: np.ndarray,
                      labeled_image: np.ndarray,
                      particles: List[Dict]) -> np.ndarray:
        """
        Crea una imagen con partículas resaltadas.
        
        Args:
            original_image: Imagen original.
            labeled_image: Imagen con regiones etiquetadas.
            particles: Lista de partículas detectadas.
            
        Returns:
            Imagen con partículas resaltadas y numeradas.
        """
        # Crear copia de la imagen original
        if len(original_image.shape) == 2:
            overlay = cv2.cvtColor(original_image, cv2.COLOR_GRAY2BGR)
        else:
            overlay = original_image.copy()
        
        # Dibujar contornos y etiquetas
        for particle in particles:
            bbox = particle['bbox']
            centroid = particle['centroid']
            
            # Dibujar rectángulo
            cv2.rectangle(overlay, 
                         (bbox[1], bbox[0]), 
                         (bbox[3], bbox[2]),
                         (0, 255, 0), 2)
            
            # Agregar número de partícula
            text = f"{particle['label']}"
            cv2.putText(overlay, text, 
                       (int(centroid[1]), int(centroid[0])),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        return overlay
