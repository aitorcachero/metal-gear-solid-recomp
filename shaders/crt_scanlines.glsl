// CRT Retro Scanline Shader for PS1 Recomp
uniform float u_scanline_intensity;
uniform float u_bloom;

void main() {
    vec3 col = textureLod(u_tex, v_uv, 0.0).rgb;
    // Scanline modulation
    float scanline = sin(v_uv.y * 480.0 * 3.14159265);
    scanline = (scanline + 1.0) * 0.5;
    col *= mix(1.0, 0.85 + 0.15 * scanline, u_scanline_intensity);
    o = vec4(clamp(col, 0.0, 1.0), 1.0);
}
