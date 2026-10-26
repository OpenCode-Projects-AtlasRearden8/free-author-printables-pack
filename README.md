# Author Book-Day Printables Pack

Seven free, unbranded printable sheets for a book launch. Everything is
plain HTML/CSS that a local build script turns into print-ready PDFs - no
signups, no accounts, nothing online.

## What's inside

`printables/` holds only unbranded sheets (no company or author names on
them), and `printables/usage/` has a friendly one-page guide for every
sheet:

- **Launch-Week Countdown Calendar** - one focus area per day for the
  week before launch
- **Launch-Day Checklist** - morning to evening, one page, tick as you go
- **Bookmark Templates** - two per page, fill in by hand, cut on the line
- **Thank-You Card Templates** - three quarter-fold cards per page
- **Series Bible One-Pager** - books, cast, places, timeline rules on
  one sheet
- **Signing & Market Day Sales Log** - tallies and totals only, never
  customer data
- **Review Request Postcards** - two per page; the buyer fills in all
  personal fields themselves

This pack complements the free author marketing kit; it intentionally
does not repeat anything that kit already covers (it covers day-of and
book-day logistics, not the long-range marketing plan).

## How to build

Requirements: Python 3 with `pip install weasyprint`.

```
python3 build.py
```

That renders every sheet in `sources/` into `printables/` and every
usage guide into `printables/usage/`. To verify everything builds as a
valid, US-Letter PDF with a text layer:

```
python3 -m pytest tests/ -q
```

(open `verify` above runs the build inside a temp copy of the repo, so
the shipped printables are never disturbed).

## Printing tips

- Paper: US Letter (8.5 x 11 in), 0.5 in margins - built in.
- Pick **"Actual size"** (not "Fit to page") in the print dialog.
- Cardstock (65-80 lb) for bookmarks; plain 24 lb paper for cards.
- Duplicate and print as many copies as you like for your own books.

## Files

```
sources/            HTML + shared CSS for every sheet (the only place to edit)
build.py            one-command local build to PDF
tests/              pytest suite over the built PDFs
printables/         unbranded output PDFs (plus usage/ guides)
```

Free, local, and beginner-friendly - published by **Asdale Dynamics, LLC**
(AI explained like a friend would; see the hub at the author's site for
more free tools). MIT licensed - see `LICENSE`.
