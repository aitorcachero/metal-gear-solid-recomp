@echo off
cd /d "%~dp0"
title Metal Gear Solid Recompiled - Master Launcher

if exist "Metal_Gear_Solid_Launcher.exe" (
    start "" "Metal_Gear_Solid_Launcher.exe" %*
    exit /b
)
if exist "metal-gear-solid-recomp\build-release\Metal_Gear_Solid_Launcher.exe" (
    cd /d "%~dp0metal-gear-solid-recomp\build-release"
    start "" "Metal_Gear_Solid_Launcher.exe" %*
    exit /b
)
if exist "metal-gear-solid-recomp\Metal_Gear_Solid_Launcher.exe" (
    cd /d "%~dp0metal-gear-solid-recomp"
    start "" "Metal_Gear_Solid_Launcher.exe" %*
    exit /b
)
pause
exit /b