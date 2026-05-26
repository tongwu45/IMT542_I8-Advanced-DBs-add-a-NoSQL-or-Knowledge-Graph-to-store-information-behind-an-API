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

