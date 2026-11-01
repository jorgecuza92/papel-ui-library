# icons

39 icons, `svg/<name>.svg`, 24×24, 1px stroke on .5 coordinates (crisp at 1x), square caps, `stroke="currentColor"`.
Names are short and lowercase like the menus (`fil`, `db`, `set`, `pls`). Only `mark` and `dot` use colour (signal, for the dot).

- `sprite.svg`: every icon as a `<symbol id="papel-<name>">`. Use `<svg><use href="sprite.svg#papel-play"/></svg>` (served over http).
- `index.html`: the sheet.
- New icon: draw it on the same grid, add the name to `ORDER.txt`, then run `python3 icons/build.py`.
