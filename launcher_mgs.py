#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Metal Gear Solid Recompiled — Master Launcher
Inspirado en el layout y estilo visual de Terranigma / Illusion of Time SNES Recomp.
Paleta Deep Slate Navy (#0A0F1D / #101828) + Tactical Kojima Orange (#FF7600) + HUD Cyan (#38BDF8).
Apertura automática en Pantalla Completa con soporte para F11, Enter y Esc.
"""

import os
import sys
import subprocess
import ctypes
from pathlib import Path
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image

# ── Paleta de color SNES Recomp / Terranigma ──
C_BG_DEEP       = "#0a0f1d"   # Fondo ultra-oscuro Deep Navy
C_CARD_BG       = "#101828"   # Tarjetas Slate Blue
C_CARD_HOVER    = "#16233b"   # Hover en tarjetas
C_BORDER        = "#1e293b"   # Borde sutil pizarra
C_BORDER_ACTIVE = "#334155"   # Borde enfocado
C_ORANGE        = "#ff7600"   # Naranja táctico Metal Gear Solid
C_ORANGE_HOVER  = "#ff8c26"   # Naranja hover
C_ORANGE_DARK   = "#d95d00"   # Naranja click
C_TEXT_WHITE    = "#f8fafc"   # Texto blanco nítido
C_TEXT_MUTED    = "#94a3b8"   # Texto secundario pizarra
C_CYAN          = "#38bdf8"   # Acentos cian HUD
C_GREEN         = "#22c55e"   # Estado activo OK
C_GOLD          = "#fbbf24"   # Acento dorado

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent

def find_game_environment():
    """Localiza el ejecutable recompilado nativo y el directorio de trabajo."""
    candidates = [
        (BASE_DIR / "metal-gear-solid-recomp" / "build-release" / "Metal_Gear_Solid_Recompiled.exe", BASE_DIR / "metal-gear-solid-recomp" / "build-release"),
        (BASE_DIR / "build-release" / "Metal_Gear_Solid_Recompiled.exe", BASE_DIR / "build-release"),
        (BASE_DIR / "Metal_Gear_Solid_Recompiled.exe", BASE_DIR),
        (BASE_DIR / "MetalGearSolid.exe", BASE_DIR),
        (BASE_DIR.parent / "metal-gear-solid-recomp" / "build-release" / "Metal_Gear_Solid_Recompiled.exe", BASE_DIR.parent / "metal-gear-solid-recomp" / "build-release"),
    ]
    for exe, work_dir in candidates:
        if exe.exists() and (work_dir / "disc").exists():
            return exe.resolve(), work_dir.resolve()
    for exe, work_dir in candidates:
        if exe.exists():
            return exe.resolve(), work_dir.resolve()
    return (BASE_DIR / "Metal_Gear_Solid_Recompiled.exe").resolve(), BASE_DIR.resolve()

GAME_EXE, GAME_WORK_DIR = find_game_environment()

DISCS_INFO = [
    {
        "id": 1,
        "title": "DISCO 1: Infiltración en Shadow Moses",
        "cue": "disc/Metal Gear Solid (Spain) (Disc 1).cue",
        "desc": "El muelle de inserción, el helipuerto de vigilancia, el hangar de tanques, combate con Vulcan Raven, Psycho Mantis y Sniper Wolf."
    },
    {
        "id": 2,
        "title": "DISCO 2: Fase Final y Metal Gear REX",
        "cue": "disc/Metal Gear Solid (Spain) (Disc 2).cue",
        "desc": "Las Torres de Comunicación, descenso en rápel, alto horno, el hangar subterráneo de Metal Gear REX y la persecución en jeep con Liquid Snake."
    }
]

def detect_gamepad_name():
    """Detecta mandos de juego conectados en Windows mediante XInput o WinMM."""
    try:
        xinput = ctypes.windll.xinput1_4
        class XINPUT_STATE(ctypes.Structure):
            _fields_ = [("dwPacketNumber", ctypes.c_ulong), ("Gamepad", ctypes.c_ubyte * 12)]
        for i in range(4):
            state = XINPUT_STATE()
            if xinput.XInputGetState(i, ctypes.byref(state)) == 0:
                return f"🎮 Mando Xbox / XInput (Puerto {i+1}) [DualShock Analógico]"
    except Exception:
        pass

    try:
        num_devs = ctypes.windll.winmm.joyGetNumDevs()
        if num_devs > 0:
            return "🎮 Mando PlayStation / DirectInput [DualShock Analógico]"
    except Exception:
        pass

    return "⌨️ Teclado y Ratón [Mapeo Táctico MGS1]"

def parse_toml(path: Path) -> dict:
    data = {}
    cur = "root"
    if not path.exists():
        return data
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                l = line.strip()
                if not l or l.startswith("#"): continue
                if l.startswith("[") and l.endswith("]"):
                    cur = l[1:-1].strip()
                    if cur not in data: data[cur] = {}
                    continue
                if "=" in l:
                    k, v = l.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if cur not in data: data[cur] = {}
                    data[cur][k] = v
    except Exception:
        pass
    return data

def save_mod_state(work_dirs: list, hd_textures_enabled: bool, dump_enabled: bool):
    for base in work_dirs:
        try:
            mods_dir = base / "mods"
            mods_dir.mkdir(parents=True, exist_ok=True)
            tex_pack_dir = mods_dir / "texture-packs" / "SLES-01734"
            (tex_pack_dir / "replacements").mkdir(parents=True, exist_ok=True)
            (tex_pack_dir / "dumps").mkdir(parents=True, exist_ok=True)

            state_file = mods_dir / "state.toml"
            content = f"""format_version = 2

[[package]]
id = "psx.enhancement.hd-textures"
version = "1.0.0"

[[feature]]
package_id = "psx.enhancement.hd-textures"
id = "hd-textures"
enabled = {'true' if (hd_textures_enabled or dump_enabled) else 'false'}

[feature.values]
replacements = "{'true' if hd_textures_enabled else 'false'}"
dump = "{'true' if dump_enabled else 'false'}"

[feature.resources]
pack = "mods/texture-packs/SLES-01734"
"""
            state_file.write_text(content, encoding="utf-8")
        except Exception:
            pass


class MGSModernLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Metal Gear Solid — Master Launcher (Recompiled PC Edition)")
        self.configure(fg_color=C_BG_DEEP)

        # ── PANTALLA COMPLETA AL INICIO (Requisito usuario) ──
        self.is_fullscreen = True
        try:
            self.attributes("-fullscreen", True)
        except Exception:
            try:
                self.state("zoomed")
            except Exception:
                pass

        # Atajos de teclado
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Return>", lambda e: self.launch_game())
        self.bind("<Escape>", lambda e: self.confirm_exit())

        # Variables de Configuración
        self.selected_disc = tk.IntVar(value=1)
        self.game_fullscreen = tk.IntVar(value=1)          # 1 = Borderless Fullscreen, 0 = Windowed, 2 = Exclusive
        self.aspect_ratio = tk.StringVar(value="16:9")     # 16:9, 21:9, 4:3
        self.resolution = tk.StringVar(value="4k")         # 4k, 1440p, 1080p, 720p, 240p
        self.supersample = tk.StringVar(value="2.0")       # 2.0, 1.5, 1.0
        self.pgxp_enabled = tk.BooleanVar(value=True)      # PGXP Anti-jitter
        self.pgxp_depth = tk.BooleanVar(value=True)        # PGXP Depth Buffer
        self.perspective_enabled = tk.BooleanVar(value=True) # Perspective correction
        self.texture_filter = tk.StringVar(value="bilinear") # bilinear, nearest
        self.anisotropic_filter = tk.StringVar(value="16") # 16, 8, 4, 0
        self.post_shader = tk.StringVar(value="shaders/remaster_cinematic.pfx")
        self.fmv_smoothing = tk.BooleanVar(value=True)     # FMV Chroma smoothing
        self.vsync_enabled = tk.StringVar(value="off")     # off, on
        self.spu_hq_enabled = tk.BooleanVar(value=True)    # SPU HQ 48 kHz
        self.analog_mode = tk.StringVar(value="analog")    # analog, digital
        self.deadzone_val = tk.IntVar(value=10)            # Stick deadzone %
        self.hd_textures_enabled = tk.BooleanVar(value=True)
        self.texture_dump_enabled = tk.BooleanVar(value=False)
        self.active_preset_name = tk.StringVar(value="🌟 4K UHD Master Edition (16:9)")

        self.load_existing_toml()
        self.build_ui()

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)
        if hasattr(self, "btn_fs_toggle"):
            txt = "🗖 Salir de Pantalla Completa (F11)" if self.is_fullscreen else "⛶ Pantalla Completa (F11)"
            self.btn_fs_toggle.configure(text=txt)

    def confirm_exit(self):
        self.destroy()

    def load_existing_toml(self):
        toml_path = GAME_WORK_DIR / "game.toml"
        data = parse_toml(toml_path)
        if "video" in data:
            v = data["video"]
            if "fullscreen" in v:
                try:
                    self.game_fullscreen.set(int(v["fullscreen"]))
                except ValueError:
                    self.game_fullscreen.set(1 if v["fullscreen"].lower() == "true" else 0)
            if "aspect_ratio" in v: self.aspect_ratio.set(v["aspect_ratio"])
            if "internal_resolution" in v: self.resolution.set(v["internal_resolution"])
            if "supersample" in v: self.supersample.set(v["supersample"])
            if "pgxp_depth_buffer" in v: self.pgxp_depth.set(v["pgxp_depth_buffer"].lower() == "true")
            if "geometry_correction" in v: self.pgxp_enabled.set(v["geometry_correction"].lower() == "true")
            if "perspective_texturing" in v: self.perspective_enabled.set(v["perspective_texturing"].lower() == "true")
            if "texture_filtering" in v: self.texture_filter.set(v["texture_filtering"])
            if "anisotropic_filtering" in v: self.anisotropic_filter.set(str(v["anisotropic_filtering"]))
            if "post_shader" in v: self.post_shader.set(v["post_shader"])
            if "vsync" in v: self.vsync_enabled.set(v["vsync"])
        if "audio" in data:
            a = data["audio"]
            if "spu_hq" in a: self.spu_hq_enabled.set(a["spu_hq"].lower() == "true")
        if "controller" in data:
            c = data["controller"]
            if "default_mode" in c: self.analog_mode.set(c["default_mode"])

    def build_ui(self):
        # Grid raíz 2 filas (contenido expandible, footer fijo)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=0, minsize=400)
        self.grid_columnconfigure(1, weight=1)

        # ══════════════════════════════════════════════════════
        # ── 1. COLUMNA IZQUIERDA: PÓSTER Y ESTADO TÁCTICO ──
        # ══════════════════════════════════════════════════════
        self.left_frame = ctk.CTkFrame(self, fg_color=C_CARD_BG, corner_radius=0, border_width=1, border_color=C_BORDER)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(0, weight=1)

        # Contenedor del póster
        poster_candidates = [
            BASE_DIR / "assets" / "img" / "poster.png",
            BASE_DIR / "build-release" / "assets" / "img" / "poster.png",
            GAME_WORK_DIR / "assets" / "img" / "poster.png",
            BASE_DIR / "assets" / "img" / "boxart.png",
        ]
        poster_found = None
        for pc in poster_candidates:
            if pc.exists():
                poster_found = pc
                break

        if poster_found:
            try:
                pil_img = Image.open(poster_found)
                w, h = 380, 560
                self.ctk_poster = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(w, h))
                self.poster_label = ctk.CTkLabel(self.left_frame, image=self.ctk_poster, text="")
                self.poster_label.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
            except Exception:
                pass

        # Tarjeta de metadatos del juego
        meta_card = ctk.CTkFrame(self.left_frame, fg_color=C_BG_DEEP, corner_radius=8, border_width=1, border_color=C_BORDER)
        meta_card.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 16))

        ctk.CTkLabel(meta_card, text="METAL GEAR SOLID", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color=C_TEXT_WHITE).pack(anchor="w", padx=14, pady=(10, 2))
        ctk.CTkLabel(meta_card, text="PAL ESPAÑA (SLES-01734) | VOCES EN CASTELLANO",
                     font=ctk.CTkFont(size=11, weight="bold"), text_color=C_ORANGE).pack(anchor="w", padx=14, pady=2)

        badges_frame = ctk.CTkFrame(meta_card, fg_color="transparent")
        badges_frame.pack(fill="x", padx=14, pady=6)
        badges = [("4K UHD", C_CYAN), ("PGXP", C_GREEN), ("16:9 / 21:9", C_GOLD), ("60 FPS", C_ORANGE)]
        for b_txt, b_col in badges:
            b_lbl = ctk.CTkLabel(badges_frame, text=f" {b_txt} ", font=ctk.CTkFont(size=10, weight="bold"),
                                 fg_color=C_CARD_BG, text_color=b_col, corner_radius=4)
            b_lbl.pack(side="left", padx=(0, 6))

        desc_txt = "Recompilación binaria nativa a código C ejecutándose a velocidad x64. Incluye Alfonso Vallés como Solid Snake y motor SPU HQ."
        ctk.CTkLabel(meta_card, text=desc_txt, font=ctk.CTkFont(size=11), text_color=C_TEXT_MUTED,
                     wraplength=350, justify="left").pack(anchor="w", padx=14, pady=(4, 10))

        # ══════════════════════════════════════════════════════
        # ── 2. COLUMNA DERECHA: CONSOLA DE CONFIGURACIÓN ──
        # ══════════════════════════════════════════════════════
        self.right_frame = ctk.CTkFrame(self, fg_color=C_BG_DEEP, corner_radius=0)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=12)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1)

        # Barra Superior de Estado y Botón Fullscreen
        top_bar = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        top_bar.grid_columnconfigure(0, weight=1)

        title_box = ctk.CTkFrame(top_bar, fg_color="transparent")
        title_box.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(title_box, text="METAL GEAR SOLID — RECOMPILED EDITION",
                     font=ctk.CTkFont(size=24, weight="bold"), text_color=C_TEXT_WHITE).pack(anchor="w")
        ctk.CTkLabel(title_box, text="● SISTEMA RECOMPILADO LISTO — Selecciona disco o inicia la misión con Enter",
                     font=ctk.CTkFont(size=12, weight="bold"), text_color=C_GREEN).pack(anchor="w", pady=(2, 0))

        # Botón de alternancia de pantalla completa del Launcher
        self.btn_fs_toggle = ctk.CTkButton(top_bar, text="🗖 Salir de Pantalla Completa (F11)",
                                           font=ctk.CTkFont(size=12, weight="bold"),
                                           fg_color=C_CARD_BG, hover_color=C_CARD_HOVER,
                                           border_width=1, border_color=C_BORDER,
                                           text_color=C_TEXT_WHITE, command=self.toggle_fullscreen,
                                           height=34, width=220)
        self.btn_fs_toggle.grid(row=0, column=1, sticky="e", padx=(10, 0))

        # Cuaderno de Pestañas Estilo Terranigma SNES Recomp
        self.tabview = ctk.CTkTabview(self.right_frame, fg_color=C_CARD_BG,
                                      segmented_button_fg_color=C_BG_DEEP,
                                      segmented_button_selected_color=C_ORANGE,
                                      segmented_button_selected_hover_color=C_ORANGE_HOVER,
                                      segmented_button_unselected_color=C_BG_DEEP,
                                      segmented_button_unselected_hover_color=C_CARD_HOVER,
                                      text_color=C_TEXT_WHITE)
        self.tabview.grid(row=1, column=0, sticky="nsew", pady=4)

        tab_play     = self.tabview.add("🚀 MISIÓN & LANZADOR")
        tab_video    = self.tabview.add("🖥️ VÍDEO Y MEJORAS 3D")
        tab_textures = self.tabview.add("🎨 TEXTURAS HD & SHADERS")
        tab_ctrl     = self.tabview.add("🎮 MANDOS Y CONTROLES")
        tab_audio    = self.tabview.add("🔊 AUDIO & SISTEMA")

        self.build_play_tab(tab_play)
        self.build_video_tab(tab_video)
        self.build_textures_tab(tab_textures)
        self.build_controls_tab(tab_ctrl)
        self.build_audio_tab(tab_audio)

        # ══════════════════════════════════════════════════════
        # ── 3. FOOTER FIJO INFERIOR CON ACCIÓN DE DISPARO ──
        # ══════════════════════════════════════════════════════
        footer = ctk.CTkFrame(self, fg_color=C_CARD_BG, corner_radius=0, height=76, border_width=1, border_color=C_BORDER)
        footer.grid(row=1, column=0, columnspan=2, sticky="ew", padx=0, pady=0)
        footer.grid_columnconfigure(0, weight=1)
        footer.grid_columnconfigure(1, weight=0)

        # Indicador de mando
        self.gamepad_label = ctk.CTkLabel(footer, text=detect_gamepad_name(), font=ctk.CTkFont(size=13, weight="bold"),
                                          text_color=C_CYAN)
        self.gamepad_label.grid(row=0, column=0, sticky="w", padx=24, pady=16)

        # Controles rápidos de salida y lanzamiento
        btn_box = ctk.CTkFrame(footer, fg_color="transparent")
        btn_box.grid(row=0, column=1, sticky="e", padx=20, pady=14)

        btn_folder = ctk.CTkButton(btn_box, text="📁 Abrir Carpeta", font=ctk.CTkFont(size=12, weight="bold"),
                                   fg_color=C_BG_DEEP, hover_color=C_CARD_HOVER, border_width=1, border_color=C_BORDER,
                                   command=self.open_game_folder, width=130, height=44)
        btn_folder.pack(side="left", padx=6)

        btn_exit = ctk.CTkButton(btn_box, text="✕ Salir (Esc)", font=ctk.CTkFont(size=12, weight="bold"),
                                 fg_color=C_BG_DEEP, hover_color=C_CARD_HOVER, border_width=1, border_color=C_BORDER,
                                 command=self.confirm_exit, width=110, height=44)
        btn_exit.pack(side="left", padx=6)

        btn_launch = ctk.CTkButton(btn_box, text="▶ INICIAR METAL GEAR SOLID (ENTER)",
                                   font=ctk.CTkFont(size=15, weight="bold"),
                                   fg_color=C_ORANGE, hover_color=C_ORANGE_HOVER, width=320, height=44,
                                   command=self.launch_game)
        btn_launch.pack(side="left", padx=(10, 4))

    # ──────────────────────────────────────────────────────────
    # PESTAÑA 1: MISIÓN & LANZADOR
    # ──────────────────────────────────────────────────────────
    def build_play_tab(self, tab):
        tab.grid_columnconfigure(0, weight=1)

        # 1. Selector de Disco
        disc_frame = ctk.CTkFrame(tab, fg_color="transparent")
        disc_frame.pack(fill="x", padx=16, pady=(10, 14))

        ctk.CTkLabel(disc_frame, text="SELECCIÓN DE DISCO — ARCHIVO DE OPERACIONES:",
                     font=ctk.CTkFont(size=13, weight="bold"), text_color=C_ORANGE).pack(anchor="w", pady=(0, 6))

        cards_box = ctk.CTkFrame(disc_frame, fg_color="transparent")
        cards_box.pack(fill="x")
        cards_box.grid_columnconfigure((0, 1), weight=1)

        for i, d in enumerate(DISCS_INFO):
            card = ctk.CTkFrame(cards_box, fg_color=C_BG_DEEP, border_width=1, border_color=C_BORDER, corner_radius=8)
            card.grid(row=0, column=i, sticky="nsew", padx=6, pady=4)

            rb = ctk.CTkRadioButton(card, text=d["title"], variable=self.selected_disc, value=d["id"],
                                    font=ctk.CTkFont(size=13, weight="bold"), fg_color=C_ORANGE, hover_color=C_ORANGE_HOVER,
                                    text_color=C_TEXT_WHITE)
            rb.pack(anchor="w", padx=12, pady=(10, 4))
            ctk.CTkLabel(card, text=d["desc"], font=ctk.CTkFont(size=11), text_color=C_TEXT_MUTED,
                         wraplength=380, justify="left").pack(anchor="w", padx=12, pady=(0, 10))

        # 2. Modo de Pantalla del Juego (Requisito clave: Pantalla Completa de Inicio)
        fs_mode_frame = ctk.CTkFrame(tab, fg_color=C_BG_DEEP, corner_radius=8, border_width=1, border_color=C_BORDER)
        fs_mode_frame.pack(fill="x", padx=16, pady=8)

        ctk.CTkLabel(fs_mode_frame, text="MODO DE PANTALLA AL INICIAR EL JUEGO:",
                     font=ctk.CTkFont(size=13, weight="bold"), text_color=C_CYAN).pack(anchor="w", padx=14, pady=(10, 6))

        fs_opts_box = ctk.CTkFrame(fs_mode_frame, fg_color="transparent")
        fs_opts_box.pack(fill="x", padx=14, pady=(0, 10))

        rb_fs1 = ctk.CTkRadioButton(fs_opts_box, text="⛶ Pantalla Completa Sin Bordes (Recomendado - 4K Nativo)",
                                     variable=self.game_fullscreen, value=1, font=ctk.CTkFont(size=12, weight="bold"),
                                     fg_color=C_ORANGE, hover_color=C_ORANGE_HOVER, text_color=C_TEXT_WHITE)
        rb_fs1.pack(side="left", padx=(0, 16))

        rb_fs2 = ctk.CTkRadioButton(fs_opts_box, text="🖥️ Pantalla Completa Exclusiva",
                                     variable=self.game_fullscreen, value=2, font=ctk.CTkFont(size=12),
                                     fg_color=C_ORANGE, hover_color=C_ORANGE_HOVER, text_color=C_TEXT_WHITE)
        rb_fs2.pack(side="left", padx=16)

        rb_fs0 = ctk.CTkRadioButton(fs_opts_box, text="🪟 Modo Ventana",
                                     variable=self.game_fullscreen, value=0, font=ctk.CTkFont(size=12),
                                     fg_color=C_ORANGE, hover_color=C_ORANGE_HOVER, text_color=C_TEXT_WHITE)
        rb_fs0.pack(side="left", padx=16)

        # 3. Presets Rápidos
        preset_frame = ctk.CTkFrame(tab, fg_color="transparent")
        preset_frame.pack(fill="x", padx=16, pady=8)

        ctk.CTkLabel(preset_frame, text="PRESETS DE OPTIMIZACIÓN EN UN CLIC:",
                     font=ctk.CTkFont(size=13, weight="bold"), text_color=C_ORANGE).pack(anchor="w", pady=(0, 6))

        presets_box = ctk.CTkFrame(preset_frame, fg_color="transparent")
        presets_box.pack(fill="x")
        presets_box.grid_columnconfigure((0, 1, 2, 3), weight=1)

        presets = [
            ("🌟 4K UHD Master Edition", "3840x2160 SSAA 2.0x\n16:9 Widescreen GTE\nPGXP Anti-Jitter + Depth\nRemaster Cinematic Shader",
             lambda: self.apply_preset("16:9", "4k", "2.0", True, True, True, "shaders/remaster_cinematic.pfx", "off", 1, "🌟 4K UHD Master Edition")),
            ("🏎️ 21:9 Ultrawide Cinema", "3440x1440 SSAA 2.0x\n21:9 Campo Visual Ampliado\nPGXP 3D Sin Temblor\nRemaster Shader Activo",
             lambda: self.apply_preset("21:9", "4k", "2.0", True, True, True, "shaders/remaster_cinematic.pfx", "off", 1, "🏎️ 21:9 Ultrawide Cinema")),
            ("📺 4:3 PlayStation 1998", "1440x1080 (4:3 Original)\nScanlines CRT Auténticas\nAudio SPU HQ 48 kHz\nExperiencia Clásica PS1",
             lambda: self.apply_preset("4:3", "1080p", "1.0", False, False, False, "shaders/crt_scanlines.pfx", "on", 1, "📺 4:3 PlayStation 1998")),
            ("⚡ 1080p Rendimiento / Deck", "1920x1080 Nativo\nBajo consumo GPU\n60 FPS Máxima fluidez\nIdeal Portátiles / Steam Deck",
             lambda: self.apply_preset("16:9", "1080p", "1.0", True, True, True, "none", "on", 1, "⚡ 1080p Rendimiento / Deck")),
        ]

        for idx, (p_title, p_desc, p_cmd) in enumerate(presets):
            p_card = ctk.CTkButton(presets_box, text=f"{p_title}\n\n{p_desc}", font=ctk.CTkFont(size=11, weight="bold"),
                                   fg_color=C_BG_DEEP, hover_color=C_CARD_HOVER, border_width=1, border_color=C_BORDER,
                                   text_color=C_TEXT_WHITE, command=p_cmd, height=100)
            p_card.grid(row=0, column=idx, sticky="nsew", padx=4, pady=4)

        # Estado del preset actual
        self.preset_status_lbl = ctk.CTkLabel(tab, text=f"✔ Preset Activo: {self.active_preset_name.get()}",
                                              font=ctk.CTkFont(size=12, weight="bold"), text_color=C_GREEN)
        self.preset_status_lbl.pack(anchor="w", padx=20, pady=(10, 4))

    def apply_preset(self, aspect, res, ss, pgxp, depth, persp, shader, vsync, fs, name):
        self.aspect_ratio.set(aspect)
        self.resolution.set(res)
        self.supersample.set(ss)
        self.pgxp_enabled.set(pgxp)
        self.pgxp_depth.set(depth)
        self.perspective_enabled.set(persp)
        self.post_shader.set(shader)
        self.vsync_enabled.set(vsync)
        self.game_fullscreen.set(fs)
        self.active_preset_name.set(name)
        self.preset_status_lbl.configure(text=f"✔ Preset Activo: {name} (Aplicado y Guardado)")

    # ──────────────────────────────────────────────────────────
    # PESTAÑA 2: VÍDEO Y MEJORAS 3D
    # ──────────────────────────────────────────────────────────
    def build_video_tab(self, tab):
        frame = ctk.CTkFrame(tab, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=16, pady=12)

        # Fila 1: Relación de Aspecto
        r1 = ctk.CTkFrame(frame, fg_color=C_BG_DEEP, corner_radius=6, border_width=1, border_color=C_BORDER)
        r1.pack(fill="x", pady=4)
        ctk.CTkLabel(r1, text="Relación de Aspecto Widescreen (FOV Ajustado):", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=C_TEXT_WHITE).pack(side="left", padx=14, pady=10)
        ctk.CTkOptionMenu(r1, values=["16:9", "21:9", "4:3"], variable=self.aspect_ratio,
                          fg_color=C_CARD_BG, button_color=C_ORANGE, button_hover_color=C_ORANGE_HOVER).pack(side="right", padx=14)

        # Fila 2: Resolución Interna de Renderizado
        r2 = ctk.CTkFrame(frame, fg_color=C_BG_DEEP, corner_radius=6, border_width=1, border_color=C_BORDER)
        r2.pack(fill="x", pady=4)
        ctk.CTkLabel(r2, text="Resolución Interna de Renderizado GPU:", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=C_TEXT_WHITE).pack(side="left", padx=14, pady=10)
        ctk.CTkOptionMenu(r2, values=["4k", "1440p", "1080p", "720p", "240p"], variable=self.resolution,
                          fg_color=C_CARD_BG, button_color=C_ORANGE, button_hover_color=C_ORANGE_HOVER).pack(side="right", padx=14)

        # Fila 3: Antialiasing Supersampling (SSAA)
        r3 = ctk.CTkFrame(frame, fg_color=C_BG_DEEP, corner_radius=6, border_width=1, border_color=C_BORDER)
        r3.pack(fill="x", pady=4)
        ctk.CTkLabel(r3, text="Supersampling Antialiasing (SSAA 2.0x Ultra-nítido):", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=C_TEXT_WHITE).pack(side="left", padx=14, pady=10)
        ctk.CTkOptionMenu(r3, values=["2.0", "1.5", "1.0"], variable=self.supersample,
                          fg_color=C_CARD_BG, button_color=C_ORANGE, button_hover_color=C_ORANGE_HOVER).pack(side="right", padx=14)

        # Fila 4: PGXP Subpixel Precision
        r4 = ctk.CTkFrame(frame, fg_color=C_BG_DEEP, corner_radius=6, border_width=1, border_color=C_BORDER)
        r4.pack(fill="x", pady=4)
        ctk.CTkLabel(r4, text="PGXP Subpixel Precision (Elimina el temblor / wobble poligonal de PS1):",
                     font=ctk.CTkFont(size=12, weight="bold"), text_color=C_TEXT_WHITE).pack(side="left", padx=14, pady=10)
        ctk.CTkSwitch(r4, text="", variable=self.pgxp_enabled, progress_color=C_ORANGE).pack(side="right", padx=14)

        # Fila 5: PGXP Depth Buffer (Z-Buffer 32-bit)
        r5 = ctk.CTkFrame(frame, fg_color=C_BG_DEEP, corner_radius=6, border_width=1, border_color=C_BORDER)
        r5.pack(fill="x", pady=4)
        ctk.CTkLabel(r5, text="PGXP Depth Buffer Z-Buffer (Evita que polígonos traspasen paredes):",
                     font=ctk.CTkFont(size=12, weight="bold"), text_color=C_TEXT_WHITE).pack(side="left", padx=14, pady=10)
        ctk.CTkSwitch(r5, text="", variable=self.pgxp_depth, progress_color=C_ORANGE).pack(side="right", padx=14)

        # Fila 6: Corrección de Perspectiva
        r6 = ctk.CTkFrame(frame, fg_color=C_BG_DEEP, corner_radius=6, border_width=1, border_color=C_BORDER)
        r6.pack(fill="x", pady=4)
        ctk.CTkLabel(r6, text="Corrección de Texturas en Perspectiva (Geometría 3D sin distorsión afín):",
                     font=ctk.CTkFont(size=12, weight="bold"), text_color=C_TEXT_WHITE).pack(side="left", padx=14, pady=10)
        ctk.CTkSwitch(r6, text="", variable=self.perspective_enabled, progress_color=C_ORANGE).pack(side="right", padx=14)

        # Fila 7: VSync
        r7 = ctk.CTkFrame(frame, fg_color=C_BG_DEEP, corner_radius=6, border_width=1, border_color=C_BORDER)
        r7.pack(fill="x", pady=4)
        ctk.CTkLabel(r7, text="Sincronización Vertical (VSync):", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=C_TEXT_WHITE).pack(side="left", padx=14, pady=10)
        ctk.CTkOptionMenu(r7, values=["off", "on"], variable=self.vsync_enabled,
                          fg_color=C_CARD_BG, button_color=C_ORANGE, button_hover_color=C_ORANGE_HOVER).pack(side="right", padx=14)

    # ──────────────────────────────────────────────────────────
    # PESTAÑA 3: TEXTURAS HD & SHADERS
    # ──────────────────────────────────────────────────────────
    def build_textures_tab(self, tab):
        frame = ctk.CTkFrame(tab, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=16, pady=12)

        # Shaders de Post-procesado
        s_row = ctk.CTkFrame(frame, fg_color=C_BG_DEEP, corner_radius=6, border_width=1, border_color=C_BORDER)
        s_row.pack(fill="x", pady=4)
        ctk.CTkLabel(s_row, text="Shader de Post-Procesado Cinematográfico:", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=C_TEXT_WHITE).pack(side="left", padx=14, pady=10)
        ctk.CTkOptionMenu(s_row, values=["shaders/remaster_cinematic.pfx", "shaders/crt_scanlines.pfx", "none"],
                          variable=self.post_shader, fg_color=C_CARD_BG, button_color=C_ORANGE,
                          button_hover_color=C_ORANGE_HOVER, width=240).pack(side="right", padx=14)

        # Inyección de Texturas HD
        r1 = ctk.CTkFrame(frame, fg_color=C_BG_DEEP, corner_radius=6, border_width=1, border_color=C_BORDER)
        r1.pack(fill="x", pady=4)
        ctk.CTkLabel(r1, text="Inyección de Texturas HD en Tiempo Real (Formato DuckStation):",
                     font=ctk.CTkFont(size=12, weight="bold"), text_color=C_TEXT_WHITE).pack(side="left", padx=14, pady=10)
        ctk.CTkSwitch(r1, text="", variable=self.hd_textures_enabled, progress_color=C_ORANGE).pack(side="right", padx=14)

        # Dumper de Texturas
        r2 = ctk.CTkFrame(frame, fg_color=C_BG_DEEP, corner_radius=6, border_width=1, border_color=C_BORDER)
        r2.pack(fill="x", pady=4)
        ctk.CTkLabel(r2, text="Texture Dumper (Volcar texturas originales de la VRAM a disco):",
                     font=ctk.CTkFont(size=12, weight="bold"), text_color=C_TEXT_WHITE).pack(side="left", padx=14, pady=10)
        ctk.CTkSwitch(r2, text="", variable=self.texture_dump_enabled, progress_color=C_ORANGE).pack(side="right", padx=14)

        # Botones de Acceso Rápido
        btn_box = ctk.CTkFrame(frame, fg_color="transparent")
        btn_box.pack(fill="x", pady=10)

        ctk.CTkButton(btn_box, text="📁 Abrir Carpeta de Reemplazos HD", font=ctk.CTkFont(size=12, weight="bold"),
                      fg_color=C_BG_DEEP, hover_color=C_CARD_HOVER, border_width=1, border_color=C_BORDER,
                      command=self.open_replacements_folder, height=38).pack(side="left", fill="x", expand=True, padx=(0, 6))

        ctk.CTkButton(btn_box, text="📸 Abrir Carpeta de Volcados (Dumps)", font=ctk.CTkFont(size=12, weight="bold"),
                      fg_color=C_BG_DEEP, hover_color=C_CARD_HOVER, border_width=1, border_color=C_BORDER,
                      command=self.open_dumps_folder, height=38).pack(side="left", fill="x", expand=True, padx=6)

        ctk.CTkButton(frame, text="⚡ Ejecutar Asistente Automatizado (INSTALAR_PACK_TEXTURAS_HD.bat)",
                      font=ctk.CTkFont(size=13, weight="bold"), fg_color=C_CARD_BG, hover_color=C_CARD_HOVER,
                      border_width=1, border_color=C_ORANGE, text_color=C_ORANGE,
                      command=self.run_texture_installer, height=44).pack(fill="x", pady=10)

        # Nota explicativa
        note_box = ctk.CTkFrame(frame, fg_color=C_BG_DEEP, corner_radius=6, border_width=1, border_color=C_BORDER)
        note_box.pack(fill="x", pady=4)
        ctk.CTkLabel(note_box, text="Compatibilidad DuckStation:", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=C_CYAN).pack(anchor="w", padx=14, pady=(8, 2))
        info_t = "Puedes arrastrar cualquier pack HD comprimido (.zip, .7z) sobre INSTALAR_PACK_TEXTURAS_HD.bat para cargarlo instantáneamente."
        ctk.CTkLabel(note_box, text=info_t, font=ctk.CTkFont(size=11), text_color=C_TEXT_MUTED,
                     wraplength=680, justify="left").pack(anchor="w", padx=14, pady=(2, 8))

    # ──────────────────────────────────────────────────────────
    # PESTAÑA 4: MANDOS Y CONTROLES
    # ──────────────────────────────────────────────────────────
    def build_controls_tab(self, tab):
        frame = ctk.CTkFrame(tab, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=16, pady=12)

        r1 = ctk.CTkFrame(frame, fg_color=C_BG_DEEP, corner_radius=6, border_width=1, border_color=C_BORDER)
        r1.pack(fill="x", pady=4)
        ctk.CTkLabel(r1, text="Modo de Mando PlayStation:", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=C_TEXT_WHITE).pack(side="left", padx=14, pady=10)
        ctk.CTkOptionMenu(r1, values=["analog", "digital"], variable=self.analog_mode,
                          fg_color=C_CARD_BG, button_color=C_ORANGE, button_hover_color=C_ORANGE_HOVER).pack(side="right", padx=14)

        # Tabla de controles MGS1
        ctk.CTkLabel(frame, text="MAPEO TÁCTICO DE CONTROLES (METAL GEAR SOLID):", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=C_ORANGE).pack(anchor="w", pady=(10, 4))

        table = ctk.CTkFrame(frame, fg_color=C_BG_DEEP, corner_radius=6, border_width=1, border_color=C_BORDER)
        table.pack(fill="both", expand=True, pady=4)

        controls_data = [
            ("Mover a Solid Snake / Agacharse", "Flechas / W A S D", "Stick Analógico Izquierdo / D-Pad"),
            ("Disparar SOCOM / FA-MAS / Stinger", "Tecla Z / Barra Espaciadora", "Botón X (Xbox) / Cuadrado (PlayStation)"),
            ("Golpe / Combo cuerpo a cuerpo", "Tecla X", "Botón B (Xbox) / Círculo (PlayStation)"),
            ("Agacharse / Arrastrarse en conductos", "Tecla C", "Botón A (Xbox) / Cruz (PlayStation)"),
            ("Modo Vista en 1ª Persona (Scope/Stinger)", "Tecla V", "Botón Y (Xbox) / Triángulo (PlayStation)"),
            ("Menú Rápido de Armas", "Tecla E / Shift Derecho", "Gatillo RB / R1"),
            ("Menú Rápido de Equipo (Raciones)", "Tecla Q / Shift Izquierdo", "Gatillo LB / L1"),
            ("Abrir Códec (140.85 Coronel Campbell)", "Tabulador / Backspace", "Botón View / Back / Select"),
            ("Menú de Pausa / Opciones", "Intro / Enter", "Botón Start / Menu"),
        ]

        for i, (action, kb, pad) in enumerate(controls_data):
            row = ctk.CTkFrame(table, fg_color="transparent")
            row.pack(fill="x", padx=12, pady=2)
            row.grid_columnconfigure((0, 1, 2), weight=1)
            col = C_ORANGE if i in (1, 7) else C_TEXT_WHITE
            ctk.CTkLabel(row, text=action, font=ctk.CTkFont(size=11, weight="bold"), text_color=col, anchor="w").grid(row=0, column=0, sticky="w")
            ctk.CTkLabel(row, text=kb, font=ctk.CTkFont(size=11), text_color=C_TEXT_MUTED, anchor="w").grid(row=0, column=1, sticky="w")
            ctk.CTkLabel(row, text=pad, font=ctk.CTkFont(size=11), text_color=C_CYAN, anchor="w").grid(row=0, column=2, sticky="w")

    # ──────────────────────────────────────────────────────────
    # PESTAÑA 5: AUDIO & SISTEMA
    # ──────────────────────────────────────────────────────────
    def build_audio_tab(self, tab):
        frame = ctk.CTkFrame(tab, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=16, pady=12)

        r1 = ctk.CTkFrame(frame, fg_color=C_BG_DEEP, corner_radius=6, border_width=1, border_color=C_BORDER)
        r1.pack(fill="x", pady=4)
        ctk.CTkLabel(r1, text="Motor de Audio SPU HQ 48 kHz (Interpolación Gaussiana 24 canales):",
                     font=ctk.CTkFont(size=12, weight="bold"), text_color=C_TEXT_WHITE).pack(side="left", padx=14, pady=10)
        ctk.CTkSwitch(r1, text="", variable=self.spu_hq_enabled, progress_color=C_ORANGE).pack(side="right", padx=14)

        box_cast = ctk.CTkFrame(frame, fg_color=C_BG_DEEP, corner_radius=6, border_width=1, border_color=C_BORDER)
        box_cast.pack(fill="x", pady=10)

        ctk.CTkLabel(box_cast, text="REPARTO HISTÓRICO DE DOBLAJE AL CASTELLANO (1999):",
                     font=ctk.CTkFont(size=12, weight="bold"), text_color=C_ORANGE).pack(anchor="w", padx=14, pady=(10, 4))

        cast = [
            ("Solid Snake", "Alfonso Vallés"),
            ("Coronel Roy Campbell", "Vicente Gil"),
            ("Meryl Silverburgh", "Conchi López"),
            ("Liquid Snake", "Ricky Coello"),
            ("Revolver Ocelot", "Paco Gázquez"),
            ("Sniper Wolf", "Ana María Camps"),
            ("Dr. Hal 'Otacon' Emmerich", "Quim Roca"),
            ("Mei Ling", "Meritxell Aneiros"),
            ("Naomi Hunter", "Marta Estrada"),
        ]
        for ch, actor in cast:
            r = ctk.CTkFrame(box_cast, fg_color="transparent")
            r.pack(fill="x", padx=14, pady=1)
            ctk.CTkLabel(r, text=f"• {ch}:", font=ctk.CTkFont(size=11, weight="bold"), text_color=C_TEXT_WHITE, width=190, anchor="w").pack(side="left")
            ctk.CTkLabel(r, text=actor, font=ctk.CTkFont(size=11), text_color=C_CYAN, anchor="w").pack(side="left")

        ctk.CTkLabel(box_cast, text="", height=4).pack()

    def open_game_folder(self):
        if os.name == "nt":
            os.startfile(str(GAME_WORK_DIR))

    def open_replacements_folder(self):
        target = GAME_WORK_DIR / "mods" / "texture-packs" / "SLES-01734" / "replacements"
        target.mkdir(parents=True, exist_ok=True)
        if os.name == "nt":
            os.startfile(str(target))

    def open_dumps_folder(self):
        target = GAME_WORK_DIR / "mods" / "texture-packs" / "SLES-01734" / "dumps"
        target.mkdir(parents=True, exist_ok=True)
        if os.name == "nt":
            os.startfile(str(target))

    def run_texture_installer(self):
        bat = GAME_WORK_DIR / "INSTALAR_PACK_TEXTURAS_HD.bat"
        if not bat.exists():
            bat = BASE_DIR / "INSTALAR_PACK_TEXTURAS_HD.bat"
        if bat.exists() and os.name == "nt":
            subprocess.Popen(["cmd.exe", "/c", str(bat)], cwd=str(bat.parent))

    def save_settings(self):
        disc_num = self.selected_disc.get()
        disc_cue = f"disc/Metal Gear Solid (Spain) (Disc {disc_num}).cue"
        fs_mode = self.game_fullscreen.get()

        targets = [GAME_WORK_DIR]
        if (BASE_DIR / "build-release").exists() and (BASE_DIR / "build-release") not in targets:
            targets.append(BASE_DIR / "build-release")

        for target_dir in targets:
            toml_path = target_dir / "game.toml"
            if toml_path.exists():
                try:
                    with open(toml_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    new_lines = []
                    cur_section = ""
                    for line in lines:
                        sl = line.strip()
                        if sl.startswith("[") and sl.endswith("]"):
                            cur_section = sl[1:-1].strip()

                        if cur_section == "game" and sl.startswith("disc ="):
                            new_lines.append(f'disc = "{disc_cue}"\n')
                        elif cur_section == "video" and sl.startswith("fullscreen ="):
                            new_lines.append(f'fullscreen = {fs_mode}\n')
                        elif cur_section == "video" and sl.startswith("aspect_ratio ="):
                            new_lines.append(f'aspect_ratio = "{self.aspect_ratio.get()}"\n')
                        elif cur_section == "video" and sl.startswith("internal_resolution ="):
                            new_lines.append(f'internal_resolution = "{self.resolution.get()}"\n')
                        elif cur_section == "video" and sl.startswith("supersample ="):
                            new_lines.append(f'supersample = {self.supersample.get()}\n')
                        elif cur_section == "video" and sl.startswith("geometry_correction ="):
                            new_lines.append(f'geometry_correction = {"true" if self.pgxp_enabled.get() else "false"}\n')
                        elif cur_section == "video" and sl.startswith("pgxp_depth_buffer ="):
                            new_lines.append(f'pgxp_depth_buffer = {"true" if self.pgxp_depth.get() else "false"}\n')
                        elif cur_section == "video" and sl.startswith("perspective_texturing ="):
                            new_lines.append(f'perspective_texturing = {"true" if self.perspective_enabled.get() else "false"}\n')
                        elif cur_section == "video" and sl.startswith("post_shader ="):
                            new_lines.append(f'post_shader = "{self.post_shader.get()}"\n')
                        elif cur_section == "video" and sl.startswith("vsync ="):
                            new_lines.append(f'vsync = "{self.vsync_enabled.get()}"\n')
                        elif cur_section == "audio" and sl.startswith("spu_hq ="):
                            new_lines.append(f'spu_hq = {"true" if self.spu_hq_enabled.get() else "false"}\n')
                        elif cur_section == "controller" and sl.startswith("default_mode ="):
                            new_lines.append(f'default_mode = "{self.analog_mode.get()}"\n')
                        else:
                            new_lines.append(line)

                    with open(toml_path, "w", encoding="utf-8") as f:
                        f.writelines(new_lines)
                except Exception:
                    pass

            # Escribir settings.toml complementario
            try:
                settings_path = target_dir / "settings.toml"
                settings_content = f"""[video]
fullscreen = {fs_mode}
aspect_ratio = "{self.aspect_ratio.get()}"
internal_resolution = "{self.resolution.get()}"
supersample = {self.supersample.get()}
geometry_correction = {"true" if self.pgxp_enabled.get() else "false"}
pgxp_depth_buffer = {"true" if self.pgxp_depth.get() else "false"}
perspective_texturing = {"true" if self.perspective_enabled.get() else "false"}
post_shader = "{self.post_shader.get()}"
vsync = "{self.vsync_enabled.get()}"

[audio]
spu_hq = {"true" if self.spu_hq_enabled.get() else "false"}

[controller]
p1_device = "0300fa675e040000130b000023057801"
p1_mode = "{self.analog_mode.get()}"
p1_deadzone = 3276
multitap = false
multitap_analog = true
deadzone = 3276
default_mode = "{self.analog_mode.get()}"

[disc]
path = "{disc_cue}"
selected = {disc_num}
"""
                settings_path.write_text(settings_content, encoding="utf-8")
            except Exception:
                pass

        # Guardar mods
        save_mod_state(targets, self.hd_textures_enabled.get(), self.texture_dump_enabled.get())

    def launch_game(self):
        self.save_settings()
        if not GAME_EXE.exists():
            messagebox.showerror("Error", f"No se encontró el ejecutable nativo recompilado:\n{GAME_EXE}")
            return

        cmd = [str(GAME_EXE), "--no-launcher"]
        try:
            subprocess.Popen(cmd, cwd=str(GAME_WORK_DIR))
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error al iniciar", f"No se pudo iniciar el juego:\n{e}")

if __name__ == "__main__":
    app = MGSModernLauncher()
    app.mainloop()
