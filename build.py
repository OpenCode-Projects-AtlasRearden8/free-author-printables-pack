#!/usr/bin/env python3
"""Build the Author Book-Day Printables Pack.

Renders every sheet in sources/ to an unbranded PDF in printables/,
plus a friendly usage page per sheet. Local only; no network, no signups.
"""

import importlib.metadata
import shutil
from pathlib import Path

from weasyprint import HTML

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "sources"
OUT = ROOT / "printables"
USAGE_OUT = OUT / "usage"

# sheet file (in sources/) -> short friendly label used on usage pages
SHEETS = [
    ("countdown-calendar.html", "Launch-Week Countdown Calendar",
     "Print this the week BEFORE your book launches. Write your book title and launch "
     "date at the top, then do one focus area per day. The blanks under each day are for "
     "whatever you actually did, which is a nicer record than what you planned. If a day "
     "falls apart, use the 'one task I will not skip' box at the bottom to make a promise "
     "to yourself that's small enough to keep."),
    ("launch-day-checklist.html", "Launch-Day Checklist",
     "Print this on launch day (or the night before) and keep it on your desk. It's "
     "organized from morning to evening: prepare, go live, steady the ship, then close "
     "kindly. You do NOT need to do everything — the sheet's job is to stop you from "
     "spinning. Tick boxes as you go. The evening section exists to remind you to stop working."),
    ("bookmarks.html", "Bookmark Templates",
     "Print on cardstock (65–80 lb) on US Letter. Cut along the dashed line — there are two "
     "bookmarks per page. Fill in the blanks with pen: book title, your name, a favorite "
     "quote, which book of the series this is, and when Book 2 is coming if it's useful. "
     "They tuck perfectly into a sold copy or a giveaway envelope."),
    ("thank-you-cards.html", "Thank-You Card Templates",
     "Print on plain paper (US Letter). There are three quarter-fold cards per page: crop "
     "or cut along the dashed line, fold in half twice, and you have a tiny card. The blank "
     "lines are for the buyer's name and a personal sentence — two handwritten words beat a "
     "paragraph of print. Use any card on the sheet; they're all the same size."),
    ("series-bible-one-pager.html", "Series Bible One-Pager",
     "Print one per series and keep it beside your keyboard. Fill in planned books first, "
     "then your main cast, places, and the timeline rules you must not contradict. The "
     "'things that must never happen' box is gold: note the retcons you've already decided "
     "against. Update in pencil as the series grows — this is a living sheet."),
    ("signing-sales-log.html", "Signing & Market Day Sales Log",
     "Print one per event. At the table, tally each sale in a row — time, format, quantity, "
     "price. Update the running total column as you go. At the bottom, note copies taken / "
     "sold / home and cash on hand before leaving. NO customer names or contact info on this "
     "sheet — tallies only. 'What worked' is for next event's future-you."),
    ("review-request-postcards.html", "Review Request Postcards",
     "Print on plain cardstock (US Letter), two postcards per page, cut along the dashed "
     "line. The front/side with blanks is where the buyer adds their own address and their "
     "own note — leave those fields empty. The printed ask is short on purpose: honest "
     "review, one sentence, no pressure. Great to hand out with signed copies."),
]

USAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>How to use: {title}</title>
<link rel="stylesheet" href="css/sheet.css">
<style>
.usage-body {{ max-width: 7in; }}
.step {{ margin: 10px 0; padding-left: 24px; text-indent: -24px; }}
.step b {{ color: var(--accent); }}
.callout {{
  border-left: 4pt solid var(--accent);
  background: var(--accent-light);
  padding: 10px 12px;
  margin: 14px 0;
}}
</style>
</head>
<body>
  <div class="sheet-header">
    <h1>{title}</h1>
    <p class="subtitle">A friendly guide to this printable sheet.</p>
  </div>
  <div class="usage-body">
    <p>{story}</p>
    <h2>What you need</h2>
    <ul>
      <li>The sheet's own PDF (<b>printables/{pdf}</b>)</li>
      <li>US Letter paper — regular printer is fine (cardstock for bookmarks)</li>
      <li>A pen you like</li>
    </ul>
    <div class="callout">
      <b>Troubleshooting:</b> if the sheet prints oversized, pick "Actual size"
      (not "Fit to page") in the print dialog. Every sheet fits US Letter with
      1/2-inch margins, which every home printer can show.
    </div>
  </div>
  <div class="sheet-footer">
    Usage guide &middot; Author Book-Day Printables Pack &middot; local, free, no signups
  </div>
</body>
</html>
"""


def build() -> list[Path]:
    for d in (OUT, USAGE_OUT):
        d.mkdir(parents=True, exist_ok=True)

    made = []
    for pdf_name, title, story in SHEETS:
        html_path = SRC / pdf_name
        if not html_path.exists():
            raise FileNotFoundError(f"missing source sheet: {html_path}")

        sheet_pdf = OUT / (html_path.stem + ".pdf")
        HTML(filename=str(html_path), base_url=str(SRC)).write_pdf(str(sheet_pdf))
        made.append(sheet_pdf)

        usage_html = USAGE_TEMPLATE.format(title=title, story=story, pdf=pdf_name)
        usage_path = SRC / ("usage-" + html_path.stem + ".html")
        usage_path.write_text(usage_html, encoding="utf-8")
        usage_pdf = USAGE_OUT / ("usage-" + html_path.stem + ".pdf")
        HTML(string=usage_html, base_url=str(SRC)).write_pdf(str(usage_pdf))
        made.append(usage_pdf)

    return made


def main() -> None:
    version = importlib.metadata.version("weasyprint")
    files = build()
    print(f"weasyprint {version}: built {len(files)} PDFs into printables/")
    for f in files:
        print(f"  {f.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
