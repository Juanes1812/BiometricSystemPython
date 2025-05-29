import os
import json
from pathlib import Path

class GeneradorConfig:
    def __init__(self):
        self.estructura = {
            "main_script": "App.py",
            "assets": {
                "voces": "assets/voces",
                "rostros": "assets/rostros"
            },
            "data": {
                "usuarios": "data/usuarios.txt"
            },
            "utils": "utils",
            "excluir": ["venv", ".gitignore", "__pycache__"]
        }

    def generar_config(self):
        """Genera la configuración completa para PyInstaller con protección contra IndexError"""
        config = {
            "script": self.estructura["main_script"],
            "datas": self._obtener_recursos(),
            "hiddenimports": self._obtener_imports_ocultos(),
            "binaries": [],
            "runtime_tmpdir": "."  # Nuevo: evita problemas con rutas temporales
        }
        
        # Añadir protección para dlib
        if not any("dlib" in imp for imp in config["hiddenimports"]):
            config["hiddenimports"].append("dlib")
        
        with open("config_pyinstaller.json", "w") as f:
            json.dump(config, f, indent=4)
        
        self._generar_spec_file_mejorada(config)  # Usamos la nueva versión
        self._generar_build_script_actualizado()
        
        print("✅ Configuración generada con éxito!")
        print("📄 Archivos creados: config_pyinstaller.json, build.spec, build.bat")

    def _obtener_recursos(self):
        """Obtiene todos los recursos necesarios con verificación de existencia"""
        recursos = []
        
        # Assets con verificación
        for tipo in ["voces", "rostros"]:
            dir_assets = self.estructura["assets"][tipo]
            if os.path.exists(dir_assets):
                for root, _, files in os.walk(dir_assets):
                    for f in files:
                        src = os.path.join(root, f)
                        if os.path.exists(src):  # Verificación adicional
                            dest = os.path.relpath(root, ".")
                            recursos.append((src, dest))
        
        # Data con verificación
        data_file = self.estructura["data"]["usuarios"]
        if os.path.exists(data_file):
            recursos.append((data_file, "data"))
        
        # Utils con verificación
        utils_dir = self.estructura["utils"]
        if os.path.exists(utils_dir):
            for root, _, files in os.walk(utils_dir):
                for f in files:
                    if f.endswith(".py"):
                        src = os.path.join(root, f)
                        if os.path.exists(src):
                            dest = os.path.relpath(root, ".")
                            recursos.append((src, dest))
        
        # Añadir datos de dlib si existen
        dlib_data_path = os.path.join("venv", "Lib", "site-packages", "dlib", "data")
        if os.path.exists(dlib_data_path):
            for root, _, files in os.walk(dlib_data_path):
                for f in files:
                    src = os.path.join(root, f)
                    dest = os.path.relpath(root, "venv/Lib/site-packages/dlib")
                    recursos.append((src, dest))
        
        return recursos

    def _obtener_imports_ocultos(self):
        """Detecta módulos en utils con protección adicional"""
        imports = []
        utils_dir = self.estructura["utils"]
        
        # Módulos esenciales para evitar IndexError
        essential_imports = [
            "cv2", "pyaudio", "dlib",
            "numpy.core._methods", "numpy.lib.format",
            "tkinter", "PIL"
        ]
        
        if os.path.exists(utils_dir):
            for root, _, files in os.walk(utils_dir):
                for f in files:
                    if f.endswith(".py"):
                        mod_name = os.path.splitext(f)[0]
                        imports.append(f"utils.{mod_name}")
        
        return imports + essential_imports

    def _generar_spec_file_mejorada(self, config):
        """Genera el archivo .spec con protección contra IndexError"""
        spec_content = f"""# -*- mode: python -*-
from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os

block_cipher = None

# Configuración especial para evitar IndexError
def safe_collect_data_files(package):
    try:
        return collect_data_files(package)
    except:
        return []

a = Analysis(
    ['{config["script"]}'],
    pathex=[],
    binaries={config["binaries"]},
    datas={config["datas"]},
    hiddenimports={config["hiddenimports"]},
    hookspath=[],
    runtime_hooks=[],
    excludes=['FixTk', 'tcl', 'tk', '_tkinter', 'tkinter', 'Tkinter', 'typing', 'typing_extensions'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    runtime_tmpdir="{config["runtime_tmpdir"]}"
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

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
    runtime_tmpdir=None,
    console=False,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None
)
"""
        with open("build.spec", "w") as f:
            f.write(spec_content)

    def _generar_build_script_actualizado(self):
        """Genera el script de construcción con gestión de typing y optimizaciones"""
        bat_content = """@echo off
:: Limpieza previa
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

:: Actualizar herramientas esenciales
python -m pip install --upgrade pip setuptools wheel

:: ----- SOLUCIÓN PARA TYPING -----
:: 1. Desinstalar typing y bloquearlo
python -m pip uninstall typing typing-extensions -y
echo typing==0.0.0 > constraints.txt
echo typing-extensions==0.0.0 >> constraints.txt

:: 2. Instalar PyInstaller sin conflictos
pip install --force-reinstall pyinstaller -c constraints.txt

:: ----- INSTALACIÓN INTELIGENTE -----
:: Prioriza binarios precompilados
if exist "requirements.txt" (
    pip install -r requirements.txt -c constraints.txt --no-cache-dir --prefer-binary
) else (
    echo Instalando dependencias básicas...
    pip install numpy opencv-python dlib face-recognition pyaudio -c constraints.txt --prefer-binary
)

:: ----- COMPILACIÓN SEGURA -----
:: Excluye typing explícitamente y usa hooks personalizados
pyinstaller build.spec --onefile --windowed --clean ^
    --runtime-tmpdir "." ^
    --exclude-module typing ^
    --exclude-module typing_extensions ^
    --additional-hooks-dir=. || (
    echo Error al construir el ejecutable
    pause
    exit /b 1
)

:: Verificación final
if exist "dist\\BiometricApp.exe" (
    echo ¡Compilación exitosa! ^(Sin typing^)
    dir /b dist
) else (
    echo Error: No se generó el ejecutable
)
pause
"""
        with open("build.bat", "w", encoding='utf-8') as f:
            f.write(bat_content)

if __name__ == "__main__":
    generador = GeneradorConfig()
    generador.generar_config()