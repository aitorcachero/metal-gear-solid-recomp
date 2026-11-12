@echo off
cd /d "%~dp0"
title Metal Gear Solid Recompiled - Modo Clasico 4:3 PlayStation

(
echo [video]
echo fullscreen = 1
echo aspect_ratio = "4:3"
echo internal_resolution = "1080p"
echo supersample = 1.0
echo geometry_correction = false
echo pgxp_depth_buffer = false
echo perspective_texturing = false
echo post_shader = "shaders/crt_scanlines.pfx"
echo vsync = "on"
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

powershell -NoProfile -Command "(Get-Content game.toml) -replace 'aspect_ratio = .*', 'aspect_ratio = \"4:3\"' -replace 'supersample = .*', 'supersample = 1.0' -replace 'internal_resolution = .*', 'internal_resolution = \"1080p\"' -replace 'fullscreen = .*', 'fullscreen = 1' | Set-Content game.toml -Encoding UTF8"
if exist "build-release\game.toml" (
    copy /y "game.toml" "build-release\game.toml" >nul 2>&1
)

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
