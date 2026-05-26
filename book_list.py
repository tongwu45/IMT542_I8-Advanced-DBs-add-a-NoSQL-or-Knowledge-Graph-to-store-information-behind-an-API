from flask import Flask, request

import json

app = Flask(__name__)


# ---------------------------------------------------------------------------
# Data loading
#
# The information structure is hosted in a static JSON file (book_list.json).
# It is read once when the server starts and held in memory for the life of
# the process. This satisfies the assignment option of "a static file that
# the endpoint loads on server start" -- no separate database server needed.
# ---------------------------------------------------------------------------

def read_json_file(filename):
    with open(filename) as file:
        data = json.load(file)
    return data


my_dict = read_json_file("book_list.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def is_it_true(value):
    # Used so a query string like ?read=true is interpreted as a boolean.
    return value.lower() == 'true'


def book_summary(b):
    # A short representation: just title and author.
    new = {}
    new['title'] = b['title']
    new['author'] = b['author']
    return new


def book_full(b):
    # The complete record for a single book, copied so the caller cannot
    # accidentally mutate the in-memory data structure.
    new = {}
    new['title'] = b['title']
    new['author'] = b['author']
    new['year'] = b['year']
    new['genre'] = b['genre']
    new['isbn'] = b['isbn']
    new['purchased_date'] = b['purchased_date']
    new['read'] = b['read']
    new['rating'] = b['rating']
    return new


# ===========================================================================
# ORIGINAL ENDPOINTS  (carried over unchanged from the previous assignment)
# ===========================================================================

@app.route('/')
def info():
    message = my_dict['about']
    return message


@app.route('/all_books')
def all_books():
    result = []
    for b in my_dict['entries']:
        result.append(book_summary(b))
    return result


@app.route('/books')
def books():
    author = request.args.get('author')
    read = request.args.get('read', default=False, type=is_it_true)

    result = []

    for b in my_dict['entries']:
        if author == b['author']:
            if read == b['read']:
                result.append(book_summary(b))
    return result


# ===========================================================================
# NEW ENDPOINTS  (added for the group project)
# ===========================================================================

# --- 1. Project metadata --------------------------------------------------
# Returns the descriptive metadata at the top of the JSON structure so a
# client can learn what this API is, who made it, and what is planned.

@app.route('/metadata')
def metadata():
    result = {}
    result['author'] = my_dict['author']
    result['project'] = my_dict['project']
    result['about'] = my_dict['about']
    result['use'] = my_dict['use']
    result['todo'] = my_dict['todo']
    result['total_entries'] = len(my_dict['entries'])
    return result


# --- 2. Full detail for every book ----------------------------------------
# Like /all_books, but returns every field rather than just title/author.

@app.route('/books/details')
def books_details():
    result = []
    for b in my_dict['entries']:
        result.append(book_full(b))
    return result


# --- 3. Look up a single book by ISBN -------------------------------------
# ISBN is the closest thing to a universal identifier in the structure,
# so it is a natural key for fetching one record.

@app.route('/book/<isbn>')
def book_by_isbn(isbn):
    for b in my_dict['entries']:
        if b['isbn'] == isbn:
            return book_full(b)
    # No match: return an explanatory object and a 404 status code.
    return {'error': 'No book found with that ISBN', 'isbn': isbn}, 404


# --- 4. Keyword search across titles --------------------------------------
# /search?q=road  ->  every book whose title contains "road" (case-insensitive)

@app.route('/search')
def search():
    query = request.args.get('q', default='', type=str)
    query = query.lower()

    result = []
    for b in my_dict['entries']:
        if query in b['title'].lower():
            result.append(book_full(b))
    return result


# --- 5. Filter books by genre ---------------------------------------------
# /genre/Fiction  ->  every book in that genre (case-insensitive match)

@app.route('/genre/<genre_name>')
def books_by_genre(genre_name):
    result = []
    for b in my_dict['entries']:
        if b['genre'].lower() == genre_name.lower():
            result.append(book_full(b))
    return result


# --- 6. Filter books by a year range --------------------------------------
# /books/by_year?start=1980&end=2000  ->  books published in that span.
# Either bound may be omitted; defaults cover the whole range.

@app.route('/books/by_year')
def books_by_year():
    start = request.args.get('start', default=0, type=int)
    end = request.args.get('end', default=9999, type=int)

    result = []
    for b in my_dict['entries']:
        if start <= b['year'] <= end:
            result.append(book_full(b))
    return result


# --- 7. The unread reading list, oldest publication first -----------------
# Useful "next to read" view -- only books where read is false.

@app.route('/unread')
def unread():
    result = []
    for b in my_dict['entries']:
        if b['read'] == False:
            result.append(book_full(b))
    result = sorted(result, key=lambda b: b['year'])
    return result


# --- 8. Top-rated books ----------------------------------------------------
# /top?min=5  ->  read books with a rating at or above the threshold,
# sorted from highest rating to lowest. Books with no rating are skipped.

@app.route('/top')
def top_rated():
    minimum = request.args.get('min', default=4, type=int)

    result = []
    for b in my_dict['entries']:
        if b['rating'] is not None and b['rating'] >= minimum:
            result.append(book_full(b))
    result = sorted(result, key=lambda b: b['rating'], reverse=True)
    return result


# --- 9. Aggregate statistics about the collection -------------------------
# A computed summary -- demonstrates the API returning derived data, not
# just stored records.

@app.route('/stats')
def stats():
    entries = my_dict['entries']

    total = len(entries)
    read_count = 0
    rated = []
    genre_counts = {}
    author_counts = {}

    for b in entries:
        if b['read']:
            read_count += 1
        if b['rating'] is not None:
            rated.append(b['rating'])
        # Count books per genre.
        g = b['genre']
        genre_counts[g] = genre_counts.get(g, 0) + 1
        # Count books per author.
        a = b['author']
        author_counts[a] = author_counts.get(a, 0) + 1

    result = {}
    result['total_books'] = total
    result['read'] = read_count
    result['unread'] = total - read_count

    if len(rated) > 0:
        result['average_rating'] = round(sum(rated) / len(rated), 2)
    else:
        result['average_rating'] = None
    result['rated_books'] = len(rated)

    result['books_per_genre'] = genre_counts
    result['books_per_author'] = author_counts
    return result


# --- 10. The list of distinct authors -------------------------------------
# A convenience endpoint so a client (e.g. the React app) can populate a
# dropdown without downloading every book.

@app.route('/authors')
def authors():
    seen = []
    for b in my_dict['entries']:
        if b['author'] not in seen:
            seen.append(b['author'])
    seen = sorted(seen)
    return seen


# --- 11. The list of distinct genres --------------------------------------

@app.route('/genres')
def genres():
    seen = []
    for b in my_dict['entries']:
        if b['genre'] not in seen:
            seen.append(b['genre'])
    seen = sorted(seen)
    return seen


if __name__ == '__main__':
    # debug=True gives auto-reload and readable error pages while developing.
    app.run(debug=True, port=5000)
