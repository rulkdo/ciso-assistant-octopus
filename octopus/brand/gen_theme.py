# -*- coding: utf-8 -*-
"""Generuje frontend/octopus-brand.css: paleta z octopus-lab.pl nalozona na motyw cisotheme.
Kotwice ze strony (zmienne --ol-*): bg #0a0d1a, bg-2 #0c1022, surface #141937, accent #4f63ff,
accent-2 #6c7dff, accent-deep #3b46a8, text #eaeefb, text-dim #9aa6c4, eyebrow #8294ff, gradient #9fb0ff.
"""
import math, sys

STEPS = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]


def hex2rgb(h):
    h = h.lstrip("#"); return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]


def lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def oklch(h):
    r, g, b = (lin(c) for c in hex2rgb(h))
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (x ** (1 / 3) for x in (l, m, s))
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    A = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    B = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    C = math.hypot(A, B); H = math.degrees(math.atan2(B, A)) % 360
    return f"oklch({L*100:.2f}% {C:.3f} {H:.2f}deg)"


# Skale (hex), kotwice ze strony oznaczone komentarzem w README
PRIMARY = {  # akcent marki
    50: "#eef0ff", 100: "#e0e4ff", 200: "#c6cdff", 300: "#9fb0ff", 400: "#6c7dff", 500: "#4f63ff",
    600: "#4152e0", 700: "#3b46a8", 800: "#2e3784", 900: "#222960", 950: "#141937"}
SECONDARY = {  # granat (przyciski drugorzedne)
    50: "#f0f2fa", 100: "#e1e5f4", 200: "#c5cbe6", 300: "#9ea7d0", 400: "#6f7bb5", 500: "#3b46a8",
    600: "#333d92", 700: "#2b3378", 800: "#22295f", 900: "#1a2048", 950: "#121633"}
TERTIARY = {  # chlodny turkus (rzadko uzywany)
    50: "#ecfafc", 100: "#d2f2f7", 200: "#a8e4ee", 300: "#72cfe0", 400: "#3fb4cb", 500: "#1f98b0",
    600: "#197c92", 700: "#176477", 800: "#175262", 900: "#163f4c", 950: "#0d2932"}
SURFACE = {  # neutralne z odcieniem granatu
    50: "#f6f7fc", 100: "#eef0f8", 200: "#dfe3f0", 300: "#c4cade", 400: "#9aa6c4", 500: "#6e7898",
    600: "#4d5675", 700: "#2f3657", 800: "#1c2244", 900: "#141937", 950: "#0a0d1a"}


def scale(name, sc, light_from):
    out = []
    for s in STEPS:
        out.append(f"\t--color-{name}-{s}: {oklch(sc[s])};")
    out.append(f"\t--color-{name}-contrast-dark: var(--color-{name}-950);")
    out.append(f"\t--color-{name}-contrast-light: var(--color-{name}-50);")
    for s in STEPS:
        side = "light" if s >= light_from else "dark"
        out.append(f"\t--color-{name}-contrast-{s}: var(--color-{name}-contrast-{side});")
    return "\n".join(out)


def tw_palette(name, sc):
    return "\n".join(f"\t--color-{name}-{s}: {oklch(sc[s])};" for s in STEPS)


FONTS = []
for fam, file, weights in (("Manrope", "manrope", (400, 500, 600, 700)), ("Sora", "sora", (400, 600, 700))):
    for w in weights:
        for sub, rng in (
            ("latin-ext", "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,"
                          "U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF"),
            ("latin", "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,"
                      "U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD")):
            FONTS.append(f"@font-face {{ font-family: '{fam}'; font-style: normal; font-weight: {w}; font-display: swap;"
                         f" src: url('/fonts/{file}-{sub}-{w}-normal.woff2') format('woff2'); unicode-range: {rng}; }}")

css = f"""/*
  Octopus Lab: branding CISO Assistant by Octopus Lab.
  Paleta z www.octopus-lab.pl (granat #0a0d1a / #141937, akcent #4f63ff, #6c7dff, #3b46a8).
  Plik generowany skryptem octopus/brand/gen_theme.py. Nie edytuj recznie, zmien skrypt.
  Laduje sie po ciso-theme.css, wiec nadpisuje kolory motywu bez ruszania pliku upstream.
*/

{chr(10).join(FONTS)}

/* Fiolety i roze Tailwinda wpiete na sztywno w komponentach -> kolory marki */
@theme {{
	--font-sans: 'Manrope', ui-sans-serif, system-ui, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji';
	--font-heading: 'Sora', 'Manrope', ui-sans-serif, system-ui, sans-serif;
{tw_palette('violet', PRIMARY)}
{tw_palette('purple', PRIMARY)}
{tw_palette('pink', SECONDARY)}
{tw_palette('fuchsia', SECONDARY)}
}}

[data-theme='cisotheme'] {{
	--typo-heading--font-family: var(--font-heading);
{scale('primary', PRIMARY, 400)}
{scale('secondary', SECONDARY, 400)}
{scale('tertiary', TERTIARY, 500)}
{scale('surface', SURFACE, 600)}
}}

/* Tytul strony i naglowek logowania: kolor marki zamiast gradientu roz-fiolet */
.octo-title {{
	font-family: var(--font-heading);
	letter-spacing: -0.01em;
	color: var(--color-surface-900);
}}
.dark .octo-title {{
	color: var(--color-surface-50);
}}
.octo-accent {{
	color: var(--color-primary-500);
}}
.dark .octo-accent {{
	color: var(--color-primary-300);
}}
"""
sys.stdout.write(css)
