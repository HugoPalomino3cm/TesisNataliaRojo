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
    venv_python = script_dir / "venv_py311" / "Scripts" / "python.exe"

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

    print("=" * 70)
    print("  LABELIMG - Python 3.11")
    print("=" * 70)
    print(f"📁 Imágenes:    {len(image_files)} archivos")
    print(f"📝 Anotaciones: {annotations_dir}")
    print("=" * 70)
    print()

    # Usar Python 3.11 del venv
    if venv_python.exists():
        python_exe = str(venv_python)
        print(f"✅ Usando Python 3.11: {python_exe}")
    else:
        print("⚠️  Entorno virtual no encontrado, ejecuta:")
        print("   abrir_labelimg.bat")
        input("\nPresiona Enter...")
        sys.exit(1)

    print("⏳ Iniciando labelImg...\n")

    try:
        result = subprocess.call([
            python_exe,
            '-m',
            'labelImg.labelImg',
            str(images_dir),
            str(classes_file),
            str(annotations_dir)
        ])
        
        if result == 0:
            print("\n✅ Cerrado correctamente")
        else:
            print(f"\n⚠️  Código: {result}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        input("\nPresiona Enter...")
        sys.exit(1)

if __name__ == '__main__':
    main()


