"""
Script de Ejemplo: Uso de LabelImg para Anotar Microplásticos
==============================================================

Este script muestra cómo usar el módulo de anotación de imágenes
de forma independiente, sin necesidad de la interfaz gráfica principal.
"""

import sys
from pathlib import Path

# Agregar directorio src al path
sys.path.append(str(Path(__file__).parent.parent))

from src.image_annotation import ImageAnnotator
from config.config import RAW_IMAGES_DIR


def main():
    """Función principal para anotar imágenes."""
    
    print("=" * 70)
    print("  ANOTACIÓN DE MICROPLÁSTICOS CON LABELIMG")
    print("=" * 70)
    print()
    
    # Crear anotador
    print("Inicializando anotador de imágenes...")
    annotator = ImageAnnotator(RAW_IMAGES_DIR)
    
    print(f"✓ Directorio de imágenes: {annotator.images_dir}")
    print(f"✓ Directorio de anotaciones: {annotator.annotations_dir}")
    print(f"✓ Archivo de clases: {annotator.predefined_classes_file}")
    print()
    
    # Mostrar estadísticas actuales
    print("-" * 70)
    print("  ESTADÍSTICAS ACTUALES")
    print("-" * 70)
    stats = annotator.get_annotation_stats()
    
    print(f"📷 Imágenes anotadas: {stats['total_images']}")
    print(f"🎯 Total de objetos etiquetados: {stats['total_objects']}")
    
    if stats['classes']:
        print("\n📊 Distribución por clase:")
        for clase, count in sorted(stats['classes'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / stats['total_objects'] * 100) if stats['total_objects'] > 0 else 0
            print(f"   • {clase:30s} : {count:4d} ({percentage:5.1f}%)")
    else:
        print("\n⚠️  No hay anotaciones disponibles todavía.")
    
    print()
    print("=" * 70)
    
    # Preguntar si desea abrir LabelImg
    respuesta = input("\n¿Desea abrir LabelImg para anotar imágenes? (s/n): ")
    
    if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        print("\n🚀 Lanzando LabelImg...")
        print("\nInstrucciones rápidas:")
        print("  • Presione 'w' para crear una caja delimitadora")
        print("  • Dibuje alrededor del microplástico")
        print("  • Seleccione la clase apropiada")
        print("  • Presione Ctrl+S para guardar")
        print("  • Use 'd' y 'a' para navegar entre imágenes")
        print("\nCierre LabelImg cuando termine de anotar.\n")
        
        success = annotator.launch_labelimg()
        
        if success:
            print("✅ LabelImg lanzado exitosamente")
        else:
            print("❌ No se pudo lanzar LabelImg")
            print("\nAsegúrese de haber instalado las dependencias:")
            print("  pip install labelImg PyQt5")
    else:
        print("\n👋 ¡Hasta luego!")


if __name__ == "__main__":
    main()
