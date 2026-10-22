# Indian News RSS Feed Links

A dataset of **news RSS feed links** from Indian publishers, with the language, region,
coordinates and publisher of each feed. It is published here in **ten file formats** so you
can open it in whatever tool you already use: Excel, Google Sheets, pandas, SQL, a feed reader,
a map, or a few lines of shell.

> 221 feeds · 18 publishers · 203 feeds with coordinates · 74 feeds in English

---

## Scope and disclaimer

**Intended scope: English-language news from the Indian region only.**

- **Geography.** Every feed is from an Indian publisher and covers an Indian city, state or the
  whole country. This dataset is not meant for, and does not cover, news from other regions.
- **Language.** The intended focus is English. The full dataset also contains **147
  non-English feeds** (146 Hindi from Amar Ujala and 1 Gujarati from Gujarat Samachar) that
  fall outside this scope. They are kept in [`data/full/`](data/full/) so nothing is lost.
  If you only want in-scope data, use **[`data/english-only/`](data/english-only/)**, which
  holds the 74 English feeds.
- **Links, not news.** The dataset lists feed URLs and metadata only. The articles behind the
  links belong to the publishers, and their terms of use apply to anything you download, store
  or republish.
- **A snapshot.** Feeds move, change format, get paywalled or disappear. The file does not
  record when it was collected or whether each link works. Test a link before relying on it.
- **Approximate coordinates.** They describe the city or state a feed covers, not where the
  publisher is based, and a few look wrong (see [Known data issues](#known-data-issues)).
- **Uneven coverage.** Publishers contribute between 1 and 146 feeds each. Feed counts reflect
  how a publisher organises its feeds, not how much news a place produces.
- **No affiliation.** This project is not affiliated with or endorsed by any publisher listed.

---

## What is in this repository

```text
Indian-news-RSS-feed-links/
├── README.md
├── LICENSE
├── data/
│   ├── english-only/          ← 74 English-language feeds (the intended scope)
│   │   └── news_rss_link_db.{csv, tsv, json, jsonl, txt, opml, geojson, sqlite, xlsx, parquet}
│   └── full/                  ← all 221 feeds: English first (ids 1 to 74), then Hindi and Gujarati
│       └── news_rss_link_db.{csv, tsv, json, jsonl, txt, opml, geojson, sqlite, xlsx, parquet}
└── scripts/
    └── build_formats.py       ← optional: regenerates every format from the source CSV
```

**Which folder should I use?** Start with `english-only/`. Use `full/` only if you also need the
Hindi and Gujarati feeds. Both folders have the same ten files with the same columns.

## The ten formats

Every format contains the same data. Pick the one that suits your tool.

| Format     | File                       | Use it for                                                                                                       |
| ---------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| CSV        | `news_rss_link_db.csv`     | Excel, Google Sheets, pandas, R, almost everything. This is the source file the other formats are generated from |
| TSV        | `news_rss_link_db.tsv`     | Tools that choke on commas                                                                                       |
| JSON       | `news_rss_link_db.json`    | Web apps, APIs, JavaScript, `jq`. An array of objects; missing values are `null`                                 |
| JSON Lines | `news_rss_link_db.jsonl`   | Streaming and big-data tools. One feed per line                                                                  |
| TXT        | `news_rss_link_db.txt`     | Just the feed URLs, one per line. Shell loops and simple readers                                                 |
| OPML       | `news_rss_link_db.opml`    | Importing into a feed reader (Feedly, Inoreader, NetNewsWire and others). One folder per publisher               |
| GeoJSON    | `news_rss_link_db.geojson` | Maps and GIS (QGIS, Leaflet, geojson.io). Only feeds with coordinates are included                               |
| SQLite     | `news_rss_link_db.sqlite`  | SQL queries. Table `feeds`, indexed on `source`, `language` and `region`                                         |
| Excel      | `news_rss_link_db.xlsx`    | Non-programmers. Header row frozen, filters on                                                                   |
| Parquet    | `news_rss_link_db.parquet` | Data science tools and warehouses. Typed columns, compressed                                                     |

All files are small (the largest is under 100 KB), so you can clone the repository or download
single files from GitHub's "Raw" button.

---

## Dataset description

One row per feed. The same eight columns appear in every format (GeoJSON stores the coordinates
as geometry and the rest as properties; TXT keeps only `link`).

| Column      | Type                  | Description                                                                                                                                                                                                                                                   |
| ----------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`        | integer               | Unique identifier, numbered 1 to 221 in row order with no gaps. English feeds come first (1 to 74), so the same feed has the same `id` in both folders                                                                                                        |
| `link`      | text (URL)            | The RSS feed address. Unique across the dataset                                                                                                                                                                                                               |
| `language`  | text                  | Language of the articles: `en` (English), `hi` (Hindi), `gj` (Gujarati). `gj` is this dataset's own code; if you join with other data, note that the ISO 639-1 code for Gujarati is `gu`                                                                      |
| `region`    | text, may be empty    | City, state or district the feed covers. A place that publishers name in more than one way is stored under a single name (for example `Bengaluru`, not `Bangalore`). Empty for national or aggregate feeds                                                    |
| `latitude`  | decimal, may be empty | Approximate latitude of the region (WGS84). Empty when `region` is empty                                                                                                                                                                                      |
| `longitude` | decimal, may be empty | Approximate longitude of the region (WGS84)                                                                                                                                                                                                                   |
| `time_zone` | text                  | The time zone the feed itself uses for its publish times: `IST` (UTC+05:30) or `GMT` (UTC+00:00). Most feeds use IST; a few publishers, for example Tribune, DNA and Zee News, publish in GMT. It describes the feed's timestamps, not where the news is from |
| `source`    | text                  | Publisher short name, such as `TOI` or `HT`                                                                                                                                                                                                                   |

### At a glance

|                                                   | `english-only/` | `full/`         |
| ------------------------------------------------- | --------------- | --------------- |
| Feeds                                             | 74              | 221             |
| Publishers                                        | 16              | 18              |
| Feeds with coordinates                            | 56              | 203             |
| Feeds without coordinates (national or aggregate) | 18              | 18              |
| Distinct regions                                  | 44              | 172             |
| `time_zone`                                       | IST 60, GMT 14  | IST 206, GMT 15 |

English-language feeds by publisher: Times of India (`TOI`) 32, Hindustan Times (`HT`) 17,
The Tribune (`Tribune`) 10, The Hindu (`Hindu`) 2, One India 2, and one each for Mint, News18,
DNA, First Post, India Today, Free Press Journal, Deccan Chronicle, abp, Latestly, Zee News and
India TV. The Hindi feeds are all from Amar Ujala.

### Things to know when using the data

- **Place names are normalized.** When publishers spell the same place differently (for
  example _Bangalore_ and _Bengaluru_, or _Gurgaon_ and _Gurugram_), the dataset stores it under
  one name. A region filter such as `region == "Bengaluru"` therefore finds every feed for that
  city. If you join this data with other data that uses a different spelling, map the names
  first.
- **`time_zone` is about the feed's timestamps.** Use it as a hint when a feed's publish
  times carry no explicit offset. It says nothing about the city.
- **Region detail varies.** Some regions are cities (`Pune`), some are states (`Punjab`), some
  are districts. Coordinates are a representative point, not a boundary.
- **Several feeds can share a region.** Mumbai has a TOI and an HT feed, so a story may appear
  in both. De-duplicate articles by link or title after downloading.

### Known data issues

These were found by checking the file; none has been verified against the publishers, and the
first two are judgement calls from the coordinates and neighbouring rows, so treat them as
suspicions, not facts. Row numbers are the `id` values.

| Issue                                                                                                                                                | Where                                                                      | Suggested fix                         |
| ---------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------- |
| Coordinates probably belong to the wrong place. Both could be in one of two states                                                                   | ids 134 (`Hamirpur`) and 217 (`Bilaspur`), `full/` only                    | Check which state's feed each one is  |
| `Hamirpur` (134) and `Hamirpur Hp` (220) have identical coordinates, but there are two different Hamirpurs, in Uttar Pradesh and in Himachal Pradesh | ids 134 and 220, `full/` only                                              | Fix 134 once you know which one it is |
| Region labels that mix two names or add an abbreviation                                                                                              | `Hamirpur Hp`, `Jhajjar Bahadurgarh`, `Mahendragarh Narnaul`, `full/` only | Use one consistent naming style       |
| Plain `http://` link                                                                                                                                 | id 1                                                                       | Try `https://`                        |

Corrections with evidence are welcome (see [Contributing](#contributing)).

---

## Open it in your tool

**Excel or Google Sheets.** Open `news_rss_link_db.xlsx` (Excel), or import the CSV
(Google Sheets: File, Import, Upload).

**Feed reader.** Import `news_rss_link_db.opml` through your reader's _Import OPML_ option.
You get one folder per publisher. To follow a single city, delete the other folders.

**Python with pandas.**

```python
import pandas as pd

df = pd.read_csv("data/english-only/news_rss_link_db.csv")
df = pd.read_json("data/english-only/news_rss_link_db.jsonl", lines=True, precise_float=True)
df = pd.read_parquet("data/english-only/news_rss_link_db.parquet")
df = pd.read_excel("data/english-only/news_rss_link_db.xlsx")   # needs openpyxl
```

(`precise_float=True` stops pandas adding rounding noise to the coordinates when reading JSON.)

**Python, no extra packages.**

```python
import csv

with open("data/english-only/news_rss_link_db.csv", newline="", encoding="utf-8") as fh:
    feeds = list(csv.DictReader(fh))

pune = [f["link"] for f in feeds if f["region"] == "Pune"]
```

**SQL (SQLite).**

```bash
sqlite3 data/english-only/news_rss_link_db.sqlite \
  "SELECT region, COUNT(*) AS feeds FROM feeds WHERE region IS NOT NULL
   GROUP BY region ORDER BY feeds DESC, region LIMIT 5"
```

**Shell with `jq`.**

```bash
jq -r '.[] | select(.source=="TOI") | .link' data/english-only/news_rss_link_db.json
```

**JavaScript (Node.js).**

```javascript
const fs = require("fs");
const feeds = JSON.parse(
  fs.readFileSync("data/english-only/news_rss_link_db.json", "utf8"),
);
const mumbai = feeds.filter((f) => f.region === "Mumbai").map((f) => f.link);
```

**Maps.** Drag `news_rss_link_db.geojson` into QGIS or geojson.io to see every feed as a point.

**Straight from GitHub**, without downloading anything first:

```python
import pandas as pd
url = "https://raw.githubusercontent.com/khs14/Indian-news-RSS-feed-links/main/data/english-only/news_rss_link_db.csv"
df = pd.read_csv(url)
```

---

## Example: what the data itself tells you

Questions you can answer without downloading a single article. Which places have feeds from
more than one English-language publisher?

```python
import pandas as pd

df = pd.read_csv("data/english-only/news_rss_link_db.csv")

coverage = (
    df.dropna(subset=["region"])
      .groupby("region")["source"].agg(feeds="count", publishers="nunique")
      .sort_values(["publishers", "feeds"], ascending=False)
)
print(coverage.head(8))
```

```text
            feeds  publishers
region
Bengaluru       2           2
Chandigarh      2           2
Delhi           2           2
Gurugram        2           2
Jaipur          2           2
Kolkata         2           2
Lucknow         2           2
Mumbai          2           2
```

Of the 44 places with English-language feeds, **12 have two feeds, one from TOI and one from HT**
(Bengaluru, Chandigarh, Delhi, Gurugram, Jaipur, Kolkata, Lucknow, Mumbai, Noida, Patna, Pune and
Ranchi). The other 32 have a single feed. Largest publishers by feed count:

```python
print(df.groupby("source").size().sort_values(ascending=False).head(5))
```

```text
source
TOI          32
HT           17
Tribune      10
Hindu         2
One India     2
```

---

## Real-world applications

These show how a list of feed links turns into something useful. In each case the dataset
supplies _which feeds to read_; you supply the reader, the filters and the judgement.

| Application                                                                                                                                   | How the dataset is used                                                                                                                                      | Worth knowing                                                                                                                         |
| --------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Media and brand monitoring.** A communications team wants to know when its company, product or competitor is mentioned in the Indian press. | Load `english-only` feeds, download them on a schedule, and flag articles whose title or summary contains your keywords. The example script below does this. | Feeds carry headlines and short summaries, not full text. A mention buried in an article body will be missed.                         |
| **A local news reader.** A resident or a journalist wants one place for the news of their own city.                                           | Filter by `region` (for example Pune), import the matching feeds from the OPML or the filtered CSV into a feed reader.                                       | Several publishers may report the same story, so expect duplicates.                                                                   |
| **Weather and civic watch.** A logistics or events team wants early signals about flooding, strikes or road closures in particular cities.    | Pick the feeds for the cities you operate in and watch for words such as _flood_, _cyclone_, _strike_, _power cut_.                                          | News feeds are a lagging, unofficial signal. Use the official meteorological and disaster agencies for safety decisions.              |
| **Business and policy tracking.** An analyst or student follows interest-rate, tax and regulation news.                                       | Use the business-leaning feeds (for example Mint) and national feeds, filtered on terms like _repo rate_ or _GST_.                                           | This keeps you informed. It is not investment advice or a trading signal.                                                             |
| **A research corpus.** A researcher studies how Indian English-language media cover a topic over months.                                      | Use the feed list as a sampling frame: download headlines and summaries daily into a table and analyse them.                                                 | Store only what you need and check the publishers' terms before sharing text. A feed is a publisher's selection, not a random sample. |
| **Coverage and media-landscape mapping.** A journalism student or NGO maps which cities have English-language feeds from which publishers.    | Load the GeoJSON in QGIS, or run the pandas example above.                                                                                                   | Feed counts show how publishers organise feeds, not how much news a place produces.                                                   |
| **Teaching.** A class learns to parse RSS, clean data and de-duplicate.                                                                       | The dataset is small, real, and has real quirks (inconsistent region labels, suspect coordinates, an `http` link) to find and fix.                           | The [known issues](#known-data-issues) double as exercises.                                                                           |
| **Feed-health tracking.** A maintainer wants to know which links have died.                                                                   | Loop over the TXT file, request each URL and record the HTTP status and newest article date.                                                                 | Be gentle: see [Using feeds responsibly](#using-feeds-responsibly).                                                                   |

### End-to-end example: keyword monitor

A complete script that reads the dataset, downloads each English feed and prints new articles
that mention your keywords. It remembers what it has shown, so you can run it every hour or
two without repeats. Save it as `monitor.py` next to `data/`, then run `pip install feedparser`
and `python monitor.py`.

```python
# monitor.py: print new articles that mention your keywords
import csv, json, re, time
from pathlib import Path

import feedparser   # pip install feedparser

KEYWORDS = ["repo rate", "monsoon", "election"]            # edit these
FEEDS = "data/english-only/news_rss_link_db.csv"           # which feeds to read
SEEN_FILE = Path("seen.json")                              # remembers what was shown

pattern = re.compile("|".join(rf"\b{re.escape(k)}\b" for k in KEYWORDS), re.IGNORECASE)
seen = set(json.loads(SEEN_FILE.read_text())) if SEEN_FILE.exists() else set()

with open(FEEDS, newline="", encoding="utf-8") as fh:
    for feed in csv.DictReader(fh):
        parsed = feedparser.parse(feed["link"], agent="my-news-monitor/1.0")
        for entry in parsed.entries:
            link = entry.get("link", "")
            text = f'{entry.get("title", "")} {entry.get("summary", "")}'
            if link and link not in seen and pattern.search(text):
                seen.add(link)
                print(f'[{feed["source"]} {feed["region"] or "national"}] {entry.get("title")}')
                print(f"   {link}")
        time.sleep(1)                                      # be polite to the websites

SEEN_FILE.write_text(json.dumps(sorted(seen)))
```

The first run reports everything that currently matches. To start fresh and only see later
stories, run it once and ignore the output.

---

## Using feeds responsibly

- **Go slowly.** Many feeds share one website (146 of the 221 are on `amarujala.com`, 32 on
  `timesofindia.indiatimes.com`). Request them one at a time with a pause between requests, and
  do not poll more than every 15 to 60 minutes. News feeds do not change faster than that.
- **Identify yourself** with a descriptive User-Agent, as the example above does.
- **Respect the publishers' terms and `robots.txt`.** Feeds are meant for reading headlines and
  links. Check the terms before storing or republishing article text.
- **Expect failures.** Some links will be dead, blocked or slow. Handle errors rather than
  assuming every feed works.

---

## Regenerating the files

The CSV in `data/full/` is the source of truth. Every other file is
generated from it. If you edit the CSV, rebuild all formats with:

```bash
pip install openpyxl pyarrow     # only needed for the Excel and Parquet files
python scripts/build_formats.py
```

The script uses only the Python standard library apart from those two packages. It rewrites both
`data/full/` and `data/english-only/`. It is a convenience, not a library: delete it if you do not
need it.

## Contributing

Corrections and additions are welcome. Open an issue or a pull request that says what is wrong
(or what is missing) and gives your evidence, for example the publisher's own RSS page. Keep to
the scope: English-language news from India. If you add or change a row, edit
`data/full/news_rss_link_db.csv` (new `id` = current highest plus one; never renumber or reuse
ids once published; use one name per place, for example `Bengaluru`), then run
`python scripts/build_formats.py` so every format stays in sync.

## License

Released under the [MIT License](LICENSE). The feed URLs are references to publicly published
feeds. The content behind them is owned by the respective publishers and is not covered by this
license.
