import aiosqlite

DB_FILE = "movies_cache.db"

async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                movie_id TEXT PRIMARY KEY,
                title TEXT,
                imdb_rating TEXT,
                timestamp INTEGER
            )
        ''')
        await db.commit()

async def get_movie(movie_id):
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute("SELECT title, imdb_rating, timestamp FROM movies WHERE movie_id=?", (movie_id,))
        row = await cursor.fetchone()
        if row:
            return {"movie_id": movie_id, "title": row[0], "imdb_rating": row[1], "timestamp": row[2]}
        return None

async def save_movie(movie_id, title, imdb_rating, timestamp):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            "INSERT OR REPLACE INTO movies (movie_id, title, imdb_rating, timestamp) VALUES (?, ?, ?, ?)",
            (movie_id, title, imdb_rating, timestamp)
        )
        await db.commit()
