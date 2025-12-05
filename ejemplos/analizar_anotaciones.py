"""
Script: Convertir Anotaciones de LabelImg a DataFrame
======================================================

Este script lee los archivos XML generados por LabelImg y los
convierte a un DataFrame de pandas para análisis posterior.
"""

import sys
from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd

# Agregar directorio src al path
sys.path.append(str(Path(__file__).parent.parent))

from src.image_annotation import ImageAnnotator
from config.config import RAW_IMAGES_DIR


def parse_labelimg_xml(xml_file):
    """
    Parsea un archivo XML de LabelImg.
    
    Args:
        xml_file (Path): Ruta al archivo XML
        
    Returns:
        list: Lista de diccionarios con información de objetos
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    filename = root.find('filename').text
    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)
    
    objects = []
    
    for obj in root.findall('object'):
        name = obj.find('name').text
        bndbox = obj.find('bndbox')
        
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)
        
        # Calcular dimensiones de la caja
        box_width = xmax - xmin
        box_height = ymax - ymin
        box_area = box_width * box_height
        aspect_ratio = box_width / box_height if box_height > 0 else 0
        
        objects.append({
            'filename': filename,
            'image_width': width,
            'image_height': height,
            'class': name,
            'xmin': xmin,
            'ymin': ymin,
            'xmax': xmax,
            'ymax': ymax,
            'box_width': box_width,
            'box_height': box_height,
            'box_area': box_area,
            'aspect_ratio': aspect_ratio
        })
    
    return objects


def annotations_to_dataframe(annotations_dir):
    """
    Convierte todas las anotaciones a un DataFrame.
    
    Args:
        annotations_dir (Path): Directorio con archivos XML
        
    Returns:
        pd.DataFrame: DataFrame con todas las anotaciones
    """
    annotations_dir = Path(annotations_dir)
    
    all_objects = []
    
    for xml_file in annotations_dir.glob("*.xml"):
        try:
            objects = parse_labelimg_xml(xml_file)
            all_objects.extend(objects)
        except Exception as e:
            print(f"⚠️  Error al procesar {xml_file.name}: {e}")
    
    if not all_objects:
        return pd.DataFrame()
    
    df = pd.DataFrame(all_objects)
    return df


def main():
    """Función principal."""
    
    print("=" * 70)
    print("  CONVERSIÓN DE ANOTACIONES LABELIMG A DATAFRAME")
    print("=" * 70)
    print()
    
    # Inicializar anotador
    annotator = ImageAnnotator(RAW_IMAGES_DIR)
    
    print(f"Directorio de anotaciones: {annotator.annotations_dir}")
    print()
    
    # Convertir a DataFrame
    print("Convirtiendo anotaciones a DataFrame...")
    df = annotations_to_dataframe(annotator.annotations_dir)
    
    if df.empty:
        print("❌ No se encontraron anotaciones.")
        return
    
    print(f"✅ Se procesaron {len(df)} objetos anotados")
    print()
    
    # Mostrar resumen
    print("-" * 70)
    print("  RESUMEN DE DATOS")
    print("-" * 70)
    print(f"\nTotal de objetos: {len(df)}")
    print(f"Imágenes únicas: {df['filename'].nunique()}")
    print()
    
    print("Distribución por clase:")
    class_counts = df['class'].value_counts()
    for clase, count in class_counts.items():
        percentage = (count / len(df) * 100)
        print(f"  • {clase:30s} : {count:4d} ({percentage:5.1f}%)")
    
    print()
    print("-" * 70)
    print("  ESTADÍSTICAS DE CAJAS DELIMITADORAS")
    print("-" * 70)
    
    print(f"\nÁrea promedio de cajas: {df['box_area'].mean():.1f} píxeles²")
    print(f"Área mínima: {df['box_area'].min():.0f} píxeles²")
    print(f"Área máxima: {df['box_area'].max():.0f} píxeles²")
    
    print(f"\nRelación de aspecto promedio: {df['aspect_ratio'].mean():.2f}")
    print(f"Relación mínima: {df['aspect_ratio'].min():.2f}")
    print(f"Relación máxima: {df['aspect_ratio'].max():.2f}")
    
    print()
    print("-" * 70)
    
    # Preguntar si desea exportar
    respuesta = input("\n¿Desea exportar los datos a Excel? (s/n): ")
    
    if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        output_file = annotator.annotations_dir / "anotaciones_resumen.xlsx"
        
        # Crear resumen por clase
        summary = df.groupby('class').agg({
            'box_area': ['count', 'mean', 'std', 'min', 'max'],
            'aspect_ratio': ['mean', 'std', 'min', 'max']
        }).round(2)
        
        # Exportar
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Datos Completos', index=False)
            summary.to_excel(writer, sheet_name='Resumen por Clase')
        
        print(f"\n✅ Datos exportados a: {output_file}")
    
    print("\n👋 ¡Listo!")


if __name__ == "__main__":
    main()
