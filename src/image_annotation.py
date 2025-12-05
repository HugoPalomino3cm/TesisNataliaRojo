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
        self.annotations_dir = Path(annotations_dir) if annotations_dir else self.images_dir.parent / "annotations"
        
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
            
            # Método simplificado: usar start en Windows
            if os.name == 'nt':  # Windows
                try:
                    # Crear un script VBS temporal para abrir sin ventana CMD
                    vbs_script = self.annotations_dir / "launch_temp.vbs"
                    vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c labelImg ""{self.images_dir}"" ""{self.predefined_classes_file}"" ""{self.annotations_dir}""", 0, False
'''
                    with open(vbs_script, 'w') as f:
                        f.write(vbs_content)
                    
                    # Ejecutar el VBS
                    subprocess.Popen(['cscript', '//nologo', str(vbs_script)], 
                                   creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0)
                    
                    print("✓ LabelImg iniciado correctamente")
                    return True
                    
                except Exception as e:
                    print(f"Método VBS falló: {e}")
                    # Método alternativo: usar comando directo
                    try:
                        import winreg
                        # Obtener el ejecutable de Python
                        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                           r"SOFTWARE\Python\PythonCore", 0, 
                                           winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
                        # Cerrar la key
                        winreg.CloseKey(key)
                        
                        # Usar subprocess sin shell
                        cmd_str = f'cmd /c start /B labelImg "{self.images_dir}" "{self.predefined_classes_file}" "{self.annotations_dir}"'
                        os.system(cmd_str)
                        print("✓ LabelImg iniciado (método alternativo)")
                        return True
                    except Exception as e2:
                        print(f"Método alternativo falló: {e2}")
                        # Último recurso: abrir sin parámetros
                        try:
                            os.system('start labelImg')
                            messagebox.showinfo(
                                "LabelImg Abierto",
                                "LabelImg se abrió sin parámetros.\n\n"
                                "Desde LabelImg:\n"
                                "1. Haga clic en 'Open Dir'\n"
                                f"2. Navegue a: {self.images_dir}\n"
                                "3. Haga clic en 'Change Save Dir':\n"
                                f"   {self.annotations_dir}"
                            )
                            print("✓ LabelImg iniciado sin parámetros")
                            return True
                        except Exception as e3:
                            print(f"Todos los métodos fallaron: {e3}")
                            raise
            else:  # Linux/Mac
                cmd = [
                    "labelImg",
                    str(self.images_dir),
                    str(self.predefined_classes_file),
                    str(self.annotations_dir)
                ]
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL
                )
                print("✓ LabelImg iniciado correctamente")
                return True
            
        except FileNotFoundError:
            messagebox.showerror(
                "Error",
                "LabelImg no está instalado.\n\n"
                "Por favor, ejecute:\n"
                "pip install labelImg PyQt5"
            )
            return False
            
        except Exception as e:
            error_msg = str(e)
            messagebox.showerror(
                "Error al abrir LabelImg",
                f"No se pudo abrir LabelImg desde el botón.\n\n"
                f"Error: {error_msg}\n\n"
                f"SOLUCIÓN: Use el script batch:\n"
                f"Ejecute en una terminal: abrir_labelimg.bat\n\n"
                f"O ejecute manualmente:\n"
                f'labelImg "{self.images_dir}"'
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
