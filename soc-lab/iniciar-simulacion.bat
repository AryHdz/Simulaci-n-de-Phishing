@echo off
cd /d "%~dp0"

echo Iniciando Nexora SOC Lab en modo local...
echo.

where python >nul 2>nul
if not errorlevel 1 (
  python -m pip show flask >nul 2>nul
  if errorlevel 1 (
    echo Falta Flask. Instalando dependencias locales del proyecto...
    python -m pip install -r requirements.txt
    if errorlevel 1 goto error
  )
  python app.py
  goto end
)

where py >nul 2>nul
if not errorlevel 1 (
  py -m pip show flask >nul 2>nul
  if errorlevel 1 (
    echo Falta Flask. Instalando dependencias locales del proyecto...
    py -m pip install -r requirements.txt
    if errorlevel 1 goto error
  )
  py app.py
  goto end
)

echo No se encontro Python en este equipo.
echo Instala Python desde https://www.python.org/downloads/
echo Marca "Add python.exe to PATH" durante la instalacion.
goto end

:error
echo.
echo No se pudo iniciar la simulacion.
echo Revisa que Python este instalado y que tengas internet solo para instalar Flask la primera vez.

:end
echo.
pause
