# -*- mode: python ; coding: utf-8 -*-
"""
Archivo de especificación de PyInstaller para Análisis de Microplásticos
Este archivo permite mayor control sobre cómo se compila el ejecutable.

Uso:
    pyinstaller build.spec
"""

import sys
from pathlib import Path

block_cipher = None

# Archivos de datos a incluir
datas = [
    ('config', 'config'),
    ('src', 'src'),
    ('yolov8n.pt', '.'),
]

# Imports ocultos que PyInstaller podría no detectar
hiddenimports = [
    'PIL._tkinter_finder',
    'sklearn.utils._weight_vector',
    'cv2',
    'numpy',
    'pandas',
    'matplotlib',
    'seaborn',
    'scipy',
    'ultralytics',
    'torch',
    'torchvision',
]

# Binarios adicionales (si los necesitas)
binaries = []

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'pytest',
        'unittest',
        '_pytest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AnalisisMicroplasticos',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Comprimir el ejecutable
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin ventana de consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if Path('icon.ico').exists() else None,
)
