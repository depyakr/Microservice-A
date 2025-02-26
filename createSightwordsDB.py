import sqlite3

DB_FILE = "sightwords.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS sightwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    difficulty TEXT NOT NULL
)
''')

sightwords_data = [
    # Nouns
    ("cat", "noun", "easy"),
    ("dog", "noun", "easy"),
    ("ball", "noun", "easy"),
    ("tree", "noun", "medium"),
    ("book", "noun", "medium"),
    ("car", "noun", "medium"),
    ("house", "noun", "hard"),
    ("apple", "noun", "hard"),
    ("chair", "noun", "hard"),

    # Adjectives
    ("big", "adjective", "easy"),
    ("small", "adjective", "easy"),
    ("hot", "adjective", "easy"),
    ("cold", "adjective", "medium"),
    ("fast", "adjective", "medium"),
    ("slow", "adjective", "medium"),
    ("happy", "adjective", "hard"),
    ("sad", "adjective", "hard"),
    ("tall", "adjective", "hard"),

    # Verbs
    ("run", "verb", "easy"),
    ("jump", "verb", "easy"),
    ("walk", "verb", "easy"),
    ("eat", "verb", "medium"),
    ("play", "verb", "medium"),
    ("read", "verb", "medium"),
    ("write", "verb", "hard"),
    ("draw", "verb", "hard"),
    ("swim", "verb", "hard"),
]

cursor.executemany('''
INSERT OR IGNORE INTO sightwords (word, category, difficulty)
VALUES (?, ?, ?)
''', sightwords_data)

conn.commit()
conn.close()

print("Database setup complete!")
