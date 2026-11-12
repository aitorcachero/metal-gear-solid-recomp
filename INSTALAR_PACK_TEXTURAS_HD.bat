@echo off
setlocal
title Instalador de Texturas HD - Metal Gear Solid Recompiled
cd /d "%~dp0"

echo ==============================================================================
echo    METAL GEAR SOLID RECOMPILED - INSTALADOR DE TEXTURAS HD EN 1-CLIC
echo ==============================================================================
echo.

if not "%~1"=="" (
    python tools\installer_texture_pack.py "%~1"
) else (
    python tools\installer_texture_pack.py
)

echo.
echo Presiona cualquier tecla para salir...
pause >nul
