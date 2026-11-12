[size=150][b][PS1 Recomp] Metal Gear Solid (PAL España SLES-01734 / SLES-11734) — Port Nativo para PC v1.0 (4K UHD SSAA 2.0x, 16:9 y 21:9 Ultrawide, PGXP Subpixel sin Wobble, Doblaje Castellano Alfonso Vallés, Soporte 2 CDs, Texturas HD, Master Launcher Fullscreen Terranigma)[/b][/size]

Buenas a todos,

Tras la fantástica acogida de *Final Fantasy VIII Recompiled* y atendiendo a las peticiones de la comunidad de ElOtroLado, os traigo la recompilación estática nativa para PC de una de las mayores obras maestras del videojuego: [b]Metal Gear Solid (PlayStation 1, Edición Española Oficial)[/b], con el histórico y aclamado doblaje en castellano encabezado por [b]Alfonso Vallés[/b] como Solid Snake, Vicente Gil como el Coronel Roy Campbell y Conchi López como Meryl Silverburgh.

Al ser un motor 100% poligonal 3D en tiempo real, la tecnología de recompilación estática MIPS -> C nativo saca a relucir todo el potencial visual de Shadow Moses: resolución interna 4K ultra nítida, eliminación total del temblor poligonal típico de PS1 mediante PGXP, campo visual panorámico nativo sin estiramiento y latencia de respuesta instantánea.

[img]https://raw.githubusercontent.com/aitorcachero/metal-gear-solid-recomp/main/assets/img/poster.png[/img]

---

[size=130][b]🔗 Enlaces del Proyecto:[/b][/size]
* 📦 **Repositorio Oficial en GitHub:** [url=https://github.com/aitorcachero/metal-gear-solid-recomp]https://github.com/aitorcachero/metal-gear-solid-recomp[/url]
* 🚀 **Página de Release v1.0:** [url=https://github.com/aitorcachero/metal-gear-solid-recomp/releases/tag/v1.0.0]Metal Gear Solid Recompiled v1.0 (GitHub Releases)[/url]
* 💾 **Descarga Directa del Paquete ZIP (56.7 MB):** [url=https://github.com/aitorcachero/metal-gear-solid-recomp/releases/download/v1.0.0/Metal_Gear_Solid_Recompiled_v1.0_Windows_x64.zip]Metal_Gear_Solid_Recompiled_v1.0_Windows_x64.zip[/url]

---

[size=130][b]💿 Información de Versión e Identificadores SLES (PAL España):[/b][/size]
Esta recompilación está calibrada de forma nativa para las imágenes originales de la edición española:
* **Disco 1 (Infiltración en Shadow Moses):** [b]SLES-01734[/b] (España)
* **Disco 2 (Torres de Comunicaciones, Alto Horno y Metal Gear REX):** [b]SLES-11734[/b] (España)
* *Nota técnica:* El motor de juego recompilado ejecuta directamente el binario interno [c]MGS1.EXE[/c] (2.725 funciones y 1.8M líneas de código C), resolviendo de raíz el cuelgue en pantalla negra de la pantalla legal de advertencia europea de [c]SLES_017.34[/c] e iniciando inmediatamente al motor de juego a 60 FPS.

---

[size=130][b]🌟 Características Principales de la Versión v1.0:[/b][/size]

* 🖥️ **Resolución Interna 4K Ultra HD:** Renderizado nativo de alta precisión con supersampling SSAA 2.0x, filtrado bilineal y anisotrópico 16x.
* 📐 **Panorámico 16:9 y 21:9 Ultrawide Real:** Modo GTE Widescreen con compensación de aspecto matemática. Solid Snake, los guardias, el helipuerto de vigilancia, los conductos de ventilación y el hangar subterráneo de REX llenan el 100% de la pantalla sin deformación ni estiramientos.
* 💎 **PGXP Subpixel Precision (Sin Temblor Poligonal):** Supresión matemática total del temblor (*polygon wobble / jitter*) típico de PS1 en el modelo de Snake, Psycho Mantis, torretas, tanques y Metal Gear REX.
* 🛡️ **PGXP Depth Buffer (Z-Buffer 32-bit):** Precisión de profundidad real por hardware que evita que los polígonos traspasen paredes o se solapen erróneamente.
* 🔍 **Perspective-Correct Texturing:** Eliminación completa de la distorsión afín en todas las paredes, suelos y pasillos 3D del complejo.
* 🎙️ **Audio SPU HQ 48 kHz y Doblaje Oficial en Castellano (1999):** Motor de sonido PlayStation de 24 canales con interpolación Gaussiana y latencia ultrabaja. Disfruta de la voz legendaria de Alfonso Vallés ("¿Pero qué coño...?"), Vicente Gil (Campbell), Conchi López (Meryl) y Ricky Coello (Liquid Snake) con máxima fidelidad acústica.
* 💿 **Soporte Dinámico para 2 CDs:** Detección de imágenes de Disco 1 y Disco 2 con selector interactivo y cambio de disco en caliente.
* 🕹️ **Control Analógico DualShock:** Detección automática en caliente de mandos de Xbox (One/Series), PlayStation (DualSense/DualShock 4) y Switch Pro, con sticks analógicos 360° activos y calibración de zona muerta (deadzone).
* 🌟 **Shaders de Post-Procesado en Tiempo Real:** 
  * [b]Remaster Cinematic HD:[/b] Filtro de nitidez adaptativa CAS (Contrast Adaptive Sharpening), resplandor HDR Bloom en explosiones de C4 y granadas Chaff, y suavizado de bordes FXAA HQ.
  * [b]CRT Retro Scanlines:[/b] Simulación auténtica de televisor CRT trinitron para una experiencia nostálgica idéntica a 1998.
* 🖼️ **Inyección de Texturas HD (DuckStation Compatible):** Carga al vuelo texturas en 4K/UHD (`.png`, `.webp`, `.jpg`) sustituyendo las originales de PS1.
* ⚡ **Instalador en 1-Clic ([c]INSTALAR_PACK_TEXTURAS_HD.bat[/c]):** Basta con arrastrar y soltar cualquier archivo comprimido (.zip, .rar, .7z) para organizar y activar el pack de texturas automáticamente en [c]mods/texture-packs/SLES-01734/replacements[/c].
* 🚀 **Master Launcher Moderno a Pantalla Completa (Estilo Terranigma / SNES Recomp):** Interfaz gráfica oscura que inicia automáticamente en pantalla completa adaptativa High-DPI con presets de 1 clic, selector de disco visual y mapa de controles.

---

[size=130][b]🕹️ Mapeo Táctico de Controles en Metal Gear Solid:[/b][/size]

[table]
[tr][th]Acción en el Juego[/th][th]Teclado (PC)[/th][th]Mando Xbox / PlayStation[/th][/tr]
[tr][td]Mover a Snake / Agacharse[/td][td]Flechas / W A S D[/td][td]Stick Izquierdo / Cruceta (D-Pad)[/td][/tr]
[tr][td]Disparar (SOCOM / FA-MAS / Stinger)[/td][td]Tecla Z / Barra Espacio[/td][td]Botón X (Xbox) / Cuadrado (PlayStation)[/td][/tr]
[tr][td]Golpear (Combo puñetazo / patada)[/td][td]Tecla X[/td][td]Botón B (Xbox) / Círculo (PlayStation)[/td][/tr]
[tr][td]Agacharse / Arrastrarse en conductos[/td][td]Tecla C[/td][td]Botón A (Xbox) / Cruz (PlayStation)[/td][/tr]
[tr][td]Vista en 1ª Persona (Scope / Stinger)[/td][td]Tecla V[/td][td]Botón Y (Xbox) / Triángulo (PlayStation)[/td][/tr]
[tr][td]Menú rápido de Armas[/td][td]Tecla E / Shift Derecho[/td][td]Gatillo RB / R1[/td][/tr]
[tr][td]Menú rápido de Equipo (Raciones)[/td][td]Tecla Q / Shift Izquierdo[/td][td]Gatillo LB / L1[/td][/tr]
[tr][td]Abrir Códec (140.85 Campbell)[/td][td]Tabulador / Retroceso[/td][td]Botón View / Back / Select[/td][/tr]
[tr][td]Pausa / Menú de Opciones[/td][td]Intro / Enter[/td][td]Botón Start / Menu[/td][/tr]
[tr][td]Alternar Pantalla Completa[/td][td]Alt + Enter / F11[/td][td]F11 / Touchpad[/td][/tr]
[tr][td]Salir instantáneamente[/td][td]Escape (Esc)[/td][td]Escape (Esc)[/td][/tr]
[/table]

---

[size=130][b]📦 Contenido del Paquete ZIP (v1.0 Windows x64):[/b][/size]

* [b]Metal_Gear_Solid_Launcher.exe[/b]: Lanzador maestro gráfico moderno en pantalla completa (estilo Terranigma / Illusion of Time).
* [b]Metal_Gear_Solid_Recompiled.exe[/b]: Ejecutable nativo del juego (46.7 MB) con motor en C++ / SDL3.
* [b]MetalGearSolid.exe[/b]: Acceso directo directo al juego.
* [b]JUGAR_METAL_GEAR_SOLID.bat[/b]: Acceso principal al lanzador gráfico.
* [b]JUGAR_METAL_GEAR_SOLID_16_9_PANTALLA_COMPLETA.bat[/b]: Arranque directo 16:9 Widescreen 4K 60FPS sin pasar por menús.
* [b]JUGAR_METAL_GEAR_SOLID_21_9_ULTRAWIDE.bat[/b]: Arranque directo 21:9 Ultrawide.
* [b]JUGAR_METAL_GEAR_SOLID_4K_43.bat[/b]: Modo retro 4:3 clásico con scanlines CRT.
* [b]CONFIGURAR_METAL_GEAR_SOLID.bat[/b]: Acceso directo a la configuración de gráficos y mandos.
* [b]INSTALAR_PACK_TEXTURAS_HD.bat[/b]: Instalador drag-and-drop de texturas HD.
* [b]PREPARAR_DISCOS.bat[/b]: Extractor automatizado de imágenes en formato .CHD a .CUE/.BIN.
* [b]LEEME_INSTRUCCIONES.txt[/b]: Manual rápido y guía de referencia en castellano.

---

[size=130][b]🚀 Guía de Instalación en 3 Pasos:[/b][/size]

1. Descarga y descomprime [b]Metal_Gear_Solid_Recompiled_v1.0_Windows_x64.zip[/b] en cualquier carpeta de tu PC.
2. Coloca tus imágenes del [b]Disco 1[/b] y [b]Disco 2[/b] de Metal Gear Solid (versión España [b]SLES-01734[/b] y [b]SLES-11734[/b]) en la subcarpeta [c]disc\[/c] en formato [c].cue/.bin[/c] o [c].chd[/c]. Si están en [c].chd[/c], haz doble clic en [c]PREPARAR_DISCOS.bat[/c] para descomprimirlas en pocos segundos.
3. Ejecuta [b]JUGAR_METAL_GEAR_SOLID.bat[/b] o [b]Metal_Gear_Solid_Launcher.exe[/b], selecciona tu preset favorito y pulsa [b]Iniciar Metal Gear Solid[/b].

¡Que disfrutéis de nuevo de la mejor aventura de infiltración táctica de todos los tiempos con una calidad visual y acústica insuperable!

---
[i]Nota legal: Este proyecto no incluye ninguna ROM comercial ni material protegido por derechos de autor. Cada usuario debe proveer sus propias copias originales legítimas de los discos de Metal Gear Solid.[/i]
