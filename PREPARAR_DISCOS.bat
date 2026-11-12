@echo off
setlocal
cd /d "%~dp0"
title Preparador de Discos - Metal Gear Solid Recompiled

echo ==============================================================================
echo    METAL GEAR SOLID RECOMPILED - PREPARADOR DE DISCOS CHD A CUE/BIN
echo ==============================================================================
echo.

if not exist "tools\chdman.exe" (
    echo [ERROR] No se encontro tools\chdman.exe.
    pause
    exit /b
)

if not exist "disc" mkdir "disc"

:: Comprobar y extraer Disco 1
if exist "disc\Metal Gear Solid (Spain) (Disc 1).chd" (
    if not exist "disc\Metal Gear Solid (Spain) (Disc 1).cue" (
        echo [*] Descomprimiendo Disco 1 (Shadow Moses Infiltration)...
        tools\chdman.exe extractcd -i "disc\Metal Gear Solid (Spain) (Disc 1).chd" -o "disc\Metal Gear Solid (Spain) (Disc 1).cue" -ob "disc\Metal Gear Solid (Spain) (Disc 1).bin"
    ) else (
        echo [OK] Disco 1 ya esta preparado (CUE/BIN listo).
    )
)

:: Comprobar y extraer Disco 2
if exist "disc\Metal Gear Solid (Spain) (Disc 2).chd" (
    if not exist "disc\Metal Gear Solid (Spain) (Disc 2).cue" (
        echo [*] Descomprimiendo Disco 2 (Metal Gear REX & Final)...
        tools\chdman.exe extractcd -i "disc\Metal Gear Solid (Spain) (Disc 2).chd" -o "disc\Metal Gear Solid (Spain) (Disc 2).cue" -ob "disc\Metal Gear Solid (Spain) (Disc 2).bin"
    ) else (
        echo [OK] Disco 2 ya esta preparado (CUE/BIN listo).
    )
)

echo.
echo [COMPLETADO] Proceso finalizado. Ya puedes ejecutar JUGAR_METAL_GEAR_SOLID.bat!
echo.
pause
