"""
Módulo de detección de microplásticos usando YOLOv8.

Este módulo utiliza YOLOv8 de Ultralytics para detectar y clasificar
microplásticos en imágenes microscópicas de máscaras de pestañas.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import sys

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

sys.path.append(str(Path(__file__).parent.parent))
from config.config import IMAGE_PARAMS


class YOLODetector:
    """Clase para detectar microplásticos usando YOLOv8."""
    
    # Clases de microplásticos (deben coincidir con LabelImg)
    CLASS_NAMES = [
        'fibra',
        'fragmento', 
        'pelicula',
        'esfera',
        'microplastico_irregular',
        'aglomerado'
    ]
    
    def __init__(self, 
                 model_path: Optional[str] = None,
                 pixels_to_um: float = None,
                 confidence_threshold: float = 0.25,
                 iou_threshold: float = 0.45):
        """
        Inicializa el detector YOLO.
        
        Args:
            model_path: Ruta al modelo YOLOv8 entrenado (.pt).
                       Si es None, usa modelo preentrenado yolov8n.pt
            pixels_to_um: Factor de conversión de píxeles a micrómetros.
            confidence_threshold: Umbral de confianza para detecciones (0-1).
            iou_threshold: Umbral IoU para Non-Maximum Suppression.
        """
        if not YOLO_AVAILABLE:
            raise ImportError(
                "ultralytics no está instalado. "
                "Ejecuta: pip install ultralytics torch torchvision"
            )
        
        self.pixels_to_um = pixels_to_um or IMAGE_PARAMS['pixels_to_um']
        self.confidence_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
        
        # Cargar modelo
        if model_path and Path(model_path).exists():
            print(f"📦 Cargando modelo personalizado: {model_path}")
            self.model = YOLO(model_path)
        else:
            print("⚠️ No se encontró modelo personalizado. Usando YOLOv8n base.")
            print("   Para entrenar un modelo personalizado, usa src/train_yolo.py")
            self.model = YOLO('yolov8n.pt')  # Modelo base pequeño
        
        self.model_path = model_path
        
    def detect_particles(self, 
                        image: np.ndarray,
                        return_annotated: bool = True) -> Tuple[List[Dict], Optional[np.ndarray]]:
        """
        Detecta microplásticos en una imagen usando YOLOv8.
        
        Args:
            image: Imagen como array de numpy (BGR).
            return_annotated: Si True, devuelve imagen con anotaciones.
            
        Returns:
            Tupla con:
            - Lista de partículas detectadas (diccionarios con propiedades)
            - Imagen anotada (si return_annotated=True) o None
        """
        # Realizar detección
        results = self.model.predict(
            image,
            conf=self.confidence_threshold,
            iou=self.iou_threshold,
            verbose=False
        )[0]
        
        particles = []
        annotated_image = image.copy() if return_annotated else None
        
        # Procesar cada detección
        boxes = results.boxes
        for idx, box in enumerate(boxes):
            # Extraer información del bounding box
            xyxy = box.xyxy[0].cpu().numpy()  # [x1, y1, x2, y2]
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            
            x1, y1, x2, y2 = map(int, xyxy)
            
            # Extraer región de interés
            roi = image[y1:y2, x1:x2]
            
            # Calcular propiedades morfológicas
            particle_props = self._calculate_morphology(roi, xyxy)
            
            # Agregar metadatos de detección
            particle_props.update({
                'particle_id': idx + 1,
                'class_id': class_id,
                'class_name': self._get_class_name(class_id),
                'confidence': confidence,
                'bbox': [x1, y1, x2, y2],
                'detection_method': 'YOLOv8'
            })
            
            particles.append(particle_props)
            
            # Anotar imagen si se requiere
            if return_annotated:
                self._annotate_detection(
                    annotated_image, 
                    particle_props, 
                    x1, y1, x2, y2
                )
        
        return particles, annotated_image
    
    def _calculate_morphology(self, 
                             roi: np.ndarray, 
                             bbox: np.ndarray) -> Dict:
        """
        Calcula propiedades morfológicas de una partícula detectada.
        
        Args:
            roi: Región de interés de la partícula.
            bbox: Coordenadas del bounding box [x1, y1, x2, y2].
            
        Returns:
            Diccionario con propiedades morfológicas.
        """
        x1, y1, x2, y2 = bbox
        
        # Dimensiones del bounding box
        width_px = x2 - x1
        height_px = y2 - y1
        area_px = width_px * height_px
        
        # Convertir a escala real
        width_um = width_px * self.pixels_to_um
        height_um = height_px * self.pixels_to_um
        area_um2 = area_px * (self.pixels_to_um ** 2)
        
        # Calcular perímetro aproximado del bounding box
        perimeter_px = 2 * (width_px + height_px)
        perimeter_um = perimeter_px * self.pixels_to_um
        
        # Relación de aspecto
        aspect_ratio = width_px / height_px if height_px > 0 else 1.0
        
        # Circularidad aproximada (basada en bounding box)
        # Circularidad perfecta = 1.0 para un círculo
        circularity = (4 * np.pi * area_px) / (perimeter_px ** 2) if perimeter_px > 0 else 0
        
        # Elongación (1 = cuadrado, >1 = alargado)
        elongation = max(width_px, height_px) / min(width_px, height_px) if min(width_px, height_px) > 0 else 1.0
        
        # Diámetro equivalente (diámetro de círculo con misma área)
        equivalent_diameter_px = np.sqrt(4 * area_px / np.pi)
        equivalent_diameter_um = equivalent_diameter_px * self.pixels_to_um
        
        return {
            'area_um2': round(area_um2, 2),
            'perimeter_um': round(perimeter_um, 2),
            'width_um': round(width_um, 2),
            'height_um': round(height_um, 2),
            'aspect_ratio': round(aspect_ratio, 3),
            'circularity': round(circularity, 3),
            'elongation': round(elongation, 3),
            'equivalent_diameter_um': round(equivalent_diameter_um, 2),
            'centroid_x': round((x1 + x2) / 2, 1),
            'centroid_y': round((y1 + y2) / 2, 1)
        }
    
    def _get_class_name(self, class_id: int) -> str:
        """
        Obtiene el nombre de la clase según el ID.
        
        Args:
            class_id: ID de la clase (0-5).
            
        Returns:
            Nombre de la clase.
        """
        # Intentar obtener del modelo primero
        if hasattr(self.model, 'names') and class_id in self.model.names:
            return self.model.names[class_id]
        
        # Fallback a nombres predefinidos
        if 0 <= class_id < len(self.CLASS_NAMES):
            return self.CLASS_NAMES[class_id]
        
        return f'clase_{class_id}'
    
    def _annotate_detection(self,
                          image: np.ndarray,
                          particle: Dict,
                          x1: int, y1: int, x2: int, y2: int):
        """
        Anota una detección en la imagen.
        
        Args:
            image: Imagen donde anotar.
            particle: Diccionario con propiedades de la partícula.
            x1, y1, x2, y2: Coordenadas del bounding box.
        """
        # Color según clase (BGR para OpenCV)
        colors = {
            'fibra': (255, 0, 0),          # Azul
            'fragmento': (0, 255, 0),       # Verde
            'pelicula': (0, 255, 255),      # Amarillo
            'esfera': (255, 0, 255),        # Magenta
            'microplastico_irregular': (0, 165, 255),  # Naranja
            'aglomerado': (128, 0, 128)     # Púrpura
        }
        
        # Colores adicionales para clases nuevas (BGR)
        extra_colors = [
            (212, 182, 6),    # Cyan
            (22, 115, 249),   # Naranja oscuro
            (246, 92, 139),   # Violeta
            (153, 72, 236),   # Rosa
            (166, 184, 20),   # Teal
            (11, 158, 245),   # Ámbar
            (22, 204, 132),   # Lima
            (241, 102, 99),   # Índigo
            (247, 85, 168),   # Púrpura claro
            (68, 68, 239),    # Rojo claro
            (129, 185, 16),   # Esmeralda
            (246, 130, 59),   # Azul claro
            (239, 70, 217),   # Fucsia
            (238, 211, 34),   # Cyan claro
            (21, 204, 250),   # Amarillo oro
        ]
        
        class_name = particle['class_name']
        
        # Obtener color o generar uno automáticamente
        if class_name in colors:
            color = colors[class_name]
        else:
            # Generar color basado en hash del nombre para consistencia
            hash_val = hash(class_name) % len(extra_colors)
            color = extra_colors[hash_val]
        
        # Dibujar bounding box
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        
        # Etiqueta con clase y confianza
        label = f"{class_name}: {particle['confidence']:.2f}"
        
        # Fondo para el texto
        (label_width, label_height), _ = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
        )
        cv2.rectangle(
            image,
            (x1, y1 - label_height - 10),
            (x1 + label_width + 10, y1),
            color,
            -1
        )
        
        # Texto
        cv2.putText(
            image,
            label,
            (x1 + 5, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )
    
    def get_detection_summary(self, particles: List[Dict]) -> Dict:
        """
        Genera un resumen de las detecciones.
        
        Args:
            particles: Lista de partículas detectadas.
            
        Returns:
            Diccionario con estadísticas de detección.
        """
        if not particles:
            return {
                'total_particles': 0,
                'by_class': {},
                'avg_confidence': 0.0,
                'avg_area_um2': 0.0
            }
        
        # Contar por clase
        class_counts = {}
        confidences = []
        areas = []
        
        for p in particles:
            class_name = p['class_name']
            class_counts[class_name] = class_counts.get(class_name, 0) + 1
            confidences.append(p['confidence'])
            areas.append(p['area_um2'])
        
        return {
            'total_particles': len(particles),
            'by_class': class_counts,
            'avg_confidence': round(np.mean(confidences), 3),
            'avg_area_um2': round(np.mean(areas), 2),
            'min_area_um2': round(min(areas), 2),
            'max_area_um2': round(max(areas), 2)
        }
    
    def save_annotated_image(self, 
                           annotated_image: np.ndarray,
                           output_path: str):
        """
        Guarda la imagen anotada.
        
        Args:
            annotated_image: Imagen con anotaciones.
            output_path: Ruta donde guardar.
        """
        cv2.imwrite(str(output_path), annotated_image)
        print(f"✅ Imagen anotada guardada: {output_path}")


def test_detector():
    """Función de prueba del detector."""
    if not YOLO_AVAILABLE:
        print("❌ No se puede probar el detector sin ultralytics instalado.")
        return
    
    print("🧪 Probando YOLODetector...")
    
    # Crear detector con modelo base
    detector = YOLODetector()
    
    # Crear imagen de prueba
    test_image = np.zeros((640, 640, 3), dtype=np.uint8)
    cv2.rectangle(test_image, (100, 100), (200, 200), (255, 255, 255), -1)
    
    # Detectar
    particles, annotated = detector.detect_particles(test_image)
    
    print(f"✅ Detector inicializado correctamente")
    print(f"   Detectadas: {len(particles)} partículas")
    
    # Mostrar resumen
    summary = detector.get_detection_summary(particles)
    print(f"   Resumen: {summary}")


if __name__ == "__main__":
    test_detector()
