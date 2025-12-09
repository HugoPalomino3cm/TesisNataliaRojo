"""Script de prueba para diagnosticar labelImg"""
import sys
from pathlib import Path

print("1. Probando importación de PyQt5...")
try:
    from PyQt5.QtWidgets import QApplication
    print("   ✓ PyQt5.QtWidgets OK")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

print("\n2. Probando importación de labelImg...")
try:
    from labelImg.labelImg import MainWindow
    from labelImg import resources
    print("   ✓ labelImg importado OK")
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n3. Creando aplicación Qt...")
try:
    app = QApplication(sys.argv)
    print("   ✓ QApplication creada")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

print("\n4. Creando ventana MainWindow...")
try:
    # Configurar rutas
    script_dir = Path(__file__).parent
    images_dir = str(script_dir / "data" / "raw_images")
    classes_file = str(script_dir / "data" / "annotations" / "predefined_classes.txt")
    annotations_dir = str(script_dir / "data" / "annotations")
    
    print(f"   Imágenes: {images_dir}")
    print(f"   Clases: {classes_file}")
    print(f"   Anotaciones: {annotations_dir}")
    
    win = MainWindow(images_dir, classes_file, annotations_dir)
    print("   ✓ MainWindow creada")
except Exception as e:
    print(f"   ✗ Error al crear MainWindow: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n5. Mostrando ventana...")
try:
    win.show()
    win.raise_()
    win.activateWindow()
    print("   ✓ Ventana mostrada (debería aparecer ahora)")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

print("\n6. Ejecutando bucle de eventos...")
print("   La ventana de LabelImg debería estar abierta.")
print("   Cierra la ventana para continuar...\n")

try:
    exit_code = app.exec_()
    print(f"\n✓ Aplicación cerrada con código: {exit_code}")
except Exception as e:
    print(f"\n✗ Error durante ejecución: {e}")
    import traceback
    traceback.print_exc()

input("\nPresiona Enter para salir...")
