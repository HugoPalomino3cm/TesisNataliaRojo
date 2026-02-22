"""
Interfaz Gráfica para Análisis de Microplásticos
================================================

Esta versión del programa incluye una interfaz gráfica amigable
usando tkinter para facilitar el uso del sistema.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import sys
import subprocess
from pathlib import Path
import queue
from PIL import Image, ImageTk

# Agregar directorio src al path
sys.path.append(str(Path(__file__).parent))

from src.image_processing import ImageProcessor
from src.statistical_analysis import StatisticalAnalyzer
from src.visualization import DataVisualizer
from src.image_annotation import ImageAnnotator, launch_labelimg_standalone
from config.config import (
    RAW_IMAGES_DIR, ANALYSIS_IMAGES_DIR, PROCESSED_IMAGES_DIR, 
    ANNOTATIONS_DIR, GRAPHS_DIR, REPORTS_DIR, IMAGE_PARAMS
)


class MicroplasticAnalysisGUI:
    """Interfaz gráfica para el análisis de microplásticos."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Microplásticos en Máscaras de Pestañas")
        self.root.geometry("1000x750")
        self.root.resizable(True, True)
        self.root.configure(bg='#f5f7fa')
        
        # Variables
        self.pixels_to_um = tk.DoubleVar(value=IMAGE_PARAMS['pixels_to_um'])
        self.image_files = []
        self.analysis_running = False
        self.message_queue = queue.Queue()
        
        # Variables para YOLOv8
        self.yolo_model_path = tk.StringVar(value="")
        self.yolo_epochs = tk.IntVar(value=30)
        self.yolo_batch = tk.IntVar(value=2)
        self.yolo_model_size = tk.StringVar(value='n')
        self.yolo_imgsz = tk.IntVar(value=320)
        
        # Inicializar anotador de imágenes
        self.annotator = ImageAnnotator(RAW_IMAGES_DIR)
        
        # Crear interfaz
        self.create_widgets()
        
        # Verificar cola de mensajes
        self.root.after(100, self.check_message_queue)
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz."""
        
        # Título con gradiente visual
        title_frame = tk.Frame(self.root, bg="#047857", height=180)
        title_frame.pack(fill=tk.X, padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        # Borde inferior decorativo
        border_frame = tk.Frame(self.root, bg="#065f46", height=3)
        border_frame.pack(fill=tk.X)
        
        # Frame horizontal para logo y texto - centrado y con fill
        content_frame = tk.Frame(title_frame, bg="#047857")
        content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Intentar cargar logo
        try:
            # Buscar logo en múltiples formatos
            logo_path = None
            for ext in ['png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG']:
                test_path = Path(__file__).parent / f"logo_pucv.{ext}"
                if test_path.exists():
                    logo_path = test_path
                    break
            
            if logo_path:
                logo_image = Image.open(logo_path)
                # Redimensionar manteniendo proporción
                logo_image.thumbnail((300, 300), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_image)
                
                logo_label = tk.Label(
                    content_frame,
                    image=self.logo_photo,
                    bg="#047857",
                    relief=tk.FLAT
                )
                logo_label.pack(side=tk.LEFT, padx=25)
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")
        
        # Frame para texto
        text_frame = tk.Frame(content_frame, bg="#047857")
        text_frame.pack(side=tk.LEFT, padx=15)
        
        title_label = tk.Label(
            text_frame,
            text="🔬 Análisis de Microplásticos en Máscaras",
            font=("Segoe UI", 22, "bold"),
            bg="#047857",
            fg="#ffffff"
        )
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(
            text_frame,
            text="Sistema de Detección y Caracterización Morfológica",
            font=("Segoe UI", 12, "bold"),
            bg="#047857",
            fg="#d1fae5"
        )
        subtitle_label.pack(anchor=tk.W, pady=(3, 8))
        
        # Marca de agua con el nombre
        watermark_label = tk.Label(
            text_frame,
            text="✦ Desarrollado por: Natalia Rojo",
            font=("Segoe UI", 11, "italic"),
            bg="#047857",
            fg="#a7f3d0"
        )
        watermark_label.pack(anchor=tk.W)
        
        # Frame principal con pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=(10, 15))
        
        # Pestaña 1: Configuración
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="⚙️ Configuración")
        self.create_config_tab(config_frame)
        
        # Pestaña 2: Anotación de Imágenes
        annotation_frame = ttk.Frame(self.notebook)
        self.notebook.add(annotation_frame, text="🏷️ Anotar Imágenes")
        self.create_annotation_tab(annotation_frame)
        
        # Pestaña 3: Entrenamiento YOLO
        yolo_frame = ttk.Frame(self.notebook)
        self.notebook.add(yolo_frame, text="🤖 Entrenar YOLOv8")
        self.create_yolo_training_tab(yolo_frame)
        
        # Pestaña 4: Análisis
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text="🔬 Análisis")
        self.create_analysis_tab(analysis_frame)
        
        # Pestaña 5: Visualización de Gráficos
        viewer_frame = ttk.Frame(self.notebook)
        self.notebook.add(viewer_frame, text="📊 Ver Gráficos")
        self.create_viewer_tab(viewer_frame)
        
        # Pestaña 6: Gestión
        management_frame = ttk.Frame(self.notebook)
        self.notebook.add(management_frame, text="📁 Gestión de Resultados")
        self.create_management_tab(management_frame)
    
    def create_config_tab(self, parent):
        """Crea la pestaña de configuración."""
        
        # Frame de imágenes
        img_frame = ttk.LabelFrame(parent, text="📸 Cargar y Anotar Imágenes", padding=15)
        img_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Mensaje informativo
        info_label = tk.Label(
            img_frame,
            text="⚠️ Las imágenes cargadas se abrirán automáticamente en LabelImg para su anotación",
            font=("Segoe UI", 9, "italic"),
            fg="#d97706",
            bg="#fef3c7",
            padx=10,
            pady=8,
            relief=tk.FLAT
        )
        info_label.pack(fill=tk.X, pady=(0, 10))
        
        # Frame de botones
        btn_frame = ttk.Frame(img_frame)
        btn_frame.pack(pady=10)
        
        # Botón para buscar imágenes
        btn_browse = ttk.Button(
            btn_frame,
            text="📤 Cargar Imágenes para Anotar",
            command=self.browse_images
        )
        btn_browse.pack(side=tk.LEFT, padx=5)
        
        # Botón para eliminar imágenes seleccionadas
        btn_remove = ttk.Button(
            btn_frame,
            text="🗑️ Eliminar Seleccionadas",
            command=self.remove_selected_images
        )
        btn_remove.pack(side=tk.LEFT, padx=5)
        
        # Botón para limpiar todas
        btn_clear = ttk.Button(
            btn_frame,
            text="✖️ Limpiar Todas",
            command=self.clear_all_images
        )
        btn_clear.pack(side=tk.LEFT, padx=5)
        
        # Lista de imágenes
        list_frame = ttk.Frame(img_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.image_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            height=8,
            font=("Segoe UI", 10),
            selectmode=tk.EXTENDED,  # Permitir selección múltiple
            bg="#ffffff",
            fg="#2c3e50",
            selectbackground="#047857",  # Verde moderno
            selectforeground="#ffffff",
            activestyle="none",  # Sin estilo de activación por defecto
            highlightthickness=1,
            highlightcolor="#047857",
            highlightbackground="#e0e0e0",
            borderwidth=0,
            relief=tk.FLAT
        )
        self.image_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.image_listbox.yview)
        
        # Botón para usar directorio por defecto
        btn_default = ttk.Button(
            img_frame,
            text="📁 Cargar Imágenes para Analizar (data/analysis_images)",
            command=self.load_default_images
        )
        btn_default.pack(pady=5)
        
        # Frame de calibración
        calib_frame = ttk.LabelFrame(parent, text="📏 Calibración del Microscopio", padding=15)
        calib_frame.pack(fill=tk.X, padx=10, pady=10)
        
        calib_info = tk.Label(
            calib_frame,
            text="Factor de conversión: píxeles → micrómetros (μm)\n"
                 "Este valor depende de tu microscopio y magnificación.",
            justify=tk.LEFT,
            font=("Arial", 9)
        )
        calib_info.pack(anchor=tk.W, pady=5)
        
        calib_input_frame = ttk.Frame(calib_frame)
        calib_input_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(calib_input_frame, text="Factor (μm/píxel):", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        calib_entry = ttk.Entry(
            calib_input_frame,
            textvariable=self.pixels_to_um,
            width=15,
            font=("Arial", 11)
        )
        calib_entry.pack(side=tk.LEFT, padx=5)
        
        # Valores sugeridos
        suggest_frame = ttk.LabelFrame(calib_frame, text="💡 Valores Típicos por Magnificación", padding=10)
        suggest_frame.pack(fill=tk.X, pady=10)
        
        suggestions = [
            ("4x", "2.5 - 5.0"),
            ("10x", "1.0 - 2.0"),
            ("20x", "0.3 - 0.8"),
            ("40x", "0.15 - 0.4"),
            ("100x", "0.06 - 0.15")
        ]
        
        for mag, value in suggestions:
            row = ttk.Frame(suggest_frame)
            row.pack(fill=tk.X, pady=2)
            ttk.Label(row, text=f"{mag}:", width=8).pack(side=tk.LEFT)
            ttk.Label(row, text=f"{value} μm/píxel", foreground="blue").pack(side=tk.LEFT)
        
        # Cargar imágenes por defecto al inicio
        self.root.after(500, self.load_default_images)
    
    def create_analysis_tab(self, parent):
        """Crea la pestaña de análisis."""
        
        # Frame de control
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Botón de inicio
        self.btn_start = ttk.Button(
            control_frame,
            text="▶️ Iniciar Análisis",
            command=self.start_analysis,
            style="Accent.TButton"
        )
        self.btn_start.pack(side=tk.LEFT, padx=5)
        
        # Botón de detener
        self.btn_stop = ttk.Button(
            control_frame,
            text="⏹️ Detener",
            command=self.stop_analysis,
            state=tk.DISABLED
        )
        self.btn_stop.pack(side=tk.LEFT, padx=5)
        
        # Botón de limpiar consola
        btn_clear = ttk.Button(
            control_frame,
            text="🗑️ Limpiar Consola",
            command=self.clear_console
        )
        btn_clear.pack(side=tk.LEFT, padx=5)
        
        # Barra de progreso
        progress_frame = ttk.Frame(parent)
        progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(progress_frame, text="Progreso:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        self.progress = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(fill=tk.X, pady=5)
        
        # Console de salida
        console_frame = ttk.LabelFrame(parent, text="📋 Salida del Análisis", padding=10)
        console_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.console = scrolledtext.ScrolledText(
            console_frame,
            wrap=tk.WORD,
            font=("Courier", 9),
            bg="#1e1e1e",
            fg="#00ff00",
            height=20
        )
        self.console.pack(fill=tk.BOTH, expand=True)
        
        # Botones de resultados
        results_frame = ttk.Frame(parent)
        results_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            results_frame,
            text="📊 Abrir Carpeta de Gráficos",
            command=lambda: self.open_folder(GRAPHS_DIR)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            results_frame,
            text="📄 Abrir Carpeta de Reportes",
            command=lambda: self.open_folder(REPORTS_DIR)
        ).pack(side=tk.LEFT, padx=5)
    
    def create_annotation_tab(self, parent):
        """Crea la pestaña de anotación de imágenes con LabelImg."""
        
        # Banner de instrucciones destacado
        banner_frame = tk.Frame(parent, bg="#047857", height=80)
        banner_frame.pack(fill=tk.X, padx=0, pady=0)
        banner_frame.pack_propagate(False)
        
        banner_text = tk.Label(
            banner_frame,
            text="🏷️ ANOTAR IMÁGENES CON LABELIMG\n"
                 "Las imágenes cargadas deben ser anotadas antes del análisis",
            font=("Segoe UI", 12, "bold"),
            bg="#047857",
            fg="#ffffff",
            justify=tk.CENTER
        )
        banner_text.pack(expand=True)
        
        # Frame de acciones principales (más destacado)
        action_frame = ttk.LabelFrame(parent, text="🚀 Comenzar Anotación", padding=20)
        action_frame.pack(fill=tk.X, padx=10, pady=15)
        
        # Botón principal GRANDE para abrir LabelImg
        btn_launch = tk.Button(
            action_frame,
            text="🏷️ ABRIR LABELIMG PARA ANOTAR",
            command=self.launch_labelimg,
            font=("Segoe UI", 12, "bold"),
            bg="#047857",
            fg="#ffffff",
            activebackground="#065f46",
            activeforeground="#ffffff",
            relief=tk.RAISED,
            borderwidth=3,
            padx=30,
            pady=15,
            cursor="hand2"
        )
        btn_launch.pack(pady=10)
        
        # Información rápida de uso
        quick_info = tk.Label(
            action_frame,
            text="⌨️ Atajos: W = Nueva caja | Ctrl+S = Guardar | D/A = Navegar",
            font=("Segoe UI", 9, "italic"),
            fg="#6b7280"
        )
        quick_info.pack(pady=5)
        
        # Frame de información de directorios
        dirs_frame = ttk.Frame(action_frame)
        dirs_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            dirs_frame,
            text=f"📂 Imágenes: {RAW_IMAGES_DIR}",
            font=("Segoe UI", 9)
        ).pack(anchor=tk.W, pady=2)
        
        annotations_dir = self.annotator.annotations_dir
        ttk.Label(
            dirs_frame,
            text=f"📝 Anotaciones: {annotations_dir}",
            font=("Segoe UI", 9)
        ).pack(anchor=tk.W, pady=2)
        
        # Frame de información desplegable
        info_frame = ttk.LabelFrame(parent, text="ℹ️ Información sobre Anotación", padding=15)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        info_text = (
            "📌 Funcionalidades de LabelImg:\n"
            "  • Dibujar cajas delimitadoras alrededor de microplásticos\n"
            "  • Clasificar partículas por tipo\n"
            "  • Guardar anotaciones en formato XML\n\n"
            "🎯 Clases predefinidas:\n"
            "  • fibra: Microplásticos filamentosos\n"
            "  • fragmento: Pedazos irregulares\n"
            "  • pelicula: Láminas delgadas\n"
            "  • esfera: Partículas esféricas\n"
            "  • microplastico_irregular: Formas no clasificables\n"
            "  • aglomerado: Conjunto de partículas"
        )
        
        info_label = tk.Label(
            info_frame,
            text=info_text,
            justify=tk.LEFT,
            font=("Segoe UI", 9),
            bg="#f8f9fa",
            fg="#2c3e50"
        )
        info_label.pack(fill=tk.BOTH)
        
        # Frame de estadísticas
        stats_frame = ttk.LabelFrame(parent, text="📊 Estadísticas de Anotación", padding=15)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Área de texto para mostrar estadísticas
        self.annotation_stats_text = scrolledtext.ScrolledText(
            stats_frame,
            height=10,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#ffffff",
            fg="#2c3e50"
        )
        self.annotation_stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Botones de utilidades
        utils_frame = ttk.Frame(stats_frame)
        utils_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            utils_frame,
            text="🔄 Actualizar Estadísticas",
            command=self.update_annotation_stats
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            utils_frame,
            text="📁 Abrir Carpeta de Anotaciones",
            command=lambda: self.open_folder(self.annotator.annotations_dir)
        ).pack(side=tk.LEFT, padx=5)
        
        # Botón alternativo usando VBScript (más confiable)
        ttk.Button(
            utils_frame,
            text="🔧 Abrir LabelImg (Método Alternativo)",
            command=self.launch_labelimg_vbs
        ).pack(side=tk.LEFT, padx=5)
        
        # Cargar estadísticas iniciales
        self.root.after(1000, self.update_annotation_stats)
    
    def launch_labelimg(self):
        """Lanza la herramienta LabelImg."""
        try:
            if self.annotator.launch_labelimg():
                self.log_console("✅ LabelImg lanzado exitosamente\n")
                self.log_console("   Cierre LabelImg cuando termine de anotar\n")
            else:
                self.log_console("❌ No se pudo lanzar LabelImg\n")
        except Exception as e:
            self.log_console(f"❌ Error al lanzar LabelImg: {e}\n")
            messagebox.showerror("Error", f"Error al lanzar LabelImg:\n{str(e)}")
    
    def launch_labelimg_vbs(self):
        """Lanza LabelImg usando VBScript (método alternativo más confiable)."""
        try:
            vbs_file = Path(__file__).parent / "abrir_labelimg.vbs"
            if vbs_file.exists():
                subprocess.Popen(['cscript', '//nologo', str(vbs_file)])
                self.log_console("✅ LabelImg lanzado (método VBScript)\n")
                self.log_console("   Cierre LabelImg cuando termine de anotar\n")
            else:
                self.log_console("❌ No se encontró abrir_labelimg.vbs\n")
                messagebox.showerror("Error", f"No se encontró el archivo:\n{vbs_file}")
        except Exception as e:
            self.log_console(f"❌ Error: {e}\n")
            messagebox.showerror("Error", f"Error al lanzar LabelImg:\n{str(e)}")
    
    def update_annotation_stats(self):
        """Actualiza las estadísticas de anotación."""
        try:
            stats = self.annotator.get_annotation_stats()
            
            # Limpiar texto
            self.annotation_stats_text.delete(1.0, tk.END)
            
            # Insertar estadísticas
            self.annotation_stats_text.insert(tk.END, "═" * 60 + "\n")
            self.annotation_stats_text.insert(tk.END, "  RESUMEN DE ANOTACIONES\n")
            self.annotation_stats_text.insert(tk.END, "═" * 60 + "\n\n")
            
            self.annotation_stats_text.insert(tk.END, f"📷 Imágenes anotadas: {stats['total_images']}\n")
            self.annotation_stats_text.insert(tk.END, f"🎯 Total de objetos etiquetados: {stats['total_objects']}\n\n")
            
            if stats['classes']:
                self.annotation_stats_text.insert(tk.END, "─" * 60 + "\n")
                self.annotation_stats_text.insert(tk.END, "  DISTRIBUCIÓN POR CLASE\n")
                self.annotation_stats_text.insert(tk.END, "─" * 60 + "\n\n")
                
                for clase, count in sorted(stats['classes'].items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / stats['total_objects'] * 100) if stats['total_objects'] > 0 else 0
                    self.annotation_stats_text.insert(
                        tk.END,
                        f"  {clase:30s} : {count:4d} ({percentage:5.1f}%)\n"
                    )
            else:
                self.annotation_stats_text.insert(tk.END, "\n⚠️ No hay anotaciones disponibles todavía.\n")
                self.annotation_stats_text.insert(tk.END, "   Haga clic en 'Abrir LabelImg' para comenzar.\n")
            
            self.annotation_stats_text.insert(tk.END, "\n" + "═" * 60 + "\n")
            
        except Exception as e:
            self.annotation_stats_text.delete(1.0, tk.END)
            self.annotation_stats_text.insert(tk.END, f"❌ Error al obtener estadísticas:\n{str(e)}")
    
    def create_yolo_training_tab(self, parent):
        """Crea la pestaña de entrenamiento YOLOv8."""
        
        # Frame de información
        info_frame = ttk.LabelFrame(parent, text="ℹ️ ¿Qué es el Entrenamiento de YOLOv8?", padding=15)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        info_text = tk.Text(info_frame, height=10, wrap=tk.WORD, font=("Segoe UI", 9))
        info_text.pack(fill=tk.X)
        info_text.insert(tk.END,
            "YOLOv8 es una red neuronal que aprende a detectar microplásticos automáticamente.\n\n"
            
            "📚 ÉPOCAS: Cuántas veces el modelo ve todas tus imágenes\n"
            "   • 1 época = ve todas las imágenes 1 vez\n"
            "   • 100 épocas = ve todas las imágenes 100 veces (aprende mejor)\n"
            "   • Más épocas = más aprendizaje (pero toma más tiempo)\n\n"
            
            "📦 BATCH SIZE: Cuántas imágenes procesa a la vez\n"
            "   • Batch 8 = procesa 8 imágenes juntas (GPU pequeña)\n"
            "   • Batch 16 = procesa 16 imágenes (recomendado)\n"
            "   • Batch 32 = procesa 32 imágenes (GPU grande)\n"
            "   • Más batch = más rápido PERO necesita más memoria\n\n"
            
            "🏗️ TAMAÑO MODELO: Qué tan 'inteligente' es\n"
            "   • n (nano) = rápido pero básico\n"
            "   • m (medium) = BALANCE PERFECTO ⭐\n"
            "   • x (xlarge) = súper preciso pero lento\n\n"
            
            "⏱️ TIEMPO: Depende de tus imágenes y configuración\n"
            "   • 50 imgs + modelo 'n' + 100 épocas ≈ 20 minutos\n"
            "   • 100 imgs + modelo 'm' + 150 épocas ≈ 1-2 horas\n"
            "   • 200 imgs + modelo 'x' + 200 épocas ≈ 4-6 horas"
        )
        info_text.config(state=tk.DISABLED, bg="#f0f8ff")
        
        # Frame de configuración de entrenamiento
        train_frame = ttk.LabelFrame(parent, text="🚀 Configuración de Entrenamiento", padding=15)
        train_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Tamaño del modelo
        size_frame = ttk.Frame(train_frame)
        size_frame.pack(fill=tk.X, pady=5)
        ttk.Label(size_frame, text="Tamaño del modelo (cerebro de la IA):", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        model_sizes = [
            ('n (nano - más rápido, ~15min)', 'n'),
            ('s (small - rápido)', 's'),
            ('m (medium - RECOMENDADO)', 'm'),
            ('l (large - más preciso)', 'l'),
            ('x (xlarge - máxima precisión, ~4hrs)', 'x')
        ]
        for text, value in model_sizes:
            ttk.Radiobutton(
                size_frame,
                text=text,
                variable=self.yolo_model_size,
                value=value
            ).pack(side=tk.LEFT, padx=5)
        
        # Épocas
        epoch_frame = ttk.Frame(train_frame)
        epoch_frame.pack(fill=tk.X, pady=5)
        ttk.Label(epoch_frame, text="Épocas (cuántas veces ve todas las imágenes):", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        ttk.Entry(epoch_frame, textvariable=self.yolo_epochs, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Label(epoch_frame, text="(100-200 recomendado. Más épocas = mejor aprendizaje)", foreground="gray").pack(side=tk.LEFT)
        
        # Batch size
        batch_frame = ttk.Frame(train_frame)
        batch_frame.pack(fill=tk.X, pady=5)
        ttk.Label(batch_frame, text="Batch (imágenes por lote):", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        ttk.Entry(batch_frame, textvariable=self.yolo_batch, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Label(batch_frame, text="(2=poca RAM | 4=normal | 8-16=mucha RAM) ⚠️ Usar 2 para evitar errores", foreground="gray").pack(side=tk.LEFT)
        
        # Tamaño de imagen
        imgsz_frame = ttk.Frame(train_frame)
        imgsz_frame.pack(fill=tk.X, pady=5)
        ttk.Label(imgsz_frame, text="Tamaño imagen (píxeles):", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        ttk.Entry(imgsz_frame, textvariable=self.yolo_imgsz, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Label(imgsz_frame, text="(320=rápido/poca RAM | 416=balance | 640=lento/preciso)", foreground="gray").pack(side=tk.LEFT)
        
        # Botones de entrenamiento
        btn_frame = ttk.Frame(train_frame)
        btn_frame.pack(pady=15)
        
        ttk.Button(
            btn_frame,
            text="🚀 Entrenar Modelo YOLO",
            command=self.start_yolo_training
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="📂 Abrir Carpeta de Modelos",
            command=lambda: self.open_folder("yolo_training/models")
        ).pack(side=tk.LEFT, padx=5)
        
        # Frame de selección de modelo para uso
        use_frame = ttk.LabelFrame(parent, text="🤖 Seleccionar Modelo YOLO", padding=15)
        use_frame.pack(fill=tk.X, padx=10, pady=10)
        
        info_label = tk.Label(
            use_frame,
            text="⚠️ IMPORTANTE: Debes seleccionar un modelo entrenado (.pt) para usar el sistema",
            font=("Segoe UI", 9, "bold"),
            fg="#dc2626",
            bg="#fee2e2",
            padx=10,
            pady=8
        )
        info_label.pack(fill=tk.X, pady=(0, 10))
        
        # Selector de modelo
        model_select_frame = ttk.Frame(use_frame)
        model_select_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(model_select_frame, text="Modelo entrenado (.pt):", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        ttk.Entry(model_select_frame, textvariable=self.yolo_model_path, width=50, font=("Arial", 10)).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(
            model_select_frame,
            text="📁 Buscar Modelo",
            command=self.browse_yolo_model
        ).pack(side=tk.LEFT, padx=5)
        
        # Consola de entrenamiento
        console_frame = ttk.LabelFrame(parent, text="📋 Log de Entrenamiento", padding=10)
        console_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Barra de progreso visual
        progress_frame = ttk.Frame(console_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(progress_frame, text="Progreso:", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)
        self.yolo_progress = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            length=300
        )
        self.yolo_progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.yolo_progress_label = ttk.Label(progress_frame, text="Esperando...", font=("Arial", 9))
        self.yolo_progress_label.pack(side=tk.LEFT, padx=5)
        
        self.yolo_console = scrolledtext.ScrolledText(
            console_frame,
            height=12,
            font=("Consolas", 9),
            bg="#1e1e1e",
            fg="#00ff00",
            insertbackground="white"
        )
        self.yolo_console.pack(fill=tk.BOTH, expand=True)
    
    def browse_yolo_model(self):
        """Busca un modelo YOLO entrenado."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar modelo YOLO entrenado",
            filetypes=[("Modelos PyTorch", "*.pt"), ("Todos los archivos", "*.*")],
            initialdir="yolo_training/models"
        )
        
        if file_path:
            self.yolo_model_path.set(file_path)
            self.log_yolo(f"✅ Modelo seleccionado: {Path(file_path).name}\n")
            self.log_yolo(f"   Ruta: {file_path}\n")
            self.log_yolo(f"   Ahora puedes ir a 'Análisis' para procesar imágenes\n\n")
            messagebox.showinfo(
                "Modelo Seleccionado",
                f"Modelo YOLOv8 configurado correctamente:\n\n"
                f"{Path(file_path).name}\n\n"
                f"Ve a la pestaña 'Análisis' para procesar imágenes."
            )
    
    def start_yolo_training(self):
        """Inicia el entrenamiento de YOLO en un hilo separado."""
        if self.analysis_running:
            messagebox.showwarning("Advertencia", "Ya hay un proceso en ejecución.")
            return
        
        # Verificar que hay anotaciones
        stats = self.annotator.get_annotation_stats()
        if stats['total_images'] == 0:
            messagebox.showerror(
                "Error",
                "No hay imágenes anotadas.\n\n"
                "Ve a la pestaña 'Anotar Imágenes' y anota algunas imágenes con LabelImg primero."
            )
            return
        
        # Confirmar
        response = messagebox.askyesno(
            "Confirmar Entrenamiento",
            f"Se entrenarán {stats['total_images']} imágenes anotadas con {stats['total_objects']} objetos.\n\n"
            f"Configuración:\n"
            f"- Modelo: YOLOv8{self.yolo_model_size.get()}\n"
            f"- Épocas: {self.yolo_epochs.get()}\n"
            f"- Batch: {self.yolo_batch.get()}\n\n"
            f"⚠️ Esto puede tomar varios minutos u horas.\n\n"
            f"¿Continuar?"
        )
        
        if not response:
            return
        
        self.analysis_running = True
        self.yolo_console.delete(1.0, tk.END)
        self.log_yolo("🚀 Iniciando entrenamiento YOLOv8...\n")
        self.log_yolo("="*60 + "\n\n")
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=self.run_yolo_training, daemon=True)
        thread.start()
    
    def run_yolo_training(self):
        """Ejecuta el entrenamiento YOLO."""
        try:
            # Iniciar animación de progreso
            self.yolo_progress.start(10)
            self.yolo_progress_label.config(text="Inicializando...")
            
            from src.train_yolo import YOLOTrainer
            
            self.log_yolo("📦 Inicializando entrenador YOLO...\n")
            
            trainer = YOLOTrainer(
                annotations_dir=str(ANNOTATIONS_DIR),
                images_dir=str(RAW_IMAGES_DIR),
                output_dir="yolo_training"
            )
            
            self.log_yolo("✅ Entrenador inicializado\n\n")
            self.yolo_progress_label.config(text="Convirtiendo dataset...")
            self.log_yolo("📋 Convirtiendo anotaciones VOC a formato YOLO...\n")
            
            # Convertir dataset
            data_yaml = trainer.convert_voc_to_yolo()
            self.log_yolo(f"✅ Dataset convertido: {data_yaml}\n\n")
            
            # Entrenar
            self.yolo_progress_label.config(text="Entrenando modelo...")
            self.log_yolo("🎯 Iniciando entrenamiento...\n")
            self.log_yolo("   (Esto puede tomar mucho tiempo)\n")
            self.log_yolo(f"   Épocas: {self.yolo_epochs.get()}\n")
            self.log_yolo(f"   Tamaño: {self.yolo_imgsz.get()}px\n\n")
            
            best_model, training_number = trainer.train_model(
                data_yaml=data_yaml,
                model_size=self.yolo_model_size.get(),
                epochs=self.yolo_epochs.get(),
                batch=self.yolo_batch.get(),
                imgsz=self.yolo_imgsz.get(),
                device='cpu'  # Usar CPU (no hay GPU disponible)
            )
            
            self.yolo_progress_label.config(text="Evaluando modelo...")
            self.log_yolo("\n" + "="*60 + "\n")
            self.log_yolo(f"🎉 ENTRENAMIENTO #{training_number} COMPLETADO\n")
            self.log_yolo("="*60 + "\n\n")
            self.log_yolo(f"📦 Modelo guardado en:\n   {best_model}\n\n")
            
            # Actualizar path del modelo
            self.yolo_model_path.set(best_model)
            
            # Evaluar
            self.log_yolo("📊 Evaluando modelo...\n")
            trainer.evaluate_model(best_model, data_yaml)
            
            self.yolo_progress_label.config(text="✅ Completado")
            self.yolo_progress.stop()
            self.log_yolo("\n✅ Proceso completado exitosamente\n")
            self.log_yolo("💡 Ahora puedes usar este modelo en la pestaña de Análisis\n")
            
            messagebox.showinfo(
                "Entrenamiento Completado",
                f"Entrenamiento #{training_number} completado exitosamente.\n\n"
                f"Modelo guardado en:\n{best_model}\n\n"
                f"Ve a la pestaña de Análisis y activa 'Usar YOLOv8'"
            )
            
        except ImportError as e:
            self.yolo_progress.stop()
            self.yolo_progress_label.config(text="❌ Error")
            self.log_yolo(f"\n❌ ERROR: ultralytics no está instalado\n")
            self.log_yolo(f"   Ejecuta: pip install ultralytics torch torchvision\n")
            messagebox.showerror("Error", f"Falta ultralytics:\n{str(e)}\n\nEjecuta:\npip install ultralytics")
            
        except Exception as e:
            self.yolo_progress.stop()
            self.yolo_progress_label.config(text="❌ Error")
            self.log_yolo(f"\n❌ ERROR durante el entrenamiento:\n{str(e)}\n")
            messagebox.showerror("Error", f"Error durante el entrenamiento:\n{str(e)}")
            
        finally:
            self.analysis_running = False
    
    def log_yolo(self, message):
        """Agrega mensaje a la consola YOLO."""
        self.yolo_console.insert(tk.END, message)
        self.yolo_console.see(tk.END)
        self.root.update_idletasks()
    
    def create_viewer_tab(self, parent):
        """Crea la pestaña de visualización de gráficos."""
        
        # Frame superior con controles
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(control_frame, text="📂 Selecciona un gráfico:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Combobox para seleccionar gráfico
        self.graph_combo = ttk.Combobox(control_frame, width=50, state="readonly")
        self.graph_combo.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.graph_combo.bind("<<ComboboxSelected>>", self.load_selected_graph)
        
        # Botón refrescar
        ttk.Button(
            control_frame,
            text="🔄 Actualizar Lista",
            command=self.refresh_graph_list
        ).pack(side=tk.LEFT, padx=5)
        
        # Frame para categorías
        category_frame = ttk.Frame(parent)
        category_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(category_frame, text="🔍 Filtrar por:", font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        
        self.filter_var = tk.StringVar(value="Todos")
        filters = ["Todos", "Dashboard", "Distribución Tamaños", "Distribución Formas", 
                   "Frecuencia", "Correlación", "Comparativos"]
        
        for filter_name in filters:
            ttk.Radiobutton(
                category_frame,
                text=filter_name,
                variable=self.filter_var,
                value=filter_name,
                command=self.refresh_graph_list
            ).pack(side=tk.LEFT, padx=3)
        
        # Frame con scroll para la imagen
        canvas_frame = ttk.LabelFrame(parent, text="📊 Vista Previa del Gráfico", padding=10)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas con scrollbars
        scroll_frame = ttk.Frame(canvas_frame)
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars horizontales y verticales
        h_scrollbar = tk.Scrollbar(scroll_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        v_scrollbar = tk.Scrollbar(scroll_frame, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Canvas para mostrar imagen
        self.image_canvas = tk.Canvas(
            scroll_frame,
            bg="#f0f0f0",
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set,
            highlightthickness=0
        )
        self.image_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        v_scrollbar.config(command=self.image_canvas.yview)
        h_scrollbar.config(command=self.image_canvas.xview)
        
        # Bind de la rueda del ratón para scroll
        def on_mouse_wheel(event):
            # En Windows, event.delta es múltiplo de 120
            self.image_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def on_shift_mouse_wheel(event):
            # Shift + rueda = scroll horizontal
            self.image_canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
        
        self.image_canvas.bind("<MouseWheel>", on_mouse_wheel)
        self.image_canvas.bind("<Shift-MouseWheel>", on_shift_mouse_wheel)
        
        # Botones de control de imagen
        img_control_frame = ttk.Frame(parent)
        img_control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.zoom_var = tk.DoubleVar(value=0.3)  # Zoom predeterminado 30%
        
        ttk.Button(
            img_control_frame,
            text="🔍 Zoom +",
            command=lambda: self.zoom_image(1.2)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            img_control_frame,
            text="🔍 Zoom -",
            command=lambda: self.zoom_image(0.8)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            img_control_frame,
            text="↻ Reset Zoom",
            command=lambda: self.zoom_image(0, reset=True)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(img_control_frame, text="Zoom:").pack(side=tk.LEFT, padx=5)
        self.zoom_label = ttk.Label(img_control_frame, text="100%", font=("Arial", 9, "bold"))
        self.zoom_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            img_control_frame,
            text="💾 Guardar Como...",
            command=self.save_graph_as
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            img_control_frame,
            text="📂 Abrir en Explorador",
            command=self.open_graph_in_explorer
        ).pack(side=tk.RIGHT, padx=5)
        
        # Variables para imagen
        self.current_image_path = None
        self.current_image = None
        self.current_photo = None
        self.original_image = None
        
        # Cargar lista al inicio
        self.root.after(1500, self.refresh_graph_list)
    
    def refresh_graph_list(self):
        """Actualiza la lista de gráficos disponibles."""
        graph_files = list(GRAPHS_DIR.glob("*.png"))
        
        if not graph_files:
            self.graph_combo['values'] = ["No hay gráficos disponibles"]
            self.graph_combo.current(0)
            return
        
        # Filtrar según categoría
        filter_value = self.filter_var.get()
        
        filtered_files = []
        for file in graph_files:
            name = file.stem
            
            if filter_value == "Todos":
                filtered_files.append(file)
            elif filter_value == "Dashboard" and "dashboard" in name:
                filtered_files.append(file)
            elif filter_value == "Distribución Tamaños" and "size_distribution" in name:
                filtered_files.append(file)
            elif filter_value == "Distribución Formas" and "shape_distribution" in name:
                filtered_files.append(file)
            elif filter_value == "Frecuencia" and "frequency" in name:
                filtered_files.append(file)
            elif filter_value == "Correlación" and "correlation" in name:
                filtered_files.append(file)
            elif filter_value == "Comparativos" and "comparative" in name:
                filtered_files.append(file)
        
        if not filtered_files:
            self.graph_combo['values'] = ["No hay gráficos en esta categoría"]
            self.graph_combo.current(0)
            return
        
        # Ordenar por nombre
        filtered_files.sort()
        
        # Crear lista de nombres
        graph_names = [f.name for f in filtered_files]
        self.graph_combo['values'] = graph_names
        
        # Mensaje informativo
        self.log_console(f"[INFO] Se encontraron {len(graph_names)} graficos en la categoria '{filter_value}'\n")
        
        # Seleccionar el primero
        if graph_names:
            self.graph_combo.current(0)
            self.load_selected_graph()
    
    def load_selected_graph(self, event=None):
        """Carga el gráfico seleccionado."""
        selected = self.graph_combo.get()
        
        if not selected or selected in ["No hay gráficos disponibles", "No hay gráficos en esta categoría"]:
            return
        
        graph_path = GRAPHS_DIR / selected
        
        if not graph_path.exists():
            messagebox.showerror("Error", f"No se encontró el archivo:\n{graph_path}")
            return
        
        try:
            # Cargar imagen
            self.current_image_path = graph_path
            self.original_image = Image.open(graph_path)
            self.zoom_var.set(0.3)  # Zoom inicial 30%
            self.display_image()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la imagen:\n{str(e)}")
    
    def display_image(self):
        """Muestra la imagen en el canvas."""
        if self.original_image is None:
            return
        
        # Aplicar zoom
        zoom = self.zoom_var.get()
        new_width = int(self.original_image.width * zoom)
        new_height = int(self.original_image.height * zoom)
        
        self.current_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.current_photo = ImageTk.PhotoImage(self.current_image)
        
        # Limpiar canvas
        self.image_canvas.delete("all")
        
        # Mostrar imagen
        self.image_canvas.create_image(0, 0, anchor=tk.NW, image=self.current_photo)
        
        # Actualizar scroll region
        self.image_canvas.config(scrollregion=(0, 0, new_width, new_height))
        
        # Actualizar etiqueta de zoom
        self.zoom_label.config(text=f"{int(zoom * 100)}%")
    
    def zoom_image(self, factor, reset=False):
        """Aplica zoom a la imagen."""
        if self.original_image is None:
            return
        
        if reset:
            self.zoom_var.set(0.3)  # Reset al 30%
        else:
            current_zoom = self.zoom_var.get()
            new_zoom = current_zoom * factor
            # Limitar zoom entre 0.1x y 5x
            new_zoom = max(0.1, min(5.0, new_zoom))
            self.zoom_var.set(new_zoom)
        
        self.display_image()
    
    def save_graph_as(self):
        """Guarda el gráfico actual con otro nombre."""
        if self.current_image_path is None:
            messagebox.showwarning("Sin Gráfico", "No hay ningún gráfico cargado.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("Todos", "*.*")],
            initialfile=self.current_image_path.name
        )
        
        if file_path:
            try:
                self.original_image.save(file_path)
                messagebox.showinfo("Guardado", f"Gráfico guardado en:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar:\n{str(e)}")
    
    def open_graph_in_explorer(self):
        """Abre la ubicación del gráfico en el explorador."""
        if self.current_image_path is None:
            messagebox.showwarning("Sin Gráfico", "No hay ningún gráfico cargado.")
            return
        
        import os
        import platform
        
        if platform.system() == "Windows":
            os.system(f'explorer /select,"{self.current_image_path}"')
        elif platform.system() == "Darwin":  # macOS
            os.system(f'open -R "{self.current_image_path}"')
        else:  # Linux
            os.system(f'xdg-open "{self.current_image_path.parent}"')
    
    def create_management_tab(self, parent):
        """Crea la pestaña de gestión de resultados."""
        
        info_frame = ttk.LabelFrame(parent, text="ℹ️ Información de Resultados", padding=15)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Hacer el text widget más grande y con scroll
        text_scroll_frame = ttk.Frame(info_frame)
        text_scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(text_scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.info_text = tk.Text(
            text_scroll_frame, 
            height=15,  # Tamaño intermedio
            font=("Courier New", 10),  # Fuente más grande
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            bg="#f5f5f5",
            fg="#000000",
            padx=10,
            pady=10
        )
        self.info_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.info_text.yview)
        
        # Botones de gestión
        btn_frame = ttk.Frame(parent, padding=10)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            btn_frame,
            text="🔄 Actualizar Información",
            command=self.update_results_info
        ).pack(fill=tk.X, pady=5)
        
        ttk.Button(
            btn_frame,
            text="💾 Crear Respaldo",
            command=self.backup_results
        ).pack(fill=tk.X, pady=5)
        
        ttk.Button(
            btn_frame,
            text="🗑️ Limpiar Resultados",
            command=self.clean_results
        ).pack(fill=tk.X, pady=5)
        
        ttk.Button(
            btn_frame,
            text="📂 Abrir Carpeta de Respaldos",
            command=self.open_backups_folder
        ).pack(fill=tk.X, pady=5)
        
        # Actualizar info al cargar
        self.root.after(1000, self.update_results_info)
    
    def browse_images(self):
        """Abre diálogo para seleccionar imágenes y luego abre LabelImg para anotarlas."""
        files = filedialog.askopenfilenames(
            title="Seleccionar imágenes microscópicas para anotar",
            filetypes=[
                ("Imagenes", "*.jpg *.jpeg *.png *.tif *.tiff *.bmp"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if files:
            # Copiar archivos seleccionados a data/raw_images si no están ahí
            copied_files = []
            for file_path in files:
                source = Path(file_path)
                if source.exists() and source.is_file():
                    # Si el archivo no está en raw_images, copiarlo
                    if not str(source.parent).endswith('raw_images'):
                        dest = RAW_IMAGES_DIR / source.name
                        try:
                            import shutil
                            shutil.copy2(source, dest)
                            copied_files.append(str(dest))
                            self.log_console(f"[✓] Copiado: {source.name}\n")
                        except Exception as e:
                            self.log_console(f"[✗] Error al copiar {source.name}: {e}\n")
                    else:
                        copied_files.append(str(source))
            
            # Actualizar lista de imágenes
            if copied_files:
                self.image_files.extend(copied_files)
                self.image_files = list(set(self.image_files))  # Eliminar duplicados
                self.update_image_list()
                self.log_console(f"[OK] {len(copied_files)} imagen(es) lista(s) para anotar\n")
                
                # Preguntar si desea abrir LabelImg
                respuesta = messagebox.askyesno(
                    "Anotar Imágenes",
                    f"Se han cargado {len(copied_files)} imagen(es).\n\n"
                    "¿Desea abrir LabelImg para anotarlas ahora?",
                    icon='question'
                )
                
                if respuesta:
                    self.log_console("[→] Abriendo LabelImg para anotar imágenes...\n")
                    # Cambiar a la pestaña de anotación
                    self.notebook.select(1)  # Pestaña de anotación (índice 1)
                    # Abrir LabelImg
                    self.root.after(500, self.launch_labelimg)
            else:
                self.log_console(f"[!] No se pudieron cargar las imágenes\n")
    
    def load_default_images(self):
        """Carga imágenes de la carpeta de análisis (NO para entrenamiento)."""
        # Crear carpeta si no existe
        ANALYSIS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        
        image_extensions = ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.bmp']
        temp_files = []
        
        for ext in image_extensions:
            temp_files.extend(ANALYSIS_IMAGES_DIR.glob(f'*{ext}'))
            temp_files.extend(ANALYSIS_IMAGES_DIR.glob(f'*{ext.upper()}'))
        
        # Filtrar archivos válidos y eliminar duplicados
        unique_files = list(set([str(f) for f in temp_files if f.exists() and f.is_file()]))
        unique_files.sort()
        self.image_files = unique_files
        self.update_image_list()
        
        if self.image_files:
            self.log_console(f"[OK] Cargadas {len(self.image_files)} imágenes de análisis\n")
            messagebox.showinfo(
                "Imágenes Cargadas",
                f"Se han cargado {len(self.image_files)} imagen(es) para analizar.\n\n"
                f"Ve a la pestaña 'Análisis' para procesarlas con el modelo."
            )
        else:
            self.log_console(f"[!] No se encontraron imágenes en {ANALYSIS_IMAGES_DIR}\n")
            messagebox.showwarning(
                "Sin imágenes",
                f"No hay imágenes en la carpeta de análisis.\n\n"
                f"Copia las imágenes que quieras analizar a:\n{ANALYSIS_IMAGES_DIR}\n\n"
                f"Nota: Las imágenes de entrenamiento están en data/raw_images"
            )
            messagebox.showwarning(
                "Sin imágenes",
                f"No se encontraron imágenes en:\n{RAW_IMAGES_DIR}\n\n"
                "Use 'Cargar Imágenes para Anotar' para agregar imágenes."
            )
    
    def update_image_list(self):
        """Actualiza la lista de imagenes en la interfaz."""
        self.image_listbox.delete(0, tk.END)
        for img in self.image_files:
            filename = Path(img).name
            self.image_listbox.insert(tk.END, f"  [IMG] {filename}")
    
    def remove_selected_images(self):
        """Elimina las imágenes seleccionadas de la lista."""
        selected_indices = self.image_listbox.curselection()
        
        if not selected_indices:
            self.log_console("[!] Selecciona una o mas imagenes para eliminar (Ctrl+Click para multiple).\n")
            return
        
        # Eliminar sin confirmación
        count = len(selected_indices)
        
        # Eliminar en orden inverso para no alterar índices
        for index in reversed(selected_indices):
            del self.image_files[index]
        
        self.update_image_list()
        self.log_console(f"[OK] {count} imagen(es) eliminada(s) de la lista\n")
    
    def clear_all_images(self):
        """Limpia todas las imagenes de la lista."""
        if not self.image_files:
            self.log_console("[!] No hay imagenes en la lista.\n")
            return
        
        count = len(self.image_files)
        self.image_files = []
        self.update_image_list()
        self.log_console(f"[OK] {count} imagenes eliminadas de la lista\n")
    
    def log_console(self, message):
        """Agrega mensaje a la consola."""
        self.console.insert(tk.END, message)
        self.console.see(tk.END)
        self.root.update_idletasks()
    
    def clear_console(self):
        """Limpia la consola."""
        self.console.delete(1.0, tk.END)
    
    def check_message_queue(self):
        """Verifica mensajes en la cola."""
        try:
            while True:
                message = self.message_queue.get_nowait()
                self.log_console(message)
        except queue.Empty:
            pass
        
        self.root.after(100, self.check_message_queue)
    
    def start_analysis(self):
        """Inicia el análisis en un hilo separado."""
        if not self.image_files:
            self.log_console("[!] No hay imagenes cargadas. Usa el boton 'Usar Carpeta por Defecto' primero.\n")
            return
        
        # Validar que hay un modelo YOLO seleccionado
        if not self.yolo_model_path.get():
            messagebox.showerror(
                "Error: Modelo No Seleccionado",
                "⚠️ Debes seleccionar un modelo YOLOv8 entrenado primero.\n\n"
                "Ve a la pestaña 'Entrenar YOLOv8' y:\n"
                "1. Entrena un modelo (si no tienes uno)\n"
                "2. Haz clic en 'Buscar Modelo' para seleccionarlo"
            )
            self.log_console("[!] ERROR: No hay modelo YOLO seleccionado.\n")
            self.log_console("   Ve a 'Entrenar YOLOv8' y selecciona un modelo .pt\n")
            return
        
        # Validar que el archivo existe
        if not Path(self.yolo_model_path.get()).exists():
            messagebox.showerror(
                "Error: Modelo No Encontrado",
                f"❌ El modelo seleccionado no existe:\n\n{self.yolo_model_path.get()}\n\n"
                "Selecciona un modelo válido en la pestaña 'Entrenar YOLOv8'."
            )
            self.log_console(f"[!] ERROR: Modelo no encontrado: {self.yolo_model_path.get()}\n")
            return
        
        if self.analysis_running:
            self.log_console("[!] Ya hay un analisis en ejecucion.\n")
            return
        
        self.analysis_running = True
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.progress.start()
        self.clear_console()
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=self.run_analysis, daemon=True)
        thread.start()
    
    def run_analysis(self):
        """Ejecuta el análisis completo."""
        try:
            # Importar aquí para evitar problemas circulares
            sys.path.insert(0, str(Path(__file__).parent))
            from src.image_processing import ImageProcessor
            from src.statistical_analysis import StatisticalAnalyzer
            from src.visualization import DataVisualizer
            
            self.message_queue.put("="*60 + "\n")
            self.message_queue.put("[INICIO] ANALISIS DE MICROPLASTICOS CON YOLOv8\n")
            self.message_queue.put("="*60 + "\n\n")
            
            # Mostrar información del modelo
            model_name = Path(self.yolo_model_path.get()).name
            self.message_queue.put(f"🤖 Método de detección: YOLOv8\n")
            self.message_queue.put(f"📦 Modelo: {model_name}\n")
            self.message_queue.put(f"📏 Calibración: {self.pixels_to_um.get():.4f} μm/píxel\n")
            self.message_queue.put("\n")
            
            # Crear sistema inline
            class MicroplasticAnalysisSystem:
                def __init__(self_inner, pixels_to_um, yolo_model_path):
                    # Usar self_inner para evitar conflicto con self externo
                    self_inner.processor = ImageProcessor(
                        pixels_to_um=pixels_to_um,
                        yolo_model_path=yolo_model_path
                    )
                    self_inner.analyzer = StatisticalAnalyzer()
                    self_inner.visualizer = DataVisualizer()
                    self_inner.results = {}
                
                def analyze_single_sample(self, image_path, sample_id):
                    """Analiza una única muestra."""
                    try:
                        self.message_queue.put(f"\n{'='*60}\n")
                        self.message_queue.put(f"Analizando muestra: {sample_id}\n")
                        self.message_queue.put(f"{'='*60}\n")
                        
                        # 1. Procesar imagen
                        self.message_queue.put("1. Procesando imagen...\n")
                        particles, labeled = self.processor.process_image(
                            image_path,
                            save_processed=True,
                            output_dir=str(PROCESSED_IMAGES_DIR)
                        )
                        self.message_queue.put(f"   ✓ Detectadas {len(particles)} partículas\n")
                        
                        # Verificar si se detectaron partículas
                        if not particles or len(particles) == 0:
                            self.message_queue.put("\n⚠️  No se detectaron partículas en esta imagen\n")
                            self.message_queue.put("   El modelo puede necesitar más entrenamiento\n")
                            self.message_queue.put("   o la imagen no contiene objetos detectables\n\n")
                            return None
                        
                        # 2. Convertir a DataFrame
                        self.message_queue.put("2. Analizando datos estadísticos...\n")
                        df = self.analyzer.particles_to_dataframe(particles, sample_id)
                        
                        # Verificar que el dataframe tenga datos válidos
                        if df.empty or len(df) == 0:
                            self.message_queue.put("\n⚠️  No se pudieron procesar las partículas detectadas\n\n")
                            return None
                        
                        # 3. Generar visualizaciones
                        self.message_queue.put("3. Generando visualizaciones...\n")
                        
                        # Gráfico de distribución por TIPO de microplástico
                        if 'class_name' in df.columns and not df['class_name'].isna().all():
                            class_plot_path = GRAPHS_DIR / f"{sample_id}_class_distribution.png"
                            self.visualizer.plot_class_distribution(df, sample_id, str(class_plot_path))
                            self.message_queue.put(f"   ✓ Guardado: {class_plot_path.name}\n")
                        
                        if 'equivalent_diameter_um' in df.columns:
                            size_plot_path = GRAPHS_DIR / f"{sample_id}_size_distribution.png"
                            self.visualizer.plot_size_distribution(df, sample_id, str(size_plot_path))
                            self.message_queue.put(f"   ✓ Guardado: {size_plot_path.name}\n")
                        
                        if 'aspect_ratio' in df.columns:
                            shape_plot_path = GRAPHS_DIR / f"{sample_id}_shape_distribution.png"
                            self.visualizer.plot_shape_distribution(df, sample_id, str(shape_plot_path))
                            self.message_queue.put(f"   ✓ Guardado: {shape_plot_path.name}\n")
                        
                        dashboard_path = GRAPHS_DIR / f"{sample_id}_dashboard.png"
                        self.visualizer.create_summary_dashboard(df, sample_id, str(dashboard_path))
                        self.message_queue.put(f"   ✓ Guardado: {dashboard_path.name}\n")
                        
                        freq_path = GRAPHS_DIR / f"{sample_id}_frequency_curve.png"
                        self.visualizer.plot_size_frequency_curve(df, sample_id, str(freq_path))
                        self.message_queue.put(f"   ✓ Guardado: {freq_path.name}\n")
                        
                        corr_path = GRAPHS_DIR / f"{sample_id}_correlation_matrix.png"
                        self.visualizer.plot_correlation_matrix(df, str(corr_path))
                        self.message_queue.put(f"   ✓ Guardado: {corr_path.name}\n")
                        
                        # 4. Generar reporte textual
                        self.message_queue.put("4. Generando reporte...\n")
                        report = self.analyzer.generate_summary_report(df, sample_id)
                        report_path = REPORTS_DIR / f"{sample_id}_report.txt"
                        with open(report_path, 'w', encoding='utf-8') as f:
                            f.write(report)
                        self.message_queue.put(f"   ✓ Guardado: {report_path.name}\n")
                        
                        # 5. Exportar datos a Excel
                        self.message_queue.put("5. Exportando datos...\n")
                        excel_path = REPORTS_DIR / f"{sample_id}_data.xlsx"
                        df.to_excel(excel_path, index=False)
                        self.message_queue.put(f"   ✓ Guardado: {excel_path.name}\n")
                        
                        self.results[sample_id] = df
                        self.message_queue.put(f"\n✓ Análisis de {sample_id} completado exitosamente\n")
                        
                        return df
                        
                    except Exception as e:
                        self.message_queue.put(f"\n❌ ERROR al analizar {sample_id}:\n")
                        self.message_queue.put(f"   {str(e)}\n\n")
                        import traceback
                        self.message_queue.put(f"Detalles: {traceback.format_exc()}\n")
                        return None
                
                def analyze_multiple_samples(self, image_paths):
                    for sample_id, image_path in image_paths.items():
                        self.analyze_single_sample(image_path, sample_id)
                    
                    if len(self.results) > 1:
                        self.message_queue.put(f"\n{'='*60}\n")
                        self.message_queue.put("ANÁLISIS COMPARATIVO\n")
                        self.message_queue.put(f"{'='*60}\n")
                        
                        comp_area_path = GRAPHS_DIR / "comparative_area.png"
                        self.visualizer.plot_comparative_analysis(
                            self.results, 'area_um2', str(comp_area_path)
                        )
                        self.message_queue.put(f"   ✓ Guardado: {comp_area_path.name}\n")
                        
                        comp_diam_path = GRAPHS_DIR / "comparative_diameter.png"
                        self.visualizer.plot_comparative_analysis(
                            self.results, 'equivalent_diameter_um', str(comp_diam_path)
                        )
                        self.message_queue.put(f"   ✓ Guardado: {comp_diam_path.name}\n")
                        
                        comp_aspect_path = GRAPHS_DIR / "comparative_aspect_ratio.png"
                        self.visualizer.plot_comparative_analysis(
                            self.results, 'aspect_ratio', str(comp_aspect_path)
                        )
                        self.message_queue.put(f"   ✓ Guardado: {comp_aspect_path.name}\n")
                
                def generate_consolidated_report(self):
                    if not self.results:
                        return
                    
                    self.message_queue.put(f"\n{'='*60}\n")
                    self.message_queue.put("GENERANDO REPORTE CONSOLIDADO\n")
                    self.message_queue.put(f"{'='*60}\n")
                    
                    import pandas as pd
                    
                    all_data = pd.concat(self.results.values(), ignore_index=True)
                    
                    consolidated_path = REPORTS_DIR / "consolidated_data.xlsx"
                    all_data.to_excel(consolidated_path, index=False)
                    self.message_queue.put(f"✓ Datos consolidados guardados: {consolidated_path.name}\n")
                    
                    summary_stats = []
                    for sample_id, df in self.results.items():
                        stats = {
                            'Muestra': sample_id,
                            'N_partículas': len(df),
                            'Área_media_μm2': df['area_um2'].mean() if 'area_um2' in df.columns else 0,
                            'Área_std_μm2': df['area_um2'].std() if 'area_um2' in df.columns else 0,
                            'Diámetro_medio_μm': df['equivalent_diameter_um'].mean() if 'equivalent_diameter_um' in df.columns else 0,
                            'Diámetro_std_μm': df['equivalent_diameter_um'].std() if 'equivalent_diameter_um' in df.columns else 0,
                            'Relación_aspecto_media': df['aspect_ratio'].mean() if 'aspect_ratio' in df.columns else 0,
                        }
                        summary_stats.append(stats)
                    
                    summary_df = pd.DataFrame(summary_stats)
                    summary_path = REPORTS_DIR / "summary_statistics.xlsx"
                    summary_df.to_excel(summary_path, index=False)
                    self.message_queue.put(f"✓ Estadísticos resumen guardados: {summary_path.name}\n")
            
            # Vincular message_queue al sistema
            MicroplasticAnalysisSystem.message_queue = self.message_queue
            
            # Crear sistema con configuración YOLO
            system = MicroplasticAnalysisSystem(
                pixels_to_um=self.pixels_to_um.get(),
                yolo_model_path=self.yolo_model_path.get()
            )
            
            # Preparar muestras
            samples = {}
            for img_file in self.image_files:
                sample_id = Path(img_file).stem
                samples[sample_id] = img_file
            
            # Analizar
            if len(samples) == 1:
                sample_id, image_path = list(samples.items())[0]
                system.analyze_single_sample(image_path, sample_id)
            else:
                system.analyze_multiple_samples(samples)
            
            system.generate_consolidated_report()
            
            self.message_queue.put("\n" + "="*60 + "\n")
            self.message_queue.put("[COMPLETADO] ANALISIS FINALIZADO\n")
            self.message_queue.put("="*60 + "\n")
            self.message_queue.put(f"\n[INFO] Resultados guardados en:\n")
            self.message_queue.put(f"  - Graficos: {GRAPHS_DIR}\n")
            self.message_queue.put(f"  - Reportes: {REPORTS_DIR}\n\n")
            
            # Cambiar a pestaña de gráficos automáticamente (ahora es índice 4)
            self.root.after(0, lambda: self.notebook.select(4))
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            self.message_queue.put(f"\n[ERROR] {str(e)}\n")
            self.message_queue.put(f"{error_details}\n")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error durante el analisis:\n{str(e)}"))
        
        finally:
            self.analysis_running = False
            self.root.after(0, self.analysis_finished)
    
    def analysis_finished(self):
        """Callback cuando termina el análisis."""
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.progress.stop()
        self.update_results_info()
    
    def stop_analysis(self):
        """Detiene el análisis."""
        self.analysis_running = False
        self.log_console("\n[!] Analisis detenido por el usuario.\n")
    
    def update_results_info(self):
        """Actualiza la información de resultados."""
        try:
            from src.results_manager import ResultsManager
            
            manager = ResultsManager()
            
            self.info_text.delete(1.0, tk.END)
            
            # Obtener info
            graphs_size = manager.get_folder_size(GRAPHS_DIR)
            reports_size = manager.get_folder_size(REPORTS_DIR)
            processed_size = manager.get_folder_size(PROCESSED_IMAGES_DIR)
            
            graphs_count = manager.count_files(GRAPHS_DIR, "png")
            excel_count = manager.count_files(REPORTS_DIR, "xlsx")
            txt_count = manager.count_files(REPORTS_DIR, "txt")
            processed_count = manager.count_files(PROCESSED_IMAGES_DIR)
            
            total_size = graphs_size + reports_size + processed_size
            
            info = f"""
╔══════════════════════════════════════════════════════════════╗
║           ESTADO ACTUAL DE RESULTADOS                        ║
╚══════════════════════════════════════════════════════════════╝

📊 Gráficos (results/graphs/):
   • Archivos PNG: {graphs_count}
   • Espacio usado: {graphs_size:.2f} MB

📄 Reportes (results/reports/):
   • Archivos Excel: {excel_count}
   • Archivos TXT: {txt_count}
   • Espacio usado: {reports_size:.2f} MB

🖼️  Imágenes Procesadas:
   • Archivos: {processed_count}
   • Espacio usado: {processed_size:.2f} MB

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💾 ESPACIO TOTAL USADO: {total_size:.2f} MB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            self.info_text.insert(1.0, info)
            
        except Exception as e:
            error_msg = f"Error al actualizar información:\n{str(e)}"
            self.info_text.insert(1.0, error_msg)
            print(f"DEBUG: {error_msg}")
    
    def backup_results(self):
        """Crea respaldo de resultados."""
        from src.results_manager import ResultsManager
        from datetime import datetime
        
        # Verificar si hay resultados para respaldar
        manager = ResultsManager()
        graphs_count = manager.count_files(GRAPHS_DIR, "png")
        reports_count = manager.count_files(REPORTS_DIR, "xlsx") + manager.count_files(REPORTS_DIR, "txt")
        
        if graphs_count == 0 and reports_count == 0:
            messagebox.showwarning(
                "Sin Resultados",
                "No hay resultados disponibles para respaldar.\n\n"
                "Ejecuta un análisis primero para generar resultados."
            )
            return
        
        if messagebox.askyesno(
            "Crear Respaldo", 
            f"Se respaldarán:\n"
            f"• {graphs_count} gráficos\n"
            f"• {reports_count} reportes\n\n"
            f"¿Deseas continuar?"
        ):
            try:
                # Mostrar ventana de progreso
                progress_win = tk.Toplevel(self.root)
                progress_win.title("Creando Respaldo")
                progress_win.geometry("400x150")
                progress_win.transient(self.root)
                progress_win.grab_set()
                
                tk.Label(
                    progress_win, 
                    text="🔄 Creando respaldo...\nPor favor espera.",
                    font=("Arial", 12),
                    pady=20
                ).pack()
                
                progress_bar = ttk.Progressbar(progress_win, mode='indeterminate')
                progress_bar.pack(fill=tk.X, padx=20, pady=20)
                progress_bar.start()
                
                status_label = tk.Label(progress_win, text="Iniciando...", font=("Arial", 9))
                status_label.pack()
                
                self.root.update()
                
                # Crear respaldo
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_folder = manager.backups_dir / f"backup_{timestamp}"
                backup_folder.mkdir(parents=True, exist_ok=True)
                
                import shutil
                
                # Copiar gráficos
                if graphs_count > 0:
                    status_label.config(text="Copiando gráficos...")
                    self.root.update()
                    backup_graphs = backup_folder / "graphs"
                    backup_graphs.mkdir(parents=True, exist_ok=True)
                    for file in GRAPHS_DIR.glob("*.png"):
                        shutil.copy2(file, backup_graphs / file.name)
                
                # Copiar reportes
                if reports_count > 0:
                    status_label.config(text="Copiando reportes...")
                    self.root.update()
                    backup_reports = backup_folder / "reports"
                    backup_reports.mkdir(parents=True, exist_ok=True)
                    for file in REPORTS_DIR.glob("*"):
                        if file.suffix in ['.xlsx', '.txt']:
                            shutil.copy2(file, backup_reports / file.name)
                
                # Copiar imágenes procesadas
                processed_files = [f for f in PROCESSED_IMAGES_DIR.glob("*") 
                                 if f.name not in [".gitkeep", "INSTRUCCIONES.md"]]
                if processed_files:
                    status_label.config(text="Copiando imágenes procesadas...")
                    self.root.update()
                    backup_processed = backup_folder / "processed_images"
                    backup_processed.mkdir(parents=True, exist_ok=True)
                    for file in processed_files:
                        shutil.copy2(file, backup_processed / file.name)
                
                backup_size = manager.get_folder_size(backup_folder)
                
                progress_bar.stop()
                progress_win.destroy()
                
                messagebox.showinfo(
                    "Respaldo Creado", 
                    f"✓ El respaldo se ha creado exitosamente.\n\n"
                    f"Ubicación: {backup_folder.name}\n"
                    f"Tamaño: {backup_size:.2f} MB\n\n"
                    f"Carpeta completa:\n{backup_folder}"
                )
                
                # Abrir carpeta de respaldo
                import subprocess
                try:
                    subprocess.Popen(f'explorer "{backup_folder}"')
                except:
                    pass
                
                self.update_results_info()
                
            except Exception as e:
                if 'progress_win' in locals():
                    progress_win.destroy()
                messagebox.showerror(
                    "Error al Crear Respaldo",
                    f"Ocurrió un error al crear el respaldo:\n\n{str(e)}"
                )
    
    def clean_results(self):
        """Limpia todos los resultados."""
        from src.results_manager import ResultsManager
        
        manager = ResultsManager()
        
        # Contar archivos
        graphs_count = manager.count_files(GRAPHS_DIR, "png")
        excel_count = manager.count_files(REPORTS_DIR, "xlsx")
        txt_count = manager.count_files(REPORTS_DIR, "txt")
        processed_files = [f for f in PROCESSED_IMAGES_DIR.glob("*") 
                          if f.name not in [".gitkeep", "INSTRUCCIONES.md"]]
        processed_count = len(processed_files)
        
        total_files = graphs_count + excel_count + txt_count + processed_count
        
        if total_files == 0:
            messagebox.showinfo(
                "Sin Resultados",
                "No hay resultados para limpiar.\n\n"
                "Las carpetas ya están vacías."
            )
            return
        
        response = messagebox.askyesnocancel(
            "Limpiar Resultados",
            f"Se eliminarán:\n"
            f"• {graphs_count} gráficos PNG\n"
            f"• {excel_count} archivos Excel\n"
            f"• {txt_count} archivos TXT\n"
            f"• {processed_count} imágenes procesadas\n\n"
            f"¿Deseas crear un respaldo antes de limpiar?\n\n"
            "Sí = Respaldar y limpiar\n"
            "No = Solo limpiar\n"
            "Cancelar = No hacer nada"
        )
        
        if response is None:  # Cancelar
            return
        
        if response:  # Sí - respaldar primero
            self.backup_results()
        
        try:
            # Mostrar ventana de progreso
            progress_win = tk.Toplevel(self.root)
            progress_win.title("Limpiando Resultados")
            progress_win.geometry("400x150")
            progress_win.transient(self.root)
            progress_win.grab_set()
            
            tk.Label(
                progress_win, 
                text="🗑️ Limpiando resultados...\nPor favor espera.",
                font=("Arial", 12),
                pady=20
            ).pack()
            
            progress_bar = ttk.Progressbar(progress_win, mode='indeterminate')
            progress_bar.pack(fill=tk.X, padx=20, pady=20)
            progress_bar.start()
            
            status_label = tk.Label(progress_win, text="Eliminando archivos...", font=("Arial", 9))
            status_label.pack()
            
            self.root.update()
            
            deleted_count = 0
            
            # Limpiar gráficos
            for file in GRAPHS_DIR.glob("*.png"):
                file.unlink()
                deleted_count += 1
            
            # Limpiar reportes
            for file in REPORTS_DIR.glob("*.xlsx"):
                file.unlink()
                deleted_count += 1
            
            for file in REPORTS_DIR.glob("*.txt"):
                file.unlink()
                deleted_count += 1
            
            # Limpiar imágenes procesadas
            for file in processed_files:
                file.unlink()
                deleted_count += 1
            
            progress_bar.stop()
            progress_win.destroy()
            
            messagebox.showinfo(
                "Limpieza Completada", 
                f"✓ Los resultados han sido eliminados.\n\n"
                f"Total de archivos eliminados: {deleted_count}"
            )
            
            self.update_results_info()
            
            # Actualizar lista de gráficos si estamos en esa pestaña
            self.refresh_graph_list()
            
        except Exception as e:
            if 'progress_win' in locals():
                progress_win.destroy()
            messagebox.showerror(
                "Error al Limpiar",
                f"Ocurrió un error al limpiar resultados:\n\n{str(e)}"
            )
    
    def open_folder(self, folder_path):
        """Abre una carpeta en el explorador."""
        import os
        import subprocess
        import platform
        
        folder_path = Path(folder_path)
        folder_path.mkdir(parents=True, exist_ok=True)
        
        if platform.system() == "Windows":
            # Usar explorer.exe para asegurar que se abra la carpeta
            subprocess.Popen(f'explorer "{folder_path}"')
        elif platform.system() == "Darwin":  # macOS
            os.system(f'open "{folder_path}"')
        else:  # Linux
            os.system(f'xdg-open "{folder_path}"')
    
    def open_backups_folder(self):
        """Abre la carpeta de respaldos."""
        from src.results_manager import ResultsManager
        
        manager = ResultsManager()
        backups_folder = manager.backups_dir
        
        # Crear carpeta si no existe
        backups_folder.mkdir(parents=True, exist_ok=True)
        
        # Verificar si hay respaldos
        backups = list(backups_folder.glob("backup_*"))
        
        if not backups:
            response = messagebox.askyesno(
                "Carpeta de Respaldos Vacía",
                f"La carpeta de respaldos está vacía.\n\n"
                f"Ubicación: {backups_folder}\n\n"
                f"¿Deseas abrirla de todas formas?"
            )
            if not response:
                return
        
        # Abrir carpeta
        import os
        import platform
        
        if platform.system() == "Windows":
            os.startfile(backups_folder)
        elif platform.system() == "Darwin":  # macOS
            os.system(f'open "{backups_folder}"')
        else:  # Linux
            os.system(f'xdg-open "{backups_folder}"')


def main():
    """Función principal para ejecutar la GUI."""
    root = tk.Tk()
    
    # Aplicar tema científico personalizado
    style = ttk.Style()
    style.theme_use('clam')
    
    # Colores profesionales para química/laboratorio
    style.configure('TNotebook', background='#f5f7fa', borderwidth=0)
    style.configure('TNotebook.Tab', 
                    background='#e8f5f1', 
                    foreground='#065f46',
                    padding=[20, 10],
                    font=('Segoe UI', 10, 'bold'))
    style.map('TNotebook.Tab',
              background=[('selected', '#047857')],
              foreground=[('selected', 'white')],
              expand=[('selected', [1, 1, 1, 0])])
    
    # Estilo de botones
    style.configure('TButton',
                    background='#059669',
                    foreground='white',
                    borderwidth=1,
                    relief='flat',
                    font=('Segoe UI', 10))
    style.map('TButton',
              background=[('active', '#047857')])
    
    # LabelFrames con estilo científico
    style.configure('TLabelframe',
                    background='#ffffff',
                    borderwidth=2,
                    relief='groove')
    style.configure('TLabelframe.Label',
                    background='#ffffff',
                    foreground='#2d3748',
                    font=('Segoe UI', 11, 'bold'))
    
    app = MicroplasticAnalysisGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
