#!/usr/bin/env python3
"""
papél icons: icons/svg/*.svg -> icons/sprite.svg and icons/index.html (the sheet)

    python3 icons/build.py

Rules for new icons: 24x24 grid, content inside 3..21, 1px stroke on .5 coordinates (crisp at 1x),
square caps, mitred joins, no fills (stroke="currentColor"). Only `mark` and `dot` use signal
(#ff5000), and only for the dot. Names are short and lowercase, like the menus: fil, db, set.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    order = [l.strip() for l in open(os.path.join(HERE, 'ORDER.txt')) if l.strip()]
    names = sorted(f[:-4] for f in os.listdir(os.path.join(HERE, 'svg')) if f.endswith('.svg'))
    names = [n for n in order if n in names] + [n for n in names if n not in order]
    symbols, cells = [], []
    for n in names:
        svg = open(os.path.join(HERE, 'svg', n + '.svg')).read()
        inner = re.search(r'<svg[^>]*>(.*)</svg>', svg, re.S).group(1)
        symbols.append(f'<symbol id="papel-{n}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                       f'stroke-width="1" stroke-linecap="square" stroke-linejoin="miter">{inner}</symbol>')
        cells.append(f'<figure><img src="svg/{n}.svg" width="48" height="48" alt=""><img src="svg/{n}.svg" width="24" height="24" alt=""><figcaption>[{n}]</figcaption></figure>')
    open(os.path.join(HERE, 'sprite.svg'), 'w').write(
        '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">\n' + '\n'.join(symbols) + '\n</svg>\n')
    html = f'''<!doctype html><meta charset="utf-8"><title>papél icons</title>
<link rel="stylesheet" href="../tokens/dist/tokens.css">
<style>
body{{margin:0;background:var(--papel-paper);color:var(--papel-ink);font-family:var(--papel-font-sans)}}
header{{display:flex;justify-content:space-between;align-items:flex-start;padding:24px 32px 8px}}
header p{{font-family:var(--papel-font-mono);font-weight:700;font-size:14px;margin:6px 0 0}}
h1{{font-size:64px;line-height:1;margin:0;font-weight:700}}
main{{display:grid;grid-template-columns:repeat(8,1fr);gap:0;padding:16px 32px 40px}}
figure{{margin:0;padding:16px 0 12px;border-top:1px solid var(--papel-rule);display:flex;flex-direction:column;align-items:flex-start;gap:8px}}
figure img + img{{opacity:1}}
figcaption{{font-family:var(--papel-font-mono);font-weight:700;font-size:14px}}
</style>
<header><div><p>"icons"</p><h1>papél</h1></div><img src="../mark/mark.svg" width="114" height="54" alt="[●]™"></header>
<main>{''.join(cells)}</main>
'''
    open(os.path.join(HERE, 'index.html'), 'w').write(html)
    print(len(names), 'icons -> sprite.svg, index.html')


if __name__ == '__main__':
    main()
