#!/usr/bin/env python3
"""
papél tokens: tokens.json -> dist/tokens.css, dist/tokens.js, dist/tailwind.preset.js

    python3 tokens/build.py

tokens.json is the one source. Every colour, size, space and radius in the library comes from it.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, 'dist')


def main():
    t = json.load(open(os.path.join(HERE, 'tokens.json'), encoding='utf-8'))
    os.makedirs(DIST, exist_ok=True)

    colors = {c['name']: c['value'] for c in t['color']['tokens']}
    spacing = {s['name']: s['value'] for s in t['spacing']['tokens']}
    radius = {r['name']: r['value'] for r in t['radius']['tokens']}
    stroke = {s['name']: s['value'] for s in t.get('stroke', {}).get('tokens', [])}
    fam = t['type']['families']
    styles = {s['name']: dict(s, family=g['family']) for g in t['type']['groups'] for s in g['styles']}

    # tokens.css
    css = ['/* papél tokens: generated from tokens/tokens.json by tokens/build.py. Do not edit by hand. */']
    for f in t['type']['fonts']:
        css.append('@font-face{font-family:"%s";src:url("%s");font-weight:%s;font-display:swap}'
                   % (f['family'], '../' + f['file'], f['weight']))
    css.append(':root{')
    for k, v in colors.items():
        css.append(f'  --papel-{k}: {v};')
    for k, v in fam.items():
        css.append(f'  --papel-font-{k}: {v};')
    for k, v in {**spacing, **radius, **stroke}.items():
        css.append(f'  --papel-{k}: {v};')
    for k, s in styles.items():
        css.append(f'  --papel-{k}-size: {s["fontSize"]}; --papel-{k}-line: {s["lineHeight"]}; --papel-{k}-weight: {s["fontWeight"]};')
    css.append('}')
    open(os.path.join(DIST, 'tokens.css'), 'w', encoding='utf-8').write('\n'.join(css) + '\n')

    flat = {'color': colors, 'font': fam, 'space': spacing, 'radius': radius, 'stroke': stroke,
            'text': {k: {'family': s['family'], 'size': s['fontSize'], 'line': s['lineHeight'],
                         'weight': s['fontWeight']} for k, s in styles.items()}}
    open(os.path.join(DIST, 'tokens.js'), 'w', encoding='utf-8').write(
        '// papél tokens: generated from tokens/tokens.json. Do not edit by hand.\nexport default '
        + json.dumps(flat, indent=2, ensure_ascii=False) + ';\n')

    tw = {'theme': {'extend': {
        'colors': {'papel': colors},
        'fontFamily': {k: [p.strip().strip('"') for p in v.split(',')] for k, v in fam.items()},
        'fontSize': {f'papel-{k}': [s['fontSize'], {'lineHeight': s['lineHeight'], 'fontWeight': str(s['fontWeight'])}]
                     for k, s in styles.items()},
        'spacing': {k.replace('space-', 'papel-'): v for k, v in spacing.items()},
        'borderRadius': {'papel-0': '0', 'papel-dot': '50%'},
    }}}
    open(os.path.join(DIST, 'tailwind.preset.js'), 'w', encoding='utf-8').write(
        '// papél Tailwind preset: generated from tokens/tokens.json.\n'
        '// tailwind.config.js:  presets: [require("./tokens/dist/tailwind.preset.js")]\n'
        'module.exports = ' + json.dumps(tw, indent=2, ensure_ascii=False) + ';\n')
    print('wrote', ', '.join(sorted(os.listdir(DIST))))


if __name__ == '__main__':
    main()
