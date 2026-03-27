@echo off
REM Iniciar Monitor de Sincronización - Barein GP
REM Este script ejecuta el monitor sin mostrar la terminal

cd /d C:\Nuevo

REM Ejecutar en background usando VBScript
powershell -Command "Start-Process python -ArgumentList 'monitor_sincronizacion.py' -WindowStyle Hidden"

REM Mostrar mensaje de confirmación
echo.
echo ========================================
echo Monitor de Sincronización Iniciado
echo ========================================
echo El archivo Venta_consolidado.xlsx será sincronizado automáticamente a OneDrive
echo.
echo Para detener el monitor, abre el Administrador de tareas (Ctrl+Shift+Esc)
echo y busca la ventana de Python
echo.
pause
