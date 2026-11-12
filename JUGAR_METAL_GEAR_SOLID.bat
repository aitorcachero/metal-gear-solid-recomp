@echo off
cd /d "%~dp0"
title Metal Gear Solid Recompiled - Master Launcher

:: 1. Lanzador grafico dedicado
if exist "Metal_Gear_Solid_Launcher.exe" (
    start "" "Metal_Gear_Solid_Launcher.exe" %*
    exit /b
)
if exist "build-release\Metal_Gear_Solid_Launcher.exe" (
    start "" "build-release\Metal_Gear_Solid_Launcher.exe" %*
    exit /b
)

:: 2. Lanzador Python directo
if exist "launcher_mgs.py" (
    start "" py -3 "launcher_mgs.py" %*
    exit /b
)

:: 3. Lanzador nativo C++ integrado
if exist "MetalGearSolid.exe" (
    start "" "MetalGearSolid.exe" %*
    exit /b
)

:: 4. Ejecutable en build-release
if exist "build-release\Metal_Gear_Solid_Recompiled.exe" (
    cd /d "%~dp0build-release"
    start "" "Metal_Gear_Solid_Recompiled.exe" %*
    exit /b
)

echo [ERROR] No se encontro el ejecutable o lanzador de Metal Gear Solid.
pause
exit /b
