"""
Módulo de procesamiento de imágenes para análisis de microplásticos.

Este módulo contiene funciones para cargar, preprocesar y segmentar
imágenes microscópicas de microplásticos en máscaras de pestañas.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Tuple, List, Dict
from skimage import measure, morphology
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config.config import IMAGE_PARAMS


class ImageProcessor:
    """Clase para procesar imágenes microscópicas de microplásticos."""
    
    def __init__(self, pixels_to_um: float = None):
        """
        Inicializa el procesador de imágenes.
        
        Args:
            pixels_to_um: Factor de conversión de píxeles a micrómetros.
                         Si es None, usa el valor de configuración.
        """
        self.pixels_to_um = pixels_to_um or IMAGE_PARAMS['pixels_to_um']
        
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
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocesa la imagen para análisis.
        
        Args:
            image: Imagen original en formato BGR.
            
        Returns:
            Imagen preprocesada en escala de grises.
        """
        # Convertir a escala de grises
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Aplicar filtro de suavizado para reducir ruido
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Ecualización de histograma para mejorar contraste
        equalized = cv2.equalizeHist(blurred)
        
        return equalized
    
    def segment_particles(self, image: np.ndarray, 
                         threshold: int = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Segmenta partículas de microplásticos en la imagen.
        
        Args:
            image: Imagen preprocesada en escala de grises.
            threshold: Valor de umbral para binarización (0-255).
                      Si es None, usa umbral automático de Otsu.
            
        Returns:
            Tupla con (imagen binaria, imagen etiquetada).
        """
        if threshold is None:
            # Umbralización automática usando método de Otsu
            _, binary = cv2.threshold(image, 0, 255, 
                                     cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        else:
            # Umbralización con valor especificado
            _, binary = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
        
        # Operaciones morfológicas para limpiar la imagen
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        
        # Apertura para eliminar pequeños objetos
        opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)
        
        # Cierre para rellenar huecos
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel, iterations=2)
        
        # Etiquetar componentes conectados
        labeled = measure.label(closed, connectivity=2)
        
        return closed, labeled
    
    def extract_particles(self, labeled_image: np.ndarray,
                         min_area: int = None,
                         max_area: int = None) -> List[Dict]:
        """
        Extrae información de partículas individuales.
        
        Args:
            labeled_image: Imagen con regiones etiquetadas.
            min_area: Área mínima en píxeles para considerar una partícula.
            max_area: Área máxima en píxeles para considerar una partícula.
            
        Returns:
            Lista de diccionarios con propiedades de cada partícula.
        """
        min_area = min_area or IMAGE_PARAMS['min_particle_area']
        max_area = max_area or IMAGE_PARAMS['max_particle_area']
        
        # Extraer propiedades de regiones
        regions = measure.regionprops(labeled_image)
        
        particles = []
        for region in regions:
            # Filtrar por área
            if min_area <= region.area <= max_area:
                particle_info = {
                    'label': region.label,
                    'area_pixels': region.area,
                    'area_um2': region.area * (self.pixels_to_um ** 2),
                    'perimeter_pixels': region.perimeter,
                    'perimeter_um': region.perimeter * self.pixels_to_um,
                    'centroid': region.centroid,
                    'bbox': region.bbox,
                    'major_axis': region.major_axis_length * self.pixels_to_um,
                    'minor_axis': region.minor_axis_length * self.pixels_to_um,
                    'eccentricity': region.eccentricity,
                    'solidity': region.solidity,
                    'orientation': region.orientation,
                }
                
                # Calcular relación de aspecto
                if region.minor_axis_length > 0:
                    particle_info['aspect_ratio'] = (
                        region.major_axis_length / region.minor_axis_length
                    )
                else:
                    particle_info['aspect_ratio'] = 0
                
                # Calcular diámetro equivalente
                particle_info['equivalent_diameter_um'] = (
                    region.equivalent_diameter * self.pixels_to_um
                )
                
                particles.append(particle_info)
        
        return particles
    
    def process_image(self, image_path: str, 
                     save_processed: bool = True,
                     output_dir: str = None) -> Tuple[List[Dict], np.ndarray]:
        """
        Procesa una imagen completa y extrae partículas.
        
        Args:
            image_path: Ruta a la imagen de entrada.
            save_processed: Si True, guarda la imagen procesada.
            output_dir: Directorio donde guardar imágenes procesadas.
            
        Returns:
            Tupla con (lista de partículas, imagen etiquetada).
        """
        # Cargar imagen
        image = self.load_image(image_path)
        
        # Preprocesar
        preprocessed = self.preprocess_image(image)
        
        # Segmentar
        binary, labeled = self.segment_particles(preprocessed)
        
        # Extraer partículas
        particles = self.extract_particles(labeled)
        
        # Guardar imagen procesada si se solicita
        if save_processed and output_dir:
            output_path = Path(output_dir) / f"processed_{Path(image_path).name}"
            cv2.imwrite(str(output_path), binary)
        
        return particles, labeled
    
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
