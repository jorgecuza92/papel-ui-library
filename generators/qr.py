#!/usr/bin/env python3
"""
papél QR: a real QR code in ink on paper, square modules, whole pixels.

    python3 generators/qr.py "eject safely"                     -> eject_safely.svg
    python3 generators/qr.py "eject safely" --format png --module 7

Error correction M by default. Keep the text short: 1-14 characters fit the smallest code (21x21).
"""
import argparse
import qrcode
from PIL import Image

INK, PAPER = (0, 0, 0), (240, 236, 232)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('text')
    ap.add_argument('--format', choices=['svg', 'png'], default='svg')
    ap.add_argument('--module', type=int, default=7)
    ap.add_argument('--border', type=int, default=0, help='quiet zone in modules (0: the page is the quiet zone)')
    ap.add_argument('-o', '--out')
    a = ap.parse_args()
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=a.border, box_size=1)
    q.add_data(a.text); q.make(fit=True)
    m = q.get_matrix(); n = len(m); s = a.module
    out = a.out or f'{a.text.replace(" ", "_")}.{a.format}'
    if a.format == 'svg':
        rects = ''.join(f'<rect x="{c * s}" y="{r * s}" width="{s}" height="{s}"/>'
                        for r in range(n) for c in range(n) if m[r][c])
        open(out, 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{n*s}" height="{n*s}" viewBox="0 0 {n*s} {n*s}" '
                             f'shape-rendering="crispEdges"><title>QR: {a.text}</title><g fill="#000">{rects}</g></svg>\n')
    else:
        img = Image.new('RGB', (n * s, n * s), PAPER); px = img.load()
        for r in range(n):
            for c in range(n):
                if m[r][c]:
                    for y in range(s):
                        for x in range(s):
                            px[c * s + x, r * s + y] = INK
        img.save(out)
    print(f'{out}: {n}x{n} modules (version {q.version}), {n*s}px, "{a.text}"')


if __name__ == '__main__':
    main()
