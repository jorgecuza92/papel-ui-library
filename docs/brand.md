# papél: the brand book

`[●]™` "papél" c/o jorge cuza.

papél is Jorge Cuza's personal brand. It started as the theme on his iPod Video and follows the catalog and wall-text language of Virgil Abloh: off-white paper, black type, one orange dot, quotation marks, plain labels and real barcodes. Everything new (screens, pages, posters, merch, packaging) should look like it came off the same sheet of paper.

## The mark

- `[●]™`: thin black square brackets around an orange dot (`signal`, #ff5000), with a small superscript ™ to the right.
- The dot is always `signal` and is never recoloured. The brackets are always `ink`.
- The ™ is used **once**, beside the mark, and nowhere else.
- The mark sits in a **fixed spot, top right**, inset `space-8` from the top and `space-16` from the right. It stays in that exact spot on every screen of a set, so it never jumps.
- Masters: `mark/mark-pixel-57x27.png` is the pixel-exact mark from the iPod (with @2x/@4x/@8x copies). `mark/mark.svg` is a vector redraw for print and large sizes.

## Colour

| token | value | use |
|---|---|---|
| `paper` | #f0ece8 | the ground, always |
| `ink` | #000000 | all text, brackets, meaningful rules |
| `signal` | #ff5000 | the dot only, one orange thing per screen |
| `rule` | #b9b6af | hairlines, unfilled progress, corner ticks |
| `graphite` | #7a7772 | rare secondary counters (fails 4.5:1 on paper: keep it non-essential) |

No gradients, no shadows, no other colours. On 16-bit (RGB565) screens the paper shows as #f7efef, so pixels inside images use `paper-bitmap`. Anything meant to blend into the background can also be transparent.

## Type

- **Helvetica-style grotesk** (TeX Gyre Heros, a free Helvetica clone) for the main voice.
  - `title`: 64px bold, lowercase, the one main thing on a screen.
  - `info`: 18px regular, for every line under the title. Those lines all share one size, weight and colour (`ink`) and are set tight (`space-20` pitch).
- **Typewriter mono** (Courier Prime Papel: Courier Prime Bold condensed to 78% with 80% pitch) for subtext. It stays small, the way Abloh uses it.
  - `menu`: 17px, for menu and navigation items.
  - `label`: 14px, for labels, times and counters.
- The real Helvetica isn't free to embed. TeX Gyre Heros (GUST Font License) and Courier Prime (OFL) are the shipping fonts.

## Voice and text conventions

- **lowercase** by default: titles, song names, labels, menus.
- **"QUOTES"** for names and labels, Abloh's signature. Artist and person names go in ALL CAPS inside quotes: `"APHEX TWIN"`. Small labels get quotes too: `"now playing"`.
- **[brackets]** for navigation and menu items, echoing the mark: `[fil]`, `[set]`.
- **underscores** join words in UI labels: `[snd_set]`, `[alb_artist]`. They're used only in UI labels, never in names of things like songs or albums.
- **short labels**, three letters where possible: res, fil, db, now, set, pls, plg, sys, sht, bkm.
- **dates as circa**: `C. 1992`, year only.
- **c/o** for credit lines: `"paper" c/o jorge cuza`.
- No fake data. Every number, barcode and label is real or functional.

## Layout

- **One left-aligned column** at `space-16`, like the c/o Virgil Abloh wall text: a big title, then tight info lines.
- **Header row**: an ornament top left (a barcode, or a `"label"`), the mark top right, both on the same line.
- **Hairlines only**: 1px (`hairline`), in `rule` or `ink`. Square corners everywhere (`radius-0`). The dot is the only round thing.
- **Generous empty paper.** If a screen feels empty, that's right.
- Small corner ticks in `rule` can frame a page, like crop marks.

## Ornaments

- **Barcodes and QR codes are real and scannable.** On the iPod, the player's barcode is a Code 128 code reading `dobby`, and the USB screen is a QR code reading `eject safely`.
- Draw them at whole-pixel module sizes so they stay crisp and scan, never squeezed.
- One ornament per screen, in `ink` on `paper`.

## Applications

The iPod Video theme ([papel](https://github.com/jorgecuza92/papel)) is the reference application. `ui/examples/` has the same three screens (player, menu, plug-in) built from `ui/papel.css`.

## Don't

- Don't add a second accent colour or put orange on text.
- Don't round corners, add shadows or use gradients.
- Don't use capitals for anything except names inside quotes and the C. in dates.
- Don't put the ™ anywhere but beside the mark.
- Don't move the mark between screens of the same set.
