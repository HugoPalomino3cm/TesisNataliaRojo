"""
Script de ejemplo para entrenar YOLOv8 desde línea de comandos.

Uso:
    python entrenar_yolo.py

Esto entrenará un modelo YOLOv8 usando las anotaciones de LabelImg
que se encuentran en data/raw_images/
"""

import sys
from pathlib import Path

# Agregar directorio src al path
sys.path.append(str(Path(__file__).parent))

from src.train_yolo import YOLOTrainer

def main():
    print("\n" + "="*60)
    print("  ENTRENAMIENTO DE YOLOv8 PARA MICROPLÁSTICOS")
    print("="*60 + "\n")
    
    # Configuración
    annotations_dir = "data/raw_images"  # Donde están los XML
    images_dir = "data/raw_images"        # Donde están las imágenes
    output_dir = "yolo_training"          # Donde guardar todo
    
    print(f"📂 Directorio de anotaciones: {annotations_dir}")
    print(f"📂 Directorio de imágenes: {images_dir}")
    print(f"📂 Directorio de salida: {output_dir}\n")
    
    # Crear entrenador
    print("🔧 Inicializando entrenador...")
    trainer = YOLOTrainer(
        annotations_dir=annotations_dir,
        images_dir=images_dir,
        output_dir=output_dir
    )
    
    # Convertir dataset
    print("\n📋 Convirtiendo anotaciones VOC a YOLO...")
    data_yaml = trainer.convert_voc_to_yolo(
        train_split=0.8,   # 80% para entrenamiento
        val_split=0.15     # 15% para validación, 5% para prueba
    )
    
    # Entrenar modelo
    print("\n🚀 Iniciando entrenamiento...")
    print("\n⚠️ NOTA: Este proceso puede tomar varias horas")
    print("   dependiendo de tu hardware y cantidad de datos.\n")
    
    input("Presiona ENTER para continuar o Ctrl+C para cancelar...")
    
    best_model = trainer.train_model(
        data_yaml=data_yaml,
        model_size='n',      # nano (más rápido) - usa 's', 'm', 'l', 'x' para más precisión
        epochs=100,          # Puedes aumentar a 200-300 para mejor resultado
        batch=2,             # Reducido para ahorrar memoria (antes: 16)
        imgsz=416,           # Reducido para ahorrar memoria (antes: 640)
        device='cpu',        # Usar CPU para evitar errores de VRAM (cambia a '0' si tienes GPU potente)
        patience=50          # Early stopping si no mejora en 50 épocas
    )
    
    # Evaluar modelo
    print("\n📊 Evaluando modelo...")
    trainer.evaluate_model(best_model, data_yaml)
    
    # Exportar a ONNX (opcional - para deployment)
    print("\n📤 ¿Deseas exportar el modelo a ONNX? (s/n)")
    respuesta = input("> ").lower()
    
    if respuesta == 's':
        print("Exportando a ONNX...")
        trainer.export_model(best_model, format='onnx')
    
    print("\n" + "="*60)
    print("  ✅ ENTRENAMIENTO COMPLETADO")
    print("="*60)
    print(f"\n📦 Modelo guardado en: {best_model}")
    print(f"\n💡 Para usar el modelo:")
    print(f"   1. Abre la aplicación: python main.py")
    print(f"   2. Ve a la pestaña 'Entrenar YOLOv8'")
    print(f"   3. Marca 'Usar YOLOv8 para análisis'")
    print(f"   4. Carga el modelo: {best_model}")
    print(f"   5. Ve a 'Análisis' y procesa tus imágenes\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Entrenamiento cancelado por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
