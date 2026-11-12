#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Metal Gear Solid Recompiled — Asistente Automatizado de Instalación de Texturas HD
Permite arrastrar cualquier archivo comprimido (.zip, .rar, .7z) o carpeta de texturas
y lo instala automáticamente en la estructura de SLES-01734 activando el mod en state.toml.
"""

import os
import sys
import shutil
import zipfile
import subprocess
from pathlib import Path

GAME_ID = "SLES-01734"

def find_project_root():
    candidate = Path(__file__).resolve().parent.parent
    if (candidate / "Metal_Gear_Solid_Recompiled.exe").exists() or (candidate / "game.toml").exists():
        return candidate
    if (candidate / "build-release" / "Metal_Gear_Solid_Recompiled.exe").exists():
        return candidate
    return Path.cwd()

def ensure_state_enabled(root_dir: Path):
    mods_dir = root_dir / "mods"
    mods_dir.mkdir(parents=True, exist_ok=True)
    state_file = mods_dir / "state.toml"
    content = f"""format_version = 2

[[package]]
id = "psx.enhancement.hd-textures"
version = "1.0.0"

[[feature]]
package_id = "psx.enhancement.hd-textures"
id = "hd-textures"
enabled = true

[feature.values]
replacements = "true"
dump = "false"

[feature.resources]
pack = "mods/texture-packs/{GAME_ID}"
"""
    state_file.write_text(content, encoding="utf-8")
    print(f"[OK] Inyección de texturas HD activada en mods/state.toml")

def extract_archive(archive_path: Path, temp_dir: Path) -> bool:
    print(f"[*] Descomprimiendo: {archive_path.name}...")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Si es .zip estándar
    if archive_path.suffix.lower() == ".zip":
        try:
            with zipfile.ZipFile(archive_path, 'r') as zf:
                zf.extractall(temp_dir)
            return True
        except Exception as e:
            print(f"[!] Error extrayendo zip con Python ({e}), probando con tar...")

    # 2. Intentar con tar (nativo en Windows 10/11)
    res = subprocess.run(["tar", "-xf", str(archive_path), "-C", str(temp_dir)], capture_output=True)
    if res.returncode == 0:
        return True

    # 3. Intentar con PowerShell Expand-Archive
    if archive_path.suffix.lower() == ".zip":
        ps_cmd = f"Expand-Archive -Path '{archive_path}' -DestinationPath '{temp_dir}' -Force"
        res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True)
        return res.returncode == 0

    return False

def install_textures(source_dir: Path, target_dir: Path) -> int:
    target_dir.mkdir(parents=True, exist_ok=True)
    valid_exts = {".png", ".jpg", ".jpeg", ".webp"}
    count = 0

    # Buscar si hay una subcarpeta 'replacements'
    rep_dirs = [p for p in source_dir.rglob("replacements") if p.is_dir()]
    search_root = rep_dirs[0] if rep_dirs else source_dir

    # Si hay carpetas con nombres de serial (ej: SLUS-00594, SLES-01734)
    serials = [p for p in source_dir.rglob("SLUS-*") if p.is_dir()] + [p for p in source_dir.rglob("SLES-*") if p.is_dir()]
    if serials and not rep_dirs:
        search_root = serials[0]
        if (search_root / "replacements").is_dir():
            search_root = search_root / "replacements"

    print(f"[*] Buscando imágenes HD en: {search_root.name}...")

    for root, _, files in os.walk(search_root):
        for f in files:
            p = Path(root) / f
            if p.suffix.lower() in valid_exts:
                dest = target_dir / f
                try:
                    shutil.copy2(p, dest)
                    count += 1
                except Exception as e:
                    print(f"[!] Error copiando {f}: {e}")

    return count

def main():
    print("=" * 70)
    print("  Metal Gear Solid Recompiled — Instalador de Texturas HD")
    print("=" * 70)

    root_dir = find_project_root()
    replacements_dir = root_dir / "mods" / "texture-packs" / GAME_ID / "replacements"
    replacements_dir.mkdir(parents=True, exist_ok=True)

    if len(sys.argv) < 2:
        print("\nUso del instalador:")
        print("  1. Arrastra cualquier archivo comprimido (.zip, .rar, .7z) sobre")
        print("     'INSTALAR_PACK_TEXTURAS_HD.bat'.")
        print("  2. O copia manualmente tus archivos de textura en:")
        print(f"     {replacements_dir}")
        print("\nAbriendo la carpeta de reemplazos en el Explorador de Windows...")
        if os.name == 'nt':
            os.startfile(str(replacements_dir))
        ensure_state_enabled(root_dir)
        return

    input_path = Path(sys.argv[1]).resolve()
    if not input_path.exists():
        print(f"[!] Error: La ruta no existe: {input_path}")
        return

    temp_dir = root_dir / "mods" / "_temp_install"
    if temp_dir.exists():
        shutil.rmtree(temp_dir, ignore_errors=True)

    installed_count = 0

    if input_path.is_file():
        if input_path.suffix.lower() in {".zip", ".rar", ".7z", ".tar", ".gz"}:
            if extract_archive(input_path, temp_dir):
                installed_count = install_textures(temp_dir, replacements_dir)
            else:
                print(f"[!] Error: No se pudo descomprimir {input_path.name}")
        elif input_path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
            shutil.copy2(input_path, replacements_dir / input_path.name)
            installed_count = 1
    elif input_path.is_dir():
        installed_count = install_textures(input_path, replacements_dir)

    # Limpiar temporales
    if temp_dir.exists():
        shutil.rmtree(temp_dir, ignore_errors=True)

    if installed_count > 0:
        ensure_state_enabled(root_dir)
        print(f"\n[ÉXITO] Se han instalado {installed_count} texturas HD correctamente.")
        print(f"Destino: {replacements_dir}")
        print("El pack está activado y listo para Metal Gear Solid Recompiled.")
    else:
        print("\n[!] No se encontraron texturas compatibles en la ruta seleccionada.")

if __name__ == "__main__":
    main()
