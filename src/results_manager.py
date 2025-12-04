"""
Módulo para gestionar resultados del análisis de microplásticos.

Proporciona funcionalidades para crear respaldos, limpiar resultados
y obtener información sobre el espacio usado.
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config.config import GRAPHS_DIR, REPORTS_DIR, PROCESSED_IMAGES_DIR, PROJECT_ROOT


class ResultsManager:
    """Clase para gestionar los resultados del análisis."""
    
    def __init__(self):
        """Inicializa el gestor de resultados."""
        self.graphs_dir = GRAPHS_DIR
        self.reports_dir = REPORTS_DIR
        self.processed_dir = PROCESSED_IMAGES_DIR
        self.backups_dir = PROJECT_ROOT / "backups"
        
        # Crear directorios si no existen
        self.backups_dir.mkdir(parents=True, exist_ok=True)
    
    def get_folder_size(self, folder_path: Path) -> float:
        """
        Calcula el tamaño total de una carpeta en MB.
        
        Args:
            folder_path: Ruta a la carpeta.
            
        Returns:
            Tamaño en megabytes.
        """
        if not folder_path.exists():
            return 0.0
        
        total_size = 0
        for file in folder_path.rglob('*'):
            if file.is_file():
                total_size += file.stat().st_size
        
        return total_size / (1024 * 1024)  # Convertir a MB
    
    def count_files(self, folder_path: Path, extension: str = None) -> int:
        """
        Cuenta archivos en una carpeta.
        
        Args:
            folder_path: Ruta a la carpeta.
            extension: Extensión específica (sin punto). Si es None, cuenta todos.
            
        Returns:
            Número de archivos.
        """
        if not folder_path.exists():
            return 0
        
        if extension:
            return len(list(folder_path.glob(f"*.{extension}")))
        else:
            return len([f for f in folder_path.iterdir() 
                       if f.is_file() and f.name not in [".gitkeep", "INSTRUCCIONES.md"]])
