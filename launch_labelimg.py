#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para lanzar LabelImg con Python 3.11
"""
import sys
import os
import subprocess
from pathlib import Path

def main():
    script_dir = Path(__file__).parent.resolve()
    os.chdir(script_dir)

    # Configurar las rutas
    images_dir = script_dir / "data" / "raw_images"
    annotations_dir = script_dir / "data" / "annotations"
    classes_file = annotations_dir / "predefined_classes.txt"
    
    # Python del entorno virtual
    venv_python = script_dir / "venv_py311" / "Scripts" / "pythonw.exe"

    # Crear directorios
    annotations_dir.mkdir(parents=True, exist_ok=True)

    # Crear archivo de clases
    if not classes_file.exists():
        with open(classes_file, 'w', encoding='utf-8') as f:
            f.write("fibra\nfragmento\npelicula\nesfera\nmicroplastico_irregular\naglomerado\n")

    # Verificar imágenes
    if not images_dir.exists():
        print(f"❌ No existe {images_dir}")
        input("Presiona Enter...")
        sys.exit(1)

    image_files = list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.png")) + \
                  list(images_dir.glob("*.jpeg")) + list(images_dir.glob("*.bmp"))

    if not image_files:
        print(f"⚠️  No hay imágenes en {images_dir}")
        input("Presiona Enter...")
        sys.exit(1)

    # Usar Python 3.11 del venv (pythonw = sin consola)
    if venv_python.exists():
        python_exe = str(venv_python)
    else:
        print("⚠️  Entorno virtual no encontrado, ejecuta:")
        print("   abrir_labelimg.bat")
        input("\nPresiona Enter...")
        sys.exit(1)

    # Ruta al script de labelImg clonado
    labelimg_script = script_dir / "labelImg_tool" / "labelImg.py"
    
    if not labelimg_script.exists():
        print(f"❌ No se encontró labelImg en: {labelimg_script}")
        print("⚠️  Ejecuta: git clone https://github.com/heartexlabs/labelImg.git labelImg_tool")
        input("\nPresiona Enter...")
        sys.exit(1)

    try:
        # Ejecutar labelImg desde el repositorio clonado (sin consola)
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = subprocess.SW_HIDE
        
        process = subprocess.Popen([
            python_exe,
            str(labelimg_script),
            str(images_dir),
            str(classes_file),
            str(annotations_dir)
        ], startupinfo=si if os.name == 'nt' else None)
        
        # No esperar a que termine
        # process.wait()
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        input("\nPresiona Enter...")
        sys.exit(1)

if __name__ == '__main__':
    main()


