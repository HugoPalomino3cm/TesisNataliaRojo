"""
Módulo para entrenar modelos YOLOv8 para detección de microplásticos.

Este módulo convierte las anotaciones de LabelImg (formato PASCAL VOC XML)
al formato YOLO y entrena un modelo personalizado de YOLOv8.
"""

import os
import yaml
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Tuple
import random

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("⚠️ ultralytics no está instalado. Ejecuta: pip install ultralytics")


class YOLOTrainer:
    """Clase para entrenar modelos YOLOv8 con anotaciones de microplásticos."""
    
    # Clases de microplásticos (deben coincidir con LabelImg y YOLODetector)
    CLASS_NAMES = [
        'fibra',
        'fragmento',
        'pelicula',
        'esfera',
        'microplastico_irregular',
        'aglomerado'
    ]
    
    def __init__(self,
                 annotations_dir: str,
                 images_dir: str,
                 output_dir: str = "yolo_training"):
        """
        Inicializa el entrenador YOLO.
        
        Args:
            annotations_dir: Directorio con archivos XML de LabelImg.
            images_dir: Directorio con imágenes correspondientes.
            output_dir: Directorio donde guardar dataset y modelo.
        """
        if not YOLO_AVAILABLE:
            raise ImportError(
                "ultralytics no está instalado. "
                "Ejecuta: pip install ultralytics torch torchvision"
            )
        
        self.annotations_dir = Path(annotations_dir)
        self.images_dir = Path(images_dir)
        self.output_dir = Path(output_dir)
        
        # Crear directorios de salida
        self.dataset_dir = self.output_dir / "dataset"
        self.models_dir = self.output_dir / "models"
        
        self.dataset_dir.mkdir(parents=True, exist_ok=True)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        # Almacenar información sobre splits
        self.has_test_split = False
    
    def _get_next_training_number(self, project_name: str) -> int:
        """
        Obtiene el siguiente número de entrenamiento disponible.
        
        Args:
            project_name: Nombre del proyecto.
            
        Returns:
            Siguiente número de entrenamiento.
        """
        project_dir = self.models_dir / project_name
        if not project_dir.exists():
            return 1
        
        # Buscar carpetas que sigan el patrón yolov8_N
        import re
        max_num = 0
        for folder in project_dir.iterdir():
            if folder.is_dir():
                match = re.match(r'yolov8_(\d+)', folder.name)
                if match:
                    num = int(match.group(1))
                    max_num = max(max_num, num)
        
        return max_num + 1
    
    def convert_voc_to_yolo(self,
                           train_split: float = 0.8,
                           val_split: float = 0.15) -> str:
        """
        Convierte anotaciones PASCAL VOC (XML) a formato YOLO (TXT).
        
        Args:
            train_split: Proporción de datos para entrenamiento (0-1).
            val_split: Proporción de datos para validación (0-1).
            
        Returns:
            Ruta al archivo data.yaml generado.
        """
        print("\n📦 Convirtiendo anotaciones VOC a YOLO...")
        
        # Crear estructura de directorios YOLO
        splits = ['train', 'val', 'test']
        for split in splits:
            (self.dataset_dir / split / 'images').mkdir(parents=True, exist_ok=True)
            (self.dataset_dir / split / 'labels').mkdir(parents=True, exist_ok=True)
        
        # Obtener lista de archivos XML
        xml_files = list(self.annotations_dir.glob('*.xml'))
        
        if not xml_files:
            raise FileNotFoundError(
                f"No se encontraron archivos XML en {self.annotations_dir}"
            )
        
        print(f"   Encontrados {len(xml_files)} archivos de anotaciones")
        
        # Dividir en train/val/test
        random.shuffle(xml_files)
        total_files = len(xml_files)
        
        # Ajustar splits para datasets pequeños
        if total_files <= 10:
            # Para datasets muy pequeños, asegurar al menos 1 imagen en val
            n_val = max(1, int(total_files * 0.2))  # Al menos 1 para validación
            n_test = max(0, int(total_files * 0.1))  # Puede ser 0 si es muy pequeño
            n_train = total_files - n_val - n_test
            
            train_files = xml_files[:n_train]
            val_files = xml_files[n_train:n_train + n_val]
            test_files = xml_files[n_train + n_val:] if n_test > 0 else []
        else:
            # División normal para datasets más grandes
            n_train = int(total_files * train_split)
            n_val = int(total_files * val_split)
            
            train_files = xml_files[:n_train]
            val_files = xml_files[n_train:n_train + n_val]
            test_files = xml_files[n_train + n_val:]
        
        print(f"   Train: {len(train_files)}, Val: {len(val_files)}, Test: {len(test_files)}")
        
        # Marcar si hay imágenes de test
        self.has_test_split = len(test_files) > 0
        
        # Convertir cada split
        for split_name, split_files in [
            ('train', train_files),
            ('val', val_files),
            ('test', test_files)
        ]:
            if split_files:
                self._convert_split(split_files, split_name)
        
        # Crear archivo data.yaml
        data_yaml_path = self._create_data_yaml()
        
        print(f"✅ Conversión completada")
        print(f"   Dataset guardado en: {self.dataset_dir}")
        
        return data_yaml_path
    
    def _convert_split(self, xml_files: List[Path], split_name: str):
        """
        Convierte un conjunto de archivos XML a formato YOLO.
        
        Args:
            xml_files: Lista de archivos XML a convertir.
            split_name: Nombre del split ('train', 'val', 'test').
        """
        images_out = self.dataset_dir / split_name / 'images'
        labels_out = self.dataset_dir / split_name / 'labels'
        
        converted = 0
        skipped = 0
        
        for xml_file in xml_files:
            try:
                # Parsear XML
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                # Obtener dimensiones de imagen
                size = root.find('size')
                img_width = int(size.find('width').text)
                img_height = int(size.find('height').text)
                
                # Obtener nombre de archivo de imagen
                filename = root.find('filename').text
                image_path = self.images_dir / filename
                
                if not image_path.exists():
                    print(f"   ⚠️ Imagen no encontrada: {filename}")
                    skipped += 1
                    continue
                
                # Copiar imagen
                shutil.copy(image_path, images_out / filename)
                
                # Convertir anotaciones
                yolo_annotations = []
                for obj in root.findall('object'):
                    class_name = obj.find('name').text.lower()
                    
                    # Obtener ID de clase
                    if class_name not in self.CLASS_NAMES:
                        print(f"   ⚠️ Clase desconocida: {class_name}")
                        continue
                    
                    class_id = self.CLASS_NAMES.index(class_name)
                    
                    # Obtener bounding box
                    bbox = obj.find('bndbox')
                    xmin = float(bbox.find('xmin').text)
                    ymin = float(bbox.find('ymin').text)
                    xmax = float(bbox.find('xmax').text)
                    ymax = float(bbox.find('ymax').text)
                    
                    # Convertir a formato YOLO (normalizado)
                    x_center = ((xmin + xmax) / 2) / img_width
                    y_center = ((ymin + ymax) / 2) / img_height
                    width = (xmax - xmin) / img_width
                    height = (ymax - ymin) / img_height
                    
                    # Validar valores
                    if (0 <= x_center <= 1 and 0 <= y_center <= 1 and
                        0 < width <= 1 and 0 < height <= 1):
                        yolo_annotations.append(
                            f"{class_id} {x_center:.6f} {y_center:.6f} "
                            f"{width:.6f} {height:.6f}"
                        )
                
                # Guardar archivo de etiquetas YOLO
                if yolo_annotations:
                    label_file = labels_out / f"{Path(filename).stem}.txt"
                    with open(label_file, 'w') as f:
                        f.write('\n'.join(yolo_annotations))
                    converted += 1
                else:
                    skipped += 1
                    
            except Exception as e:
                print(f"   ❌ Error procesando {xml_file.name}: {e}")
                skipped += 1
        
        print(f"   {split_name}: {converted} convertidos, {skipped} omitidos")
    
    def _create_data_yaml(self) -> str:
        """
        Crea el archivo data.yaml para entrenamiento YOLO.
        
        Returns:
            Ruta al archivo data.yaml.
        """
        data_yaml_path = self.output_dir / 'data.yaml'
        
        # Convertir rutas de Windows a forward slashes para compatibilidad YAML
        dataset_path = str(self.dataset_dir.absolute()).replace('\\', '/')
        
        # Crear YAML manualmente en el orden correcto que YOLO espera
        yaml_content = f"""path: {dataset_path}
train: train/images
val: val/images
"""
        
        # Solo incluir test si hay imágenes de test
        if self.has_test_split:
            yaml_content += "test: test/images\n"
        
        yaml_content += f"\nnc: {len(self.CLASS_NAMES)}\nnames:\n"
        
        # Agregar nombres de clases con formato de lista YAML
        for class_name in self.CLASS_NAMES:
            yaml_content += f"  - {class_name}\n"
        
        # Escribir archivo
        with open(data_yaml_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        
        print(f"   Archivo data.yaml creado: {data_yaml_path}")
        
        return str(data_yaml_path)
    
    def train_model(self,
                   data_yaml: str,
                   model_size: str = 'n',
                   epochs: int = 100,
                   imgsz: int = 320,
                   batch: int = 2,
                   device: str = 'cpu',
                   patience: int = 50,
                   project_name: str = 'microplasticos',
                   name: str = None) -> tuple:
        """
        Entrena un modelo YOLOv8.
        
        Args:
            data_yaml: Ruta al archivo data.yaml.
            model_size: Tamaño del modelo ('n', 's', 'm', 'l', 'x').
            epochs: Número de épocas de entrenamiento.
            imgsz: Tamaño de imagen para entrenamiento.
            batch: Tamaño del batch.
            device: Dispositivo ('0' para GPU, 'cpu' para CPU).
            patience: Épocas sin mejora antes de early stopping.
            project_name: Nombre del proyecto.
            name: Nombre del experimento (opcional, se auto-genera si es None).
            
        Returns:
            Tupla con (ruta al mejor modelo, número de entrenamiento).
        """
        # Obtener el siguiente número de entrenamiento
        training_number = self._get_next_training_number(project_name)
        if name is None:
            name = f'yolov8_{training_number}'
        
        print(f"\n🚀 Iniciando entrenamiento YOLOv8{model_size} - Entrenamiento #{training_number}")
        print(f"   Épocas: {epochs}")
        print(f"   Tamaño imagen: {imgsz}")
        print(f"   Batch size: {batch}")
        print(f"   Dispositivo: {device}")
        
        # Cargar modelo base
        model = YOLO(f'yolov8{model_size}.pt')
        
        # Entrenar con configuración optimizada para poca memoria
        results = model.train(
            data=data_yaml,
            epochs=epochs,
            imgsz=imgsz,
            batch=batch,
            device=device,
            patience=patience,
            project=str(self.models_dir / project_name),
            name=name,
            exist_ok=False,  # Crear nueva carpeta para cada entrenamiento
            verbose=True,
            save=True,
            plots=True,
            val=True,
            workers=1,
            cache=False
        )
        
        # Obtener el path real del modelo desde el objeto trainer
        # YOLO guarda el path en model.trainer.save_dir
        save_dir = Path(model.trainer.save_dir)
        best_model_path = save_dir / 'weights' / 'best.pt'
        
        # Verificar que el archivo existe
        if not best_model_path.exists():
            raise FileNotFoundError(
                f"No se encontró el modelo entrenado en {best_model_path}\n"
                f"Directorio de guardado: {save_dir}"
            )
        
        print(f"\n✅ Entrenamiento #{training_number} completado")
        print(f"   Mejor modelo: {best_model_path}")
        
        return str(best_model_path), training_number
    
    def evaluate_model(self, model_path: str, data_yaml: str):
        """
        Evalúa un modelo entrenado.
        
        Args:
            model_path: Ruta al modelo entrenado (.pt).
            data_yaml: Ruta al archivo data.yaml.
        """
        print(f"\n📊 Evaluando modelo: {model_path}")
        
        model = YOLO(model_path)
        
        # Validar en conjunto de validación
        metrics = model.val(data=data_yaml, split='val')
        
        print("\n📈 Métricas de validación:")
        print(f"   mAP50: {metrics.box.map50:.4f}")
        print(f"   mAP50-95: {metrics.box.map:.4f}")
        print(f"   Precisión: {metrics.box.mp:.4f}")
        print(f"   Recall: {metrics.box.mr:.4f}")
        
        # Validar en conjunto de prueba solo si existe
        test_metrics = None
        if self.has_test_split:
            test_metrics = model.val(data=data_yaml, split='test')
            print("\n📈 Métricas de prueba:")
            print(f"   mAP50: {test_metrics.box.map50:.4f}")
            print(f"   mAP50-95: {test_metrics.box.map:.4f}")
        else:
            print("\n⚠️  No hay conjunto de prueba (dataset muy pequeño)")
        
        return metrics, test_metrics
    
    def export_model(self,
                    model_path: str,
                    format: str = 'onnx') -> str:
        """
        Exporta el modelo a diferentes formatos.
        
        Args:
            model_path: Ruta al modelo entrenado (.pt).
            format: Formato de exportación ('onnx', 'torchscript', 'tflite', etc.).
            
        Returns:
            Ruta al modelo exportado.
        """
        print(f"\n📤 Exportando modelo a formato {format}...")
        
        model = YOLO(model_path)
        exported_path = model.export(format=format)
        
        print(f"✅ Modelo exportado: {exported_path}")
        
        return exported_path


def main():
    """Función principal para entrenar un modelo."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Entrenar YOLOv8 para detección de microplásticos'
    )
    parser.add_argument(
        '--annotations',
        type=str,
        default='data/raw_images',
        help='Directorio con archivos XML de LabelImg'
    )
    parser.add_argument(
        '--images',
        type=str,
        default='data/raw_images',
        help='Directorio con imágenes'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='yolo_training',
        help='Directorio de salida'
    )
    parser.add_argument(
        '--model-size',
        type=str,
        default='n',
        choices=['n', 's', 'm', 'l', 'x'],
        help='Tamaño del modelo YOLO'
    )
    parser.add_argument(
        '--epochs',
        type=int,
        default=100,
        help='Número de épocas'
    )
    parser.add_argument(
        '--batch',
        type=int,
        default=16,
        help='Tamaño del batch'
    )
    parser.add_argument(
        '--imgsz',
        type=int,
        default=640,
        help='Tamaño de imagen'
    )
    parser.add_argument(
        '--device',
        type=str,
        default='0',
        help='Dispositivo (0 para GPU, cpu para CPU)'
    )
    
    args = parser.parse_args()
    
    if not YOLO_AVAILABLE:
        print("❌ ultralytics no está instalado.")
        print("   Ejecuta: pip install ultralytics torch torchvision")
        return
    
    # Crear entrenador
    trainer = YOLOTrainer(
        annotations_dir=args.annotations,
        images_dir=args.images,
        output_dir=args.output
    )
    
    # Convertir dataset
    data_yaml = trainer.convert_voc_to_yolo()
    
    # Entrenar modelo
    best_model, training_number = trainer.train_model(
        data_yaml=data_yaml,
        model_size=args.model_size,
        epochs=args.epochs,
        batch=args.batch,
        imgsz=args.imgsz,
        device=args.device
    )
    
    # Evaluar modelo
    trainer.evaluate_model(best_model, data_yaml)
    
    print(f"\n🎉 Entrenamiento #{training_number} completado exitosamente!")
    print(f"   Modelo guardado en: {best_model}")
    print(f"\n💡 Para usar el modelo en la aplicación:")
    print(f"   1. Copia el modelo a la carpeta 'models/'")
    print(f"   2. En la GUI, selecciona 'YOLOv8' como método de detección")
    print(f"   3. Carga el modelo entrenado")


if __name__ == "__main__":
    main()
