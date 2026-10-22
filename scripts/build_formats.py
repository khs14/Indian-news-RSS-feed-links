#!/usr/bin/env python3
"""Regenerate every data file from the source CSV. Optional: only needed after editing the data.

    python scripts/build_formats.py

Reads  data/full/news_rss_link_db.csv  (the source of truth)
Writes data/full/          every format, all 221 rows
       data/english-only/  every format, only rows where language == "en"

Standard library only, except two optional formats:
    XLSX    needs openpyxl   (pip install openpyxl)
    Parquet needs pyarrow    (pip install pyarrow)
"""

from __future__ import annotations

import csv
import json
import sqlite3
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "full" / "news_rss_link_db.csv"
STEM = "news_rss_link_db"
COLUMNS = ["id", "link", "language", "region", "latitude", "longitude", "time_zone", "source"]


def read_source():
    """Rows as raw strings, exactly as written in the CSV."""
    with open(SOURCE, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            sys.exit(f"{SOURCE} is missing columns: {', '.join(missing)}")
        return list(reader)


def typed(row):
    """One row with real types; empty cells become None."""
    def text(key):
        return row[key].strip() or None

    def number(key):
        return float(row[key]) if row[key].strip() else None

    return {
        "id": int(row["id"]),
        "link": row["link"].strip(),
        "language": row["language"].strip(),
        "region": text("region"),
        "latitude": number("latitude"),
        "longitude": number("longitude"),
        "time_zone": row["time_zone"].strip(),
        "source": row["source"].strip(),
    }


def write_text(path, content):
    path.write_text(content, encoding="utf-8", newline="\n")


def write_delimited(path, raw_rows, delimiter):
    # Raw strings keep the source formatting (for example "85.3250" stays "85.3250").
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, delimiter=delimiter, lineterminator="\n")
        writer.writerow(COLUMNS)
        for row in raw_rows:
            writer.writerow([row[c] for c in COLUMNS])


def label(row):
    return f"{row['source']} · {row['region']}" if row["region"] else f"{row['source']} #{row['id']}"


def build_opml(rows):
    root = ET.Element("opml", version="2.0")
    ET.SubElement(ET.SubElement(root, "head"), "title").text = "News RSS feeds (India)"
    body = ET.SubElement(root, "body")
    folders = {}
    for r in rows:
        if r["source"] not in folders:
            folders[r["source"]] = ET.SubElement(body, "outline", text=r["source"], title=r["source"])
        ET.SubElement(folders[r["source"]], "outline", type="rss", text=label(r), title=label(r),
                      xmlUrl=r["link"], language=r["language"])
    ET.indent(root)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="unicode") + "\n"


def build_geojson(rows):
    features = [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [r["longitude"], r["latitude"]]},
            "properties": {k: r[k] for k in COLUMNS if k not in ("latitude", "longitude")},
        }
        for r in rows
        if r["latitude"] is not None and r["longitude"] is not None
    ]
    return json.dumps({"type": "FeatureCollection", "features": features},
                      ensure_ascii=False, indent=2) + "\n"


def write_sqlite(path, rows):
    path.unlink(missing_ok=True)
    db = sqlite3.connect(path)
    db.execute("""CREATE TABLE feeds (
        id INTEGER PRIMARY KEY, link TEXT NOT NULL UNIQUE, language TEXT NOT NULL, region TEXT,
        latitude REAL, longitude REAL, time_zone TEXT NOT NULL, source TEXT NOT NULL)""")
    db.executemany("INSERT INTO feeds VALUES (?,?,?,?,?,?,?,?)",
                   [tuple(r[c] for c in COLUMNS) for r in rows])
    for col in ("source", "language", "region"):
        db.execute(f"CREATE INDEX idx_feeds_{col} ON feeds({col})")
    db.commit()
    db.close()


def write_xlsx(path, rows):
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font
        from openpyxl.utils import get_column_letter
    except ImportError:
        sys.exit("XLSX needs openpyxl:  pip install openpyxl")
    wb = Workbook()
    ws = wb.active
    ws.title = "feeds"
    ws.append(COLUMNS)
    for cell in ws[1]:
        cell.font = Font(bold=True)
    for r in rows:
        ws.append([r[c] for c in COLUMNS])
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    for i, col in enumerate(COLUMNS, start=1):
        widest = max([len(col)] + [len(str(r[col] or "")) for r in rows])
        ws.column_dimensions[get_column_letter(i)].width = min(widest + 2, 80)
    wb.save(path)


def write_parquet(path, rows):
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
    except ImportError:
        sys.exit("Parquet needs pyarrow:  pip install pyarrow")
    types = {"id": pa.int64(), "latitude": pa.float64(), "longitude": pa.float64()}
    table = pa.table({c: pa.array([r[c] for r in rows], types.get(c, pa.string())) for c in COLUMNS})
    pq.write_table(table, path, compression="zstd")


def build_set(out_dir, raw_rows, write_csv):
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = [typed(r) for r in raw_rows]
    f = lambda ext: out_dir / f"{STEM}.{ext}"  # noqa: E731

    if write_csv:  # the full set's CSV is the untouched source file
        write_delimited(f("csv"), raw_rows, ",")
    write_delimited(f("tsv"), raw_rows, "\t")
    write_text(f("json"), json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    write_text(f("jsonl"), "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    write_text(f("txt"), "".join(r["link"] + "\n" for r in rows))
    write_text(f("opml"), build_opml(rows))
    write_text(f("geojson"), build_geojson(rows))
    write_sqlite(f("sqlite"), rows)
    write_xlsx(f("xlsx"), rows)
    write_parquet(f("parquet"), rows)
    print(f"{out_dir.relative_to(ROOT)}: {len(rows)} feeds")


def main():
    raw = read_source()
    build_set(ROOT / "data" / "full", raw, write_csv=False)
    english = [r for r in raw if r["language"].strip() == "en"]
    build_set(ROOT / "data" / "english-only", english, write_csv=True)


if __name__ == "__main__":
    main()
