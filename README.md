<div align="center">

# 🥷 Metal Gear Solid Recompiled (PC Port Nativo x64 — Master Edition)

### *Port nativo para PC (Windows x64) mediante ingeniería inversa y recompilación estática LLVM*
### *Versión Española Oficial (SLES-01734 / SLES-11734) con el doblaje de Alfonso Vallés*

[![Platform](https://img.shields.io/badge/Plataforma-Windows%20x64%20Nativo-blue.svg?style=for-the-badge&logo=windows)](https://github.com/aitorcachero/metal-gear-solid-recomp)
[![Resolution](https://img.shields.io/badge/Resoluci%C3%B3n-Nativa%204K%20UHD%20(3840x2160)-brightgreen.svg?style=for-the-badge)](https://github.com/aitorcachero/metal-gear-solid-recomp)
[![Framerate](https://img.shields.io/badge/Refresco-60%20FPS%20%2F%20VBlank%20Pacing-orange.svg?style=for-the-badge)](https://github.com/aitorcachero/metal-gear-solid-recomp)
[![Aspect Ratio](https://img.shields.io/badge/Aspecto-16%3A9%20%2F%2021%3A9%20Ultrawide-purple.svg?style=for-the-badge)](https://github.com/aitorcachero/metal-gear-solid-recomp)
[![PGXP](https://img.shields.io/badge/Geometr%C3%ADa-PGXP%20Subpixel%20Precision-red.svg?style=for-the-badge)](https://github.com/aitorcachero/metal-gear-solid-recomp)
[![Doblaje](https://img.shields.io/badge/Doblaje-Castellano%20Oficial%20(Alfonso%20Vall%C3%A9s)-gold.svg?style=for-the-badge)](https://github.com/aitorcachero/metal-gear-solid-recomp)
[![License](https://img.shields.io/badge/Licencia-MIT-green.svg?style=for-the-badge)](LICENSE)

---

</div>

## 📖 Descripción

**Metal Gear Solid Recompiled** es un port nativo para PC (Windows x64) de la obra maestra creada en 1998 por **Hideo Kojima y Konami** para PlayStation 1.

A diferencia de los emuladores tradicionales que interpretan en tiempo real las instrucciones de la CPU MIPS R3000A, este proyecto emplea recompilación estática anticipada (AOT) mediante **psxrecomp** y la suite de compiladores **LLVM/Clang**. El binario ejecutable completo del juego (`MGS1.EXE`, 2.725 funciones identificadas y más de 1.8 millones de líneas de código C) se traduce directamente a código fuente C optimizado que compila a código nativo x64 de 64 bits enlazado con la GPU moderna vía OpenGL y SDL3.

El resultado es una experiencia fluida a 60 FPS estables con latencia de entrada mínima, arranque instantáneo y compatibilidad perfecta con el doblaje en castellano de la versión PAL España (**SLES-01734** para el Disco 1 y **SLES-11734** para el Disco 2).

---

## ✨ Características Principales

* 🖥️ **Resolución Interna 4K Ultra HD:** Renderizado de alta fidelidad con supersampling (SSAA 2.0x), filtrado bilineal y anisotrópico 16x.
* 📐 **Relación de Aspecto Panorámica 16:9 y 21:9 Ultrawide:** Campo de visión ampliado nativamente con compensación matemática GTE. Solid Snake, el helipuerto de Shadow Moses, las torretas, los conductos y el hangar de Metal Gear REX llenan el 100% del monitor sin franjas ni deformación de geometrías.
* 💎 **PGXP Subpixel Precision (Sin Temblor Poligonal):** Supresión matemática total del temblor (*polygon jitter/wobble*) típico de PS1 en el modelo 3D de Snake, Psycho Mantis, Vulcan Raven y Metal Gear REX.
* 🛡️ **PGXP Depth Buffer (Z-Buffer 32-bit):** Precisión de profundidad real por hardware que evita que los polígonos o extremidades traspasen paredes u objetos adyacentes.
* 🔍 **Perspective-Correct Texturing:** Eliminación de la distorsión afín en todas las paredes, pasillos y texturas 3D del complejo nuclear.
* 🎙️ **Doblaje Oficial en Castellano (1999) con Audio SPU HQ a 48 kHz:**
  * Solid Snake: **Alfonso Vallés**
  * Coronel Roy Campbell: **Vicente Gil**
  * Meryl Silverburgh: **Conchi López**
  * Liquid Snake: **Ricky Coello**
  * Revolver Ocelot: **Paco Gázquez**
  * Sniper Wolf: **Ana María Camps**
  * Dr. Hal "Otacon" Emmerich: **Quim Roca**
  * Mei Ling: **Meritxell Aneiros**
  * Naomi Hunter: **Marta Estrada**
  * *Motor de audio SPU de 24 canales con interpolación Gaussiana y latencia ultrabaja.*
* 💿 **Soporte Dinámico para 2 CDs:** Detección de imágenes del Disco 1 y Disco 2 con cambio de disco en caliente.
* 🕹️ **Control Analógico DualShock:** Detección automática en caliente de mandos de Xbox (One, Series), PlayStation (DualSense, DualShock 4) y Switch Pro, con sticks analógicos 360° activos y calibración de zona muerta.
* 🌟 **Shaders de Post-procesado en Tiempo Real (GLSL):**
  * **Remaster Cinematic HD:** Filtro de nitidez adaptativa CAS (Contrast Adaptive Sharpening), resplandor HDR Bloom en explosiones de C4 y granadas Chaff, y suavizado de bordes FXAA HQ.
  * **CRT Retro Scanlines:** Simulación auténtica de televisión de tubo trinitron de 1998 para puristas.
* 🖼️ **Inyección de Texturas HD (Compatible con DuckStation):** Carga en tiempo real texturas en 4K/UHD (`.png`, `.webp`, `.jpg`) sustituyendo las de baja resolución de PS1 sin tocar el código original.
* ⚡ **Asistente Automatizado en 1-Clic (`INSTALAR_PACK_TEXTURAS_HD.bat`):** Basta con arrastrar y soltar cualquier archivo `.zip`, `.rar` o `.7z` sobre el script para activar un pack de texturas.
* 🚀 **Master Launcher Moderno a Pantalla Completa (Estilo Terranigma / SNES Recomp):** Interfaz oscura neumórfica adaptativa que inicia directamente a pantalla completa con 4 presets de 1 clic, selector visual de discos y mapa interactivo de controles.

---

## 🕹️ Mapeo Táctico de Controles

| Acción | Teclado (PC) | Mando Xbox / PlayStation |
| :--- | :--- | :--- |
| **Mover a Snake / Agacharse** | Flechas / W A S D | Stick Analógico Izquierdo / Cruceta (D-Pad) |
| **Disparar (SOCOM / FA-MAS / Stinger)** | Tecla Z / Espacio | Botón X (Xbox) / Cuadrado (PlayStation) |
| **Golpe / Combo cuerpo a cuerpo** | Tecla X | Botón B (Xbox) / Círculo (PlayStation) |
| **Agacharse / Arrastrarse** | Tecla C | Botón A (Xbox) / Cruz (PlayStation) |
| **Vista en 1ª Persona (Scope/Stinger)** | Tecla V | Botón Y (Xbox) / Triángulo (PlayStation) |
| **Menú Rápido de Armas** | Tecla E / Shift Derecho | Gatillo RB / R1 |
| **Menú Rápido de Equipo (Raciones)** | Tecla Q / Shift Izquierdo | Gatillo LB / L1 |
| **Abrir Códec (140.85 Campbell)** | Tabulador / Retroceso | Botón View / Back / Select |
| **Pausa / Menú de Opciones** | Intro / Enter | Botón Start / Menu |
| **Alternar Pantalla Completa** | Alt + Enter / F11 | F11 / Touchpad |
| **Salir instantáneamente** | Escape (Esc) | Escape (Esc) |

---

## 🚀 Cómo Jugar en 3 Pasos

1. Descarga el paquete oficial desde la sección **[Releases](https://github.com/aitorcachero/metal-gear-solid-recomp/releases)**: `Metal_Gear_Solid_Recompiled_v1.0_Windows_x64.zip`.
2. Coloca tus imágenes del Disco 1 y Disco 2 de Metal Gear Solid (versión España `SLES-01734` y `SLES-11734`) en formato `.cue`/`.bin` o `.chd` dentro de la subcarpeta `disc/`. Si están en formato `.chd`, ejecuta `PREPARAR_DISCOS.bat` para convertirlas automáticamente.
3. Ejecuta `JUGAR_METAL_GEAR_SOLID.bat` o `Metal_Gear_Solid_Launcher.exe`, selecciona tu preset gráfico favorito y pulsa **Iniciar Metal Gear Solid**.

---

## ⚖️ Nota Legal

Este repositorio contiene únicamente el código fuente recompilado a C, el motor de tiempo de ejecución y las herramientas de lanzamiento. No se distribuye ningún archivo con copyright de Konami ni ROMs protegidas. El usuario debe suministrar sus propias copias legítimas de los discos originales de Metal Gear Solid.
