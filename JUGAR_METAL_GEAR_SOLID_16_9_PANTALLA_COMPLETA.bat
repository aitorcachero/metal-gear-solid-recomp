@echo off
cd /d "%~dp0"
title Metal Gear Solid Recompiled - Modo Panoramico 16:9 4K UHD 60FPS

:: 1. Configurar settings.toml para arranque inmediato en pantalla completa 16:9 4K
(
echo [video]
echo fullscreen = 1
echo aspect_ratio = "16:9"
echo internal_resolution = "4k"
echo supersample = 2.0
echo geometry_correction = true
echo pgxp_depth_buffer = true
echo perspective_texturing = true
echo post_shader = "shaders/remaster_cinematic.pfx"
echo vsync = "off"
echo.
echo [audio]
echo spu_hq = true
echo.
echo [controller]
echo p1_device = "0300fa675e040000130b000023057801"
echo p1_mode = "analog"
echo p1_deadzone = 3276
echo multitap = false
echo multitap_analog = true
echo deadzone = 3276
echo default_mode = "analog"
) > "settings.toml"

if exist "build-release" (
    copy /y "settings.toml" "build-release\settings.toml" >nul 2>&1
)

:: 2. Actualizar game.toml
powershell -NoProfile -Command "(Get-Content game.toml) -replace 'aspect_ratio = .*', 'aspect_ratio = \"16:9\"' -replace 'supersample = .*', 'supersample = 2.0' -replace 'internal_resolution = .*', 'internal_resolution = \"4k\"' -replace 'fullscreen = .*', 'fullscreen = 1' | Set-Content game.toml -Encoding UTF8"
if exist "build-release\game.toml" (
    copy /y "game.toml" "build-release\game.toml" >nul 2>&1
)

:: 3. Lanzar ejecutable
if exist "MetalGearSolid.exe" (
    start "" "MetalGearSolid.exe" --fullscreen --no-launcher %*
    exit /b
)

if exist "Metal_Gear_Solid_Recompiled.exe" (
    start "" "Metal_Gear_Solid_Recompiled.exe" --fullscreen --no-launcher %*
    exit /b
)

if exist "build-release\Metal_Gear_Solid_Recompiled.exe" (
    cd /d "%~dp0build-release"
    start "" "Metal_Gear_Solid_Recompiled.exe" --fullscreen --no-launcher %*
    exit /b
)

echo [ERROR] No se encontro el ejecutable de Metal Gear Solid.
pause
exit /b
