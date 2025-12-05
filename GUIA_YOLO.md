# Guía de Uso de YOLOv8 en el Sistema de Análisis de Microplásticos

## 🤖 ¿Qué es YOLOv8?

YOLOv8 (You Only Look Once version 8) es un modelo de inteligencia artificial de última generación para detección de objetos en imágenes. A diferencia del método tradicional de procesamiento de imágenes, YOLOv8 puede:

- **Detectar automáticamente** microplásticos en imágenes sin necesidad de ajustar umbrales manualmente
- **Clasificar tipos** de microplásticos (fibra, fragmento, película, esfera, etc.)
- **Aprender de ejemplos** anotados para mejorar con el tiempo
- **Ser más preciso** en condiciones de iluminación variables

## 📋 Flujo de Trabajo Completo

### 1. Anotar Imágenes con LabelImg

Primero debes etiquetar tus imágenes manualmente para entrenar el modelo:

1. **Carga tus imágenes** en la pestaña "⚙️ Configuración"
2. **Ve a la pestaña "🏷️ Anotar Imágenes"**
3. **Haz clic en "Abrir LabelImg"**
4. **En LabelImg:**
   - Presiona `W` para crear un rectángulo
   - Dibuja alrededor de cada microplástico
   - Selecciona la clase correcta (fibra, fragmento, etc.)
   - Presiona `Ctrl+S` para guardar
   - Presiona `D` para pasar a la siguiente imagen

**Recomendación:** Anota al menos 50-100 imágenes para un buen modelo. Más imágenes = mejor precisión.

### 2. Entrenar el Modelo YOLOv8

Una vez que tengas imágenes anotadas:

#### Opción A: Desde la Interfaz Gráfica

1. **Ve a la pestaña "🤖 Entrenar YOLOv8"**
2. **Configura los parámetros:**
   - **Tamaño del modelo:** 
     - `n` (nano): Más rápido, menos preciso - ideal para pruebas
     - `s` (small): Balance bueno
     - `m` (medium): Recomendado para uso general
     - `l` (large): Más preciso, más lento
     - `x` (xlarge): Máxima precisión, requiere GPU potente
   
   - **Épocas:** 100-300 (cuánto tiempo entrenar)
     - Menos imágenes → menos épocas (50-100)
     - Más imágenes → más épocas (200-300)
   
   - **Batch size:** 8-32
     - GPU pequeña → 8
     - GPU media → 16
     - GPU grande → 32
     - Sin GPU (CPU) → 4-8

3. **Haz clic en "🚀 Entrenar Modelo YOLO"**
4. **Espera** (puede tomar de 30 minutos a varias horas)
5. **El modelo se guardará** en `yolo_training/models/`

#### Opción B: Desde Línea de Comandos

```bash
# Entrenamiento rápido (modelo nano)
python entrenar_yolo.py

# O usando src/train_yolo.py directamente con opciones avanzadas
python src/train_yolo.py --model-size m --epochs 200 --batch 16
```

Parámetros disponibles:
```bash
--annotations     # Directorio con XMLs (default: data/raw_images)
--images          # Directorio con imágenes (default: data/raw_images)
--output          # Directorio de salida (default: yolo_training)
--model-size      # Tamaño: n, s, m, l, x (default: n)
--epochs          # Número de épocas (default: 100)
--batch           # Tamaño del batch (default: 16)
--imgsz           # Tamaño de imagen (default: 640)
--device          # 0 para GPU, cpu para CPU (default: 0)
```

### 3. Usar el Modelo Entrenado

#### En la Interfaz Gráfica:

1. **Ve a la pestaña "🤖 Entrenar YOLOv8"**
2. **Marca "✅ Usar YOLOv8 para análisis"**
3. **Haz clic en "📁 Buscar"** y selecciona tu modelo entrenado (.pt)
   - Busca en: `yolo_training/models/microplasticos/yolov8/weights/best.pt`
4. **Ve a la pestaña "🔬 Análisis"**
5. **Haz clic en "▶️ Iniciar Análisis"**

El análisis ahora usará YOLOv8 en lugar de detección tradicional.

#### En Código Python:

```python
from src.yolo_detector import YOLODetector
import cv2

# Cargar modelo
detector = YOLODetector(
    model_path="yolo_training/models/microplasticos/yolov8/weights/best.pt",
    pixels_to_um=0.5,  # Tu factor de calibración
    confidence_threshold=0.25  # Confianza mínima (0-1)
)

# Cargar imagen
image = cv2.imread("data/raw_images/muestra.jpg")

# Detectar microplásticos
particles, annotated_image = detector.detect_particles(image)

# Ver resultados
print(f"Detectadas {len(particles)} partículas")

for p in particles:
    print(f"  - {p['class_name']}: {p['area_um2']:.2f} µm² (confianza: {p['confidence']:.2f})")

# Guardar imagen anotada
cv2.imwrite("resultado.jpg", annotated_image)

# Obtener resumen
summary = detector.get_detection_summary(particles)
print(f"\nResumen: {summary}")
```

## 🔧 Configuración Avanzada

### Ajustar Umbrales de Confianza

Si el modelo detecta demasiados falsos positivos:

```python
detector = YOLODetector(
    model_path="tu_modelo.pt",
    confidence_threshold=0.5,  # Aumenta esto (0.25 → 0.5)
    iou_threshold=0.45         # Umbral de superposición
)
```

### Entrenar con Datos Balanceados

Asegúrate de tener ejemplos de todas las clases:

```python
from src.image_annotation import ImageAnnotator

annotator = ImageAnnotator("data/raw_images")
stats = annotator.get_annotation_stats()

print("Distribución de clases:")
for clase, count in stats['classes'].items():
    print(f"  {clase}: {count}")
```

**Recomendación:** Cada clase debe tener al menos 20-30 ejemplos.

### Aumentar Datos (Data Augmentation)

YOLOv8 hace esto automáticamente durante el entrenamiento:
- Rotación
- Zoom
- Cambios de brillo/contraste
- Flip horizontal/vertical

## 📊 Evaluación del Modelo

Después del entrenamiento, YOLOv8 genera métricas:

- **mAP50:** Precisión promedio con IoU=0.5
- **mAP50-95:** Precisión promedio con IoU de 0.5 a 0.95
- **Precisión:** Porcentaje de detecciones correctas
- **Recall:** Porcentaje de objetos detectados

**Valores buenos:**
- mAP50 > 0.7 → Excelente
- mAP50 > 0.5 → Bueno
- mAP50 < 0.3 → Necesita más entrenamiento o más datos

## 🐛 Solución de Problemas

### Error: "ultralytics no está instalado"

```bash
pip install ultralytics torch torchvision
```

### Error: GPU no detectada

El entrenamiento usará CPU automáticamente (será más lento).

Para usar GPU:
1. Verifica que tienes una GPU NVIDIA
2. Instala CUDA: https://developer.nvidia.com/cuda-downloads
3. Instala PyTorch con soporte CUDA:
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

### Modelo no detecta nada

1. **Verifica las anotaciones:** Asegúrate de tener archivos XML en `data/raw_images/`
2. **Entrena más tiempo:** Aumenta el número de épocas
3. **Baja el umbral de confianza:**
   ```python
   detector = YOLODetector(model_path="...", confidence_threshold=0.15)
   ```
4. **Añade más datos:** Anota más imágenes

### Demasiados falsos positivos

1. **Sube el umbral de confianza:**
   ```python
   detector = YOLODetector(model_path="...", confidence_threshold=0.5)
   ```
2. **Limpia las anotaciones:** Elimina anotaciones incorrectas
3. **Re-entrena** con datos más limpios

## 💡 Consejos Avanzados

### Usar Transfer Learning

YOLOv8 ya usa transfer learning automáticamente al partir de modelos pre-entrenados en COCO dataset.

### Exportar para Deployment

```python
from src.train_yolo import YOLOTrainer

trainer = YOLOTrainer(...)
# Exportar a ONNX (más rápido para inferencia)
trainer.export_model("modelo.pt", format='onnx')
```

### Fine-tuning

Si ya tienes un modelo entrenado y quieres mejorarlo:

1. Anota más imágenes (especialmente de casos difíciles)
2. Entrena de nuevo usando tu modelo como punto de partida:
   ```python
   from ultralytics import YOLO
   
   model = YOLO("tu_modelo_anterior.pt")  # Partir de modelo previo
   model.train(data="data.yaml", epochs=50)  # Entrenar más
   ```

## 📚 Recursos Adicionales

- **Documentación Ultralytics:** https://docs.ultralytics.com/
- **Tutorial YOLOv8:** https://github.com/ultralytics/ultralytics
- **Paper original YOLO:** https://arxiv.org/abs/1506.02640

## 🎯 Comparación: YOLOv8 vs Tradicional

| Aspecto | Tradicional | YOLOv8 |
|---------|-------------|---------|
| **Setup** | Listo para usar | Requiere entrenamiento |
| **Precisión** | Depende de parámetros | Alta con datos suficientes |
| **Velocidad** | Rápido | Rápido (con GPU) |
| **Clasificación** | No clasifica tipos | Clasifica automáticamente |
| **Adaptabilidad** | Requiere ajuste manual | Aprende automáticamente |
| **Recomendado para** | Pruebas rápidas | Producción/Análisis serio |

## ✅ Checklist de Implementación

- [ ] Anotar al menos 50-100 imágenes con LabelImg
- [ ] Verificar distribución balanceada de clases
- [ ] Entrenar modelo YOLOv8 (empezar con 'n', luego 'm')
- [ ] Evaluar métricas (mAP > 0.5)
- [ ] Probar con imágenes de prueba
- [ ] Ajustar umbrales si es necesario
- [ ] Activar YOLOv8 en la GUI
- [ ] Analizar muestras reales
- [ ] Comparar resultados con método tradicional
- [ ] Iterar: más datos → re-entrenar → evaluar

¡Éxito con tu análisis de microplásticos! 🎉
