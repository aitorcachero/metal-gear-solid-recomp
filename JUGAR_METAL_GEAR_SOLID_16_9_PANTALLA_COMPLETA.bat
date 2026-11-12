@echo off
cd /d "%~dp0metal-gear-solid-recomp\build-release"
title Metal Gear Solid Recompiled - Modo Panoramico 16:9 4K UHD 60FPS

:: 1. Configurar settings.toml para arranque inmediato en pantalla completa 16:9 4K
(
echo [video]
echo fullscreen = 1
echo aspect_ratio = "16:9"
echo internal_resolution = "4k"
echo supersample = 1.0
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
echo.
echo [disc]
echo path = "disc/Metal Gear Solid (Spain) (Disc 1).cue"
echo selected = 1
) > "settings.toml"

:: 2. Lanzar ejecutable optimizado
if exist "Metal_Gear_Solid_Recompiled.exe" (
    start "" "Metal_Gear_Solid_Recompiled.exe" --fullscreen --no-launcher %*
    exit /b
)
if exist "MetalGearSolid.exe" (
    start "" "MetalGearSolid.exe" --fullscreen --no-launcher %*
    exit /b
)

echo [ERROR] No se encontro el ejecutable de Metal Gear Solid en build-release.
pause
exit /b