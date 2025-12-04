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
from pathlib import Path
import queue
from PIL import Image, ImageTk

# Agregar directorio src al path
sys.path.append(str(Path(__file__).parent))

from src.image_processing import ImageProcessor
from src.statistical_analysis import StatisticalAnalyzer
from src.visualization import DataVisualizer
from config.config import (
    RAW_IMAGES_DIR, PROCESSED_IMAGES_DIR, GRAPHS_DIR, 
    REPORTS_DIR, IMAGE_PARAMS
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
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=(10, 15))
        
        # Pestaña 1: Configuración
        config_frame = ttk.Frame(notebook)
        notebook.add(config_frame, text="⚙️ Configuración")
        self.create_config_tab(config_frame)
        
        # Pestaña 2: Análisis
        analysis_frame = ttk.Frame(notebook)
        notebook.add(analysis_frame, text="🔬 Análisis")
        self.create_analysis_tab(analysis_frame)
        
        # Pestaña 3: Visualización de Gráficos
        viewer_frame = ttk.Frame(notebook)
        notebook.add(viewer_frame, text="📊 Ver Gráficos")
        self.create_viewer_tab(viewer_frame)
        
        # Pestaña 4: Gestión
        management_frame = ttk.Frame(notebook)
        notebook.add(management_frame, text="📁 Gestión de Resultados")
        self.create_management_tab(management_frame)
    
    def create_config_tab(self, parent):
        """Crea la pestaña de configuración."""
        
        # Frame de imágenes
        img_frame = ttk.LabelFrame(parent, text="📸 Selección de Imágenes", padding=15)
        img_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame de botones
        btn_frame = ttk.Frame(img_frame)
        btn_frame.pack(pady=10)
        
        # Botón para buscar imágenes
        btn_browse = ttk.Button(
            btn_frame,
            text="📂 Buscar Imágenes",
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
            text="📁 Usar Carpeta por Defecto (data/raw_images)",
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
        """Abre diálogo para seleccionar imágenes."""
        files = filedialog.askopenfilenames(
            title="Seleccionar imágenes microscópicas",
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.tif *.tiff *.bmp"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if files:
            self.image_files = list(files)
            self.update_image_list()
    
    def load_default_images(self):
        """Carga imágenes de la carpeta por defecto."""
        image_extensions = ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.bmp']
        self.image_files = []
        
        for ext in image_extensions:
            self.image_files.extend(RAW_IMAGES_DIR.glob(f'*{ext}'))
            self.image_files.extend(RAW_IMAGES_DIR.glob(f'*{ext.upper()}'))
        
        self.image_files = [str(f) for f in self.image_files]
        self.update_image_list()
        
        if self.image_files:
            self.log_console(f"✓ Cargadas {len(self.image_files)} imágenes de {RAW_IMAGES_DIR}\n")
        else:
            self.log_console(f"⚠️ No se encontraron imágenes en {RAW_IMAGES_DIR}\n")
    
    def update_image_list(self):
        """Actualiza la lista de imágenes en la interfaz."""
        self.image_listbox.delete(0, tk.END)
        for img in self.image_files:
            filename = Path(img).name
            self.image_listbox.insert(tk.END, f"  📷 {filename}")
    
    def remove_selected_images(self):
        """Elimina las imágenes seleccionadas de la lista."""
        selected_indices = self.image_listbox.curselection()
        
        if not selected_indices:
            messagebox.showwarning(
                "Sin Selección",
                "Por favor, selecciona una o más imágenes para eliminar.\n\n"
                "Tip: Usa Ctrl+Click para seleccionar múltiples imágenes."
            )
            return
        
        # Confirmar eliminación
        count = len(selected_indices)
        if not messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Deseas eliminar {count} imagen(es) de la lista?\n\n"
            "Nota: Solo se eliminan de la lista, no del disco."
        ):
            return
        
        # Eliminar en orden inverso para no alterar índices
        for index in reversed(selected_indices):
            del self.image_files[index]
        
        self.update_image_list()
        self.log_console(f"✓ {count} imagen(es) eliminada(s) de la lista\n")
    
    def clear_all_images(self):
        """Limpia todas las imágenes de la lista."""
        if not self.image_files:
            messagebox.showinfo("Lista Vacía", "No hay imágenes en la lista.")
            return
        
        count = len(self.image_files)
        if messagebox.askyesno(
            "Limpiar Todas",
            f"¿Deseas eliminar todas las {count} imágenes de la lista?\n\n"
            "Nota: Solo se eliminan de la lista, no del disco."
        ):
            self.image_files = []
            self.update_image_list()
            self.log_console(f"✓ Todas las imágenes eliminadas de la lista\n")
    
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
            messagebox.showwarning(
                "Sin Imágenes",
                "Por favor, selecciona o carga imágenes antes de iniciar el análisis."
            )
            return
        
        if self.analysis_running:
            messagebox.showinfo("Análisis en Curso", "Ya hay un análisis en ejecución.")
            return
        
        # Confirmar calibración
        response = messagebox.askyesno(
            "Confirmar Calibración",
            f"Factor de calibración: {self.pixels_to_um.get()} μm/píxel\n\n"
            "¿Es correcto este valor?"
        )
        
        if not response:
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
            self.message_queue.put("🔬 INICIANDO ANÁLISIS DE MICROPLÁSTICOS\n")
            self.message_queue.put("="*60 + "\n\n")
            
            # Crear sistema inline
            class MicroplasticAnalysisSystem:
                def __init__(self, pixels_to_um):
                    self.processor = ImageProcessor(pixels_to_um)
                    self.analyzer = StatisticalAnalyzer()
                    self.visualizer = DataVisualizer()
                    self.results = {}
                
                def analyze_single_sample(self, image_path, sample_id):
                    """Analiza una única muestra."""
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
                    
                    # 2. Convertir a DataFrame
                    self.message_queue.put("2. Analizando datos estadísticos...\n")
                    df = self.analyzer.particles_to_dataframe(particles, sample_id)
                    
                    # 3. Generar visualizaciones
                    self.message_queue.put("3. Generando visualizaciones...\n")
                    
                    size_plot_path = GRAPHS_DIR / f"{sample_id}_size_distribution.png"
                    self.visualizer.plot_size_distribution(df, sample_id, str(size_plot_path))
                    self.message_queue.put(f"   ✓ Guardado: {size_plot_path.name}\n")
                    
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
                            'Área_media_μm2': df['area_um2'].mean(),
                            'Área_std_μm2': df['area_um2'].std(),
                            'Diámetro_medio_μm': df['equivalent_diameter_um'].mean(),
                            'Diámetro_std_μm': df['equivalent_diameter_um'].std(),
                            'Relación_aspecto_media': df['aspect_ratio'].mean(),
                            'Excentricidad_media': df['eccentricity'].mean(),
                        }
                        summary_stats.append(stats)
                    
                    summary_df = pd.DataFrame(summary_stats)
                    summary_path = REPORTS_DIR / "summary_statistics.xlsx"
                    summary_df.to_excel(summary_path, index=False)
                    self.message_queue.put(f"✓ Estadísticos resumen guardados: {summary_path.name}\n")
            
            # Vincular message_queue al sistema
            MicroplasticAnalysisSystem.message_queue = self.message_queue
            
            # Crear sistema
            system = MicroplasticAnalysisSystem(pixels_to_um=self.pixels_to_um.get())
            
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
            self.message_queue.put("✓ ANÁLISIS COMPLETADO EXITOSAMENTE\n")
            self.message_queue.put("="*60 + "\n")
            
            self.root.after(0, lambda: messagebox.showinfo(
                "Análisis Completado",
                "El análisis ha finalizado exitosamente.\n\n"
                f"Resultados guardados en:\n"
                f"• Gráficos: {GRAPHS_DIR}\n"
                f"• Reportes: {REPORTS_DIR}"
            ))
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            self.message_queue.put(f"\n❌ ERROR: {str(e)}\n")
            self.message_queue.put(f"{error_details}\n")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error durante el análisis:\n{str(e)}"))
        
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
        if messagebox.askyesno("Detener Análisis", "¿Seguro que deseas detener el análisis?"):
            self.analysis_running = False
            self.log_console("\n⚠️ Análisis detenido por el usuario.\n")
    
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
        import platform
        
        folder_path = Path(folder_path)
        folder_path.mkdir(parents=True, exist_ok=True)
        
        if platform.system() == "Windows":
            os.startfile(folder_path)
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
