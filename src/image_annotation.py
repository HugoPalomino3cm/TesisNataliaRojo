"""
Módulo de Anotación de Imágenes con LabelImg
=============================================

Este módulo proporciona funcionalidad para anotar y etiquetar imágenes
de microplásticos usando LabelImg.
"""

import os
import sys
import subprocess
from pathlib import Path
from tkinter import messagebox


class ImageAnnotator:
    """Clase para gestionar la anotación de imágenes con LabelImg."""
    
    def __init__(self, images_dir, annotations_dir=None):
        """
        Inicializa el anotador de imágenes.
        
        Args:
            images_dir (str): Directorio con las imágenes a anotar
            annotations_dir (str): Directorio donde guardar las anotaciones (opcional)
        """
        self.images_dir = Path(images_dir)
        # Por defecto, las anotaciones se guardan en el mismo directorio que las imágenes
        self.annotations_dir = Path(annotations_dir) if annotations_dir else Path(images_dir)
        
        # Crear directorio de anotaciones si no existe
        self.annotations_dir.mkdir(parents=True, exist_ok=True)
        
        # Archivo de clases predefinidas para microplásticos
        self.predefined_classes_file = self.annotations_dir / "predefined_classes.txt"
        self._create_predefined_classes()
    
    def _create_predefined_classes(self):
        """Crea un archivo con clases predefinidas para microplásticos."""
        classes = [
            "fibra",
            "fragmento",
            "pelicula",
            "esfera",
            "microplastico_irregular",
            "aglomerado"
        ]
        
        with open(self.predefined_classes_file, 'w', encoding='utf-8') as f:
            for cls in classes:
                f.write(f"{cls}\n")
    
    def launch_labelimg(self):
        """
        Lanza LabelImg para anotar imágenes.
        
        Returns:
            bool: True si se lanzó correctamente, False si hubo error
        """
        try:
            # Verificar que el directorio de imágenes existe
            if not self.images_dir.exists():
                messagebox.showerror(
                    "Error",
                    f"El directorio de imágenes no existe:\n{self.images_dir}"
                )
                return False
            
            # Verificar que hay imágenes
            image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff')
            images = [f for f in self.images_dir.iterdir() 
                     if f.suffix.lower() in image_extensions]
            
            if not images:
                messagebox.showwarning(
                    "Advertencia",
                    f"No se encontraron imágenes en:\n{self.images_dir}"
                )
                return False
            
            print(f"Lanzando LabelImg...")
            print(f"  - Directorio de imágenes: {self.images_dir}")
            print(f"  - Directorio de anotaciones: {self.annotations_dir}")
            print(f"  - Clases predefinidas: {self.predefined_classes_file}")
            
            # Intentar usar labelImg directamente desde el entorno virtual
            try:
                # Buscar el ejecutable de Python del entorno virtual (pythonw = sin consola)
                venv_pythonw = Path(__file__).parent.parent / "venv_py311" / "Scripts" / "pythonw.exe"
                labelimg_script = Path(__file__).parent.parent / "labelImg_tool" / "labelImg.py"
                
                if not venv_pythonw.exists():
                    raise FileNotFoundError("Entorno virtual no encontrado")
                
                if not labelimg_script.exists():
                    raise FileNotFoundError("labelImg.py no encontrado en labelImg_tool/")
                
                # Ejecutar labelImg con pythonw (sin consola)
                cmd = [
                    str(venv_pythonw),
                    str(labelimg_script),
                    str(self.images_dir),
                    str(self.predefined_classes_file),
                    str(self.annotations_dir)
                ]
                
                print(f"Ejecutando: {' '.join(cmd)}")
                
                # Iniciar el proceso sin consola
                import subprocess
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                si.wShowWindow = subprocess.SW_HIDE
                
                process = subprocess.Popen(
                    cmd,
                    cwd=str(labelimg_script.parent),
                    startupinfo=si if os.name == 'nt' else None
                )
                
                print("✓ LabelImg iniciado exitosamente")
                print("  Si no se abre, usa el archivo: abrir_labelimg.vbs")
                return True
                    
            except Exception as e:
                print(f"Error al iniciar directamente: {e}")
                # Intentar con el archivo VBS
                try:
                    vbs_path = Path(__file__).parent.parent / "abrir_labelimg.vbs"
                    if vbs_path.exists():
                        subprocess.Popen(["wscript", str(vbs_path)], shell=True)
                        print("✓ LabelImg iniciando con VBScript...")
                        return True
                except:
                    pass
                
                messagebox.showwarning(
                    "Método alternativo",
                    f"No se pudo abrir desde aquí.\n\n"
                    f"SOLUCIÓN:\n"
                    f"Haz doble clic en: abrir_labelimg.vbs\n\n"
                    f"(Está en la carpeta principal del proyecto)"
                )
                return False
            
        except Exception as e:
            error_msg = str(e)
            messagebox.showerror(
                "Error al abrir LabelImg",
                f"No se pudo abrir LabelImg desde el botón.\n\n"
                f"Error: {error_msg}\n\n"
                f"SOLUCIÓN: Use el script VBS:\n"
                f"Haga doble clic en: abrir_labelimg.vbs"
            )
            print(f"Error detallado: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_annotation_files(self):
        """
        Obtiene lista de archivos de anotación existentes.
        
        Returns:
            list: Lista de archivos XML de anotaciones
        """
        if not self.annotations_dir.exists():
            return []
        
        return list(self.annotations_dir.glob("*.xml"))
    
    def get_annotation_stats(self):
        """
        Obtiene estadísticas de las anotaciones realizadas.
        
        Returns:
            dict: Diccionario con estadísticas de anotaciones
        """
        import xml.etree.ElementTree as ET
        
        annotation_files = self.get_annotation_files()
        
        if not annotation_files:
            return {
                'total_images': 0,
                'total_objects': 0,
                'classes': {}
            }
        
        total_objects = 0
        classes_count = {}
        
        for xml_file in annotation_files:
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                for obj in root.findall('object'):
                    name = obj.find('name').text
                    total_objects += 1
                    classes_count[name] = classes_count.get(name, 0) + 1
            except Exception as e:
                print(f"Error al leer {xml_file}: {e}")
        
        return {
            'total_images': len(annotation_files),
            'total_objects': total_objects,
            'classes': classes_count
        }


def launch_labelimg_standalone(images_dir=None, annotations_dir=None):
    """
    Función auxiliar para lanzar LabelImg de forma independiente.
    
    Args:
        images_dir (str): Directorio con imágenes (opcional)
        annotations_dir (str): Directorio de anotaciones (opcional)
    """
    from config.config import RAW_IMAGES_DIR
    
    if images_dir is None:
        images_dir = RAW_IMAGES_DIR
    
    annotator = ImageAnnotator(images_dir, annotations_dir)
    annotator.launch_labelimg()


def find_labelimg_executable():
    """Busca el ejecutable de labelImg en el PATH."""
    try:
        # Usar 'where' en Windows para encontrar el ejecutable
        result = subprocess.run(['where', 'labelImg'], capture_output=True, text=True, check=True, shell=True)
        # 'where' puede devolver múltiples rutas, tomar la primera
        path = result.stdout.strip().split('\n')[0]
        return path
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


if __name__ == "__main__":
    # Ejemplo de uso directo
    from config.config import RAW_IMAGES_DIR
    
    annotator = ImageAnnotator(RAW_IMAGES_DIR)
    print("\n=== Estadísticas de Anotaciones ===")
    stats = annotator.get_annotation_stats()
    print(f"Imágenes anotadas: {stats['total_images']}")
    print(f"Total de objetos: {stats['total_objects']}")
    print("\nObjetos por clase:")
    for clase, count in stats['classes'].items():
        print(f"  - {clase}: {count}")
    
    # Lanzar LabelImg
    print("\nLanzando LabelImg...")
    annotator.launch_labelimg()
