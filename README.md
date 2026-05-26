# IMT542_I8-Advanced-DBs-add-a-NoSQL-or-Knowledge-Graph-to-store-information-behind-an-API

# Book List API — Extended Version

This is the second iteration of the **Portable Information Structure for Books I Read**
project. It builds directly on the previous individual assignment (`book_list-1.py`)
by adding new functions that return more of the data held in the information
structure.

## How data is hosted

The information structure lives in a **static JSON file** (`book_list.json`).
The Flask app reads it **once when the server starts** (`read_json_file(...)`)
and holds it in memory for the life of the process. This satisfies the
assignment requirement of "a static file that the endpoint loads on server
start" — no separate database server is required.

## Running the server

Requires Python 3 and Flask.

```bash
pip install flask
python book_list.py
```

The server starts on `http://127.0.0.1:5000`. Open that address in a browser
or use `curl` to hit any endpoint below.

## Endpoints

### Original endpoints (unchanged from the first assignment)

| Method & path | Description |
|---|---|
| `GET /` | Returns the project "about" description. |
| `GET /all_books` | Title + author for every book. |
| `GET /books?author=<name>&read=<true/false>` | Books matching an author and read state. |

### New endpoints (added for the group project)

| Method & path | Description |
|---|---|
| `GET /metadata` | Project metadata (author, project, about, use, todo) plus a count of entries. |
| `GET /books/details` | Every field for every book, not just title/author. |
| `GET /book/<isbn>` | Full record for one book, looked up by its ISBN. Returns HTTP 404 if not found. |
| `GET /search?q=<text>` | Books whose title contains the given text (case-insensitive). |
| `GET /genre/<genre_name>` | Every book in a given genre (case-insensitive). |
| `GET /books/by_year?start=<y>&end=<y>` | Books published within a year range. Either bound is optional. |
| `GET /unread` | Books not yet read, sorted oldest publication first. |
| `GET /top?min=<n>` | Read books with a rating >= n, sorted highest first. |
| `GET /stats` | Computed statistics: totals, average rating, counts per genre and per author. |
| `GET /authors` | Sorted list of the distinct authors. |
| `GET /genres` | Sorted list of the distinct genres. |

## Example requests

```bash
curl http://127.0.0.1:5000/metadata
curl http://127.0.0.1:5000/book/978-0-307-26543-2
curl "http://127.0.0.1:5000/search?q=road"
curl http://127.0.0.1:5000/genre/Fiction
curl "http://127.0.0.1:5000/books/by_year?start=1980&end=2000"
curl http://127.0.0.1:5000/unread
curl "http://127.0.0.1:5000/top?min=5"
curl http://127.0.0.1:5000/stats
curl http://127.0.0.1:5000/authors
curl http://127.0.0.1:5000/genres
```

## Video demonstration script

A suggested ~3 minute walkthrough for the second video:

1. **Intro (15s)** — "This is the second video for our group project. It builds
   on the book list API from the individual assignment by adding new functions
   that return more data from the information structure."

2. **Show the data source (20s)** — Open `book_list.json`. Point out the
   metadata block at the top and the `entries` array. Explain the API loads
   this static file once on server start.

3. **Start the server (15s)** — Run `python book_list.py` in the terminal.
   Show the "Running on http://127.0.0.1:5000" line.

4. **Original endpoints still work (20s)** — In the browser, visit `/`,
   `/all_books`, and `/books?author=Saul Bellow&read=true`. Note these are
   carried over unchanged.

5. **New endpoints (90s)** — Visit each new endpoint and briefly say what it
   returns:
   - `/metadata` — the project description fields.
   - `/books/details` — the full records.
   - `/book/978-0-307-26543-2` — one book by ISBN; then try a fake ISBN to
     show the 404 error response.
   - `/search?q=road` — keyword title search.
   - `/genre/Fiction` — filter by genre.
   - `/books/by_year?start=1980&end=2000` — filter by year range.
   - `/unread` — the reading list.
   - `/top?min=5` — highest-rated books.
   - `/stats` — computed statistics (highlight average rating and the per-genre
     counts — this is derived data, not just stored records).
   - `/authors` and `/genres` — the distinct value lists.

6. **Wrap up (15s)** — Mention the data is a static JSON file loaded at server
   start, and that the project's `todo` list (visible in `/metadata`) names
   database support as a future step.

