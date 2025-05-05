@echo off
setlocal

REM Verifica si ya existe el entorno virtual
IF NOT EXIST "env\" (
    echo  Creando entorno virtual...
    python -m venv env
) ELSE (
    echo   El entorno virtual 'env' ya existe.
)

REM Activar el entorno virtual
call env\Scripts\activate

REM Instalar dependencias si existe requirements.txt
IF EXIST "requirements.txt" (
    echo  Instalando dependencias desde requirements.txt...
    pip install -r requirements.txt
) ELSE (
    echo  No se encontró el archivo requirements.txt
)

echo  Entorno virtual listo y dependencias instaladas.
pause
