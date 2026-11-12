@echo off
cd /d "%~dp0"
title Configuracion de Metal Gear Solid Recompiled

if exist "Metal_Gear_Solid_Launcher.exe" (
    start "" "Metal_Gear_Solid_Launcher.exe"
    exit /b
)

if exist "build-release\Metal_Gear_Solid_Launcher.exe" (
    start "" "build-release\Metal_Gear_Solid_Launcher.exe"
    exit /b
)

if exist "launcher_mgs.py" (
    start "" py -3 "launcher_mgs.py"
    exit /b
)

if exist "MetalGearSolid.exe" (
    start "" "MetalGearSolid.exe"
    exit /b
)

if exist "build-release\Metal_Gear_Solid_Recompiled.exe" (
    cd /d "%~dp0build-release"
    start "" "Metal_Gear_Solid_Recompiled.exe"
    exit /b
)

echo [ERROR] No se encontro el configurador de Metal Gear Solid.
pause
exit /b
