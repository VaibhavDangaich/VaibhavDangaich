# Asset generators

The animated SVGs in `assets/` are generated, not hand-edited. Regenerate
after changing a project, a stack item or the palette:

```bash
python3 gen_hero.py     > ../hero.svg      # knowledge-graph banner
python3 gen_terminal.py > ../terminal.svg  # whoami boot sequence
python3 gen_sections.py ..                 # section headers, project cards,
                                           # stack matrix, footer
```

No dependencies — plain Python 3. Everything is self-contained SVG (no
external fonts or scripts) so GitHub's camo proxy serves it and the
animations play, the same way the contribution snake does.

Two rules worth keeping if you edit these:

- **Reveals must freeze, not loop.** Clip rects carry a full-width base
  value and animate once with `fill="freeze"`, so a card still reads as
  complete anywhere the animation doesn't advance.
- **No emoji inside the SVGs.** They render with whatever font the viewer
  has; drawn shapes are predictable, emoji are not.
