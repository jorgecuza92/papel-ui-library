#!/usr/bin/env python3
"""
papél barcode: a real, scannable Code 128 barcode in ink on paper (or transparent).

    python3 generators/code128.py dobby                       -> dobby.svg
    python3 generators/code128.py dobby --format png --module 1 --height 27 --transparent
    python3 generators/code128.py dobby --format bmp --height 27   (Rockbox: magenta = transparent)

Bars are whole pixels (--module, default 1) so they stay crisp and scan. Never scale a barcode
by a non-integer factor. Shorter text = narrower code (each character is 11 modules).
"""
import argparse, sys
import barcode
from PIL import Image

INK, PAPER, MAGENTA = (0, 0, 0), (240, 236, 232), (255, 0, 255)


def modules(text):
    m = barcode.get('code128', text).build()[0]
    xs = [i for i, c in enumerate(m) if c == '1']
    return m[xs[0]:xs[-1] + 1]          # no quiet zone: the page around it is the quiet zone


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('text')
    ap.add_argument('--format', choices=['svg', 'png', 'bmp'], default='svg')
    ap.add_argument('--module', type=int, default=1, help='px per bar module')
    ap.add_argument('--height', type=int, default=27)
    ap.add_argument('--transparent', action='store_true', help='png: transparent background')
    ap.add_argument('-o', '--out')
    a = ap.parse_args()
    m = modules(a.text)
    w, h = len(m) * a.module, a.height
    out = a.out or f'{a.text.replace(" ", "_")}.{a.format}'
    if a.format == 'svg':
        rects, x = [], 0
        while x < len(m):
            if m[x] == '1':
                run = 1
                while x + run < len(m) and m[x + run] == '1':
                    run += 1
                rects.append(f'<rect x="{x * a.module}" y="0" width="{run * a.module}" height="{h}"/>')
                x += run
            else:
                x += 1
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
               f'shape-rendering="crispEdges"><title>Code 128: {a.text}</title><g fill="#000">{"".join(rects)}</g></svg>\n')
        open(out, 'w').write(svg)
    else:
        bg = (0, 0, 0, 0) if a.transparent and a.format == 'png' else (MAGENTA if a.format == 'bmp' else PAPER)
        img = Image.new('RGBA' if len(bg) == 4 else 'RGB', (w, h), bg)
        px = img.load()
        for i, c in enumerate(m):
            if c == '1':
                for dx in range(a.module):
                    for y in range(h):
                        px[i * a.module + dx, y] = INK if len(bg) == 3 else INK + (255,)
        img.save(out)
    print(f'{out}: {w}x{h} px, Code 128 "{a.text}"')


if __name__ == '__main__':
    sys.exit(main())
