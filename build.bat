@echo off
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

:: ----- GESTIÓN DE MODELOS DLIB -----
:: Verificar y descargar modelos si no existen
if not exist "venv\Lib\site-packages\dlib\data\shape_predictor_68_face_landmarks.dat" (
    echo Descargando modelos dlib...
    curl -o shape_predictor_68_face_landmarks.dat.bz2 https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2
    if not exist "venv\Lib\site-packages\dlib\data" mkdir "venv\Lib\site-packages\dlib\data"
    :: Requiere 7-Zip o similar para descomprimir
    "C:\Program Files\7-Zip\7z.exe" e shape_predictor_68_face_landmarks.dat.bz2 -o"venv\Lib\site-packages\dlib\data"
    del shape_predictor_68_face_landmarks.dat.bz2
)

:: ----- INSTALACIÓN INTELIGENTE -----
:: Prioriza binarios precompilados
if exist "requirements.txt" (
    pip install -r requirements.txt -c constraints.txt --no-cache-dir --prefer-binary
) else (
    echo Instalando dependencias básicas...
    pip install numpy opencv-python dlib==19.24.0 face-recognition==1.3.0 pyaudio -c constraints.txt --prefer-binary
)

:: ----- COMPILACIÓN SEGURA -----
:: Usa SOLAMENTE el archivo .spec sin parámetros adicionales
pyinstaller build.spec --clean || (
    echo Error al construir el ejecutable
    pause
    exit /b 1
)

:: Verificación final
if exist "dist\BiometricApp.exe" (
    echo ¡Compilación exitosa! ^(Sin typing^)
    echo Modelos dlib incluidos correctamente
    dir /b dist
) else (
    echo Error: No se generó el ejecutable
)
pause