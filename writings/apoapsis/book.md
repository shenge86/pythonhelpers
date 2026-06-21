# apoapsis
### space and silence
*by Shen Ge*

This is the master index for the novel. Each link below opens the source file
for that section. The reading/build order is the order listed here — it matches
the file list in `build.yaml`, which is what pandoc uses to assemble the book.

## Front matter
- [Title, copyright & dedications](00-front-matter.md)
- [Foreword](00-foreword.md)

## Chapters
- [Chapter 1: The Journal](chapters/01-the-journal.md)
- [Chapter 2: The Break](chapters/02-the-break.md)
- [Chapter 3: The Dream](chapters/03-the-dream.md)
- [Chapter 4: The Cantina](chapters/04-the-cantina.md)
- [Chapter 5: The Message](chapters/05-the-message.md)
- [Chapter 19: Revelation](chapters/19-revelation.md)

## Poetry
- [Poetry (all poems)](poetry.md)

---

## Building the book (6×9 trim, KDP-ready PDF)

From inside this `apoapsis/` folder, run:

```bash
pandoc --defaults=build.yaml
```

This produces `apoapsis.pdf` at a 6×9 inch trim size using the default book serif.
A generated table of contents (chapters only) is inserted automatically, so
there is no hand-maintained Contents page here — that's intentional.

To export an EPUB for Kindle instead (reflowable, no fixed page size):

```bash
pandoc --defaults=build.yaml -t epub -o apoapsis.epub
```

The original, unsplit manuscript is preserved one level up at
`../apoapsis.md` as a backup.
