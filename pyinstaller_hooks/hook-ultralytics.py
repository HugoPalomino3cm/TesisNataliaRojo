# -*- coding: utf-8 -*-
"""
Hook personalizado para PyInstaller para el paquete ultralytics (YOLOv8)
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Recolectar todos los submódulos de ultralytics
hiddenimports = collect_submodules('ultralytics')

# Recolectar archivos de datos (modelos, configuración, etc.)
datas = collect_data_files('ultralytics')

# Agregar imports específicos que PyInstaller podría no detectar
hiddenimports += [
    'ultralytics.nn.modules',
    'ultralytics.nn.tasks',
    'ultralytics.utils',
    'ultralytics.engine',
]
