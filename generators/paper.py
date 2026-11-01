#!/usr/bin/env python3
"""
papél recolour: turn a dark-theme image (white on black) into the paper palette.

    python3 generators/paper.py in.png out.png [--bitmap]

black -> paper, white -> ink, red/orange -> signal, blue -> rule, everything anti-aliased keeps
its coverage. --bitmap uses paper-bitmap (#f7efef), the value 16-bit (RGB565) screens show for
paper, so images match a `background color: F0ECE8` exactly on devices like the iPod.
"""
import argparse
import numpy as np
from PIL import Image

INK, SIGNAL, RULE = np.array((0, 0, 0.)), np.array((255, 80, 0.)), np.array((185, 182, 175.))


def recolor(img, paper):
    a = np.asarray(img.convert('RGB')).astype(float)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(axis=2), a.min(axis=2)
    out = np.empty_like(a)
    gray = (mx - mn) <= 12
    red = ~gray & (r > 2.5 * g) & (r > 2.5 * b)
    blue = ~gray & ~red & (b > r) & (b > g)
    other = ~gray & ~red & ~blue
    for mask, k, t in ((gray, mx / 255, INK), (red, r / 246, SIGNAL), (blue, b / 170, RULE), (other, mx / 255, INK)):
        k = np.clip(k, 0, 1)[..., None]
        out[mask] = (paper * (1 - k) + t * k)[mask]
    magenta = (r == 255) & (g == 0) & (b == 255)
    out[magenta] = (255, 0, 255)
    return Image.fromarray(np.clip(out + .5, 0, 255).astype(np.uint8))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('dst')
    ap.add_argument('--bitmap', action='store_true')
    a = ap.parse_args()
    paper = np.array((247, 239, 239.)) if a.bitmap else np.array((240, 236, 232.))
    recolor(Image.open(a.src), paper).save(a.dst)
    print('wrote', a.dst)


if __name__ == '__main__':
    main()
