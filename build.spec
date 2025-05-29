# -*- mode: python -*-
from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os

block_cipher = None

# Configuraci�n especial para evitar IndexError
def safe_collect_data_files(package):
    try:
        return collect_data_files(package)
    except:
        return []

a = Analysis(
    ['App.py'],
    pathex=[],
    binaries=[],
    datas=[
    ('assets/*', 'assets'),
    ('data/*', 'data'),
    ('venv/Lib/site-packages/dlib/data/shape_predictor_68_face_landmarks.dat', 'dlib/data')
    ],
    hiddenimports=['pyaudio', 'cv2', 'dlib'],
    hookspath=['.'],  # Hooks personalizados
    runtime_hooks=[],
    excludes=['typing', 'typing_extensions'],  # Excluye estos módulos
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

# En la sección EXE:
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='BiometricApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=".",  # Directorio temporal
    console=False,      # Modo sin consola
    icon='assets/icon.ico'
)
