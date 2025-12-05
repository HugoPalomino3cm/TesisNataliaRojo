# 📦 Directorio de Anotaciones

Este directorio almacena las anotaciones generadas con LabelImg.

## Contenido

Cuando uses LabelImg para anotar imágenes, se generarán archivos aquí:

- **predefined_classes.txt**: Lista de clases predefinidas
- **[nombre_imagen].xml**: Archivo de anotación por cada imagen

## Formato

Los archivos XML siguen el formato PASCAL VOC, compatible con la mayoría de frameworks de machine learning.

## Uso

1. No es necesario crear archivos manualmente aquí
2. Los archivos se generan automáticamente al usar LabelImg
3. Puedes analizar las anotaciones con: `python ejemplos/analizar_anotaciones.py`
