from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import random

app = Flask(__name__)
CORS(app)

DB_FILE = "sightwords.db"


def get_db_connection():
    """Establish a database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Allows column access by name
    return conn


def initialize_db():
    """Create the database schema if it does not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sightwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            difficulty TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def set_query_and_params(category, difficulty):
    """Helper function for get_random_sightword(). Builds query string and parameters list."""
    query_string, params = "SELECT word FROM sightwords WHERE LENGTH(word) <= 5", []

    if category:
        query_string += " AND category = ?"
        params.append(category)
    if difficulty:
        query_string += " AND difficulty = ?"
        params.append(difficulty)

    return query_string, params


def execute_query(query, params):
    """Helper function for get_random_sightword(). Executes a db query and returns results."""
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(query, tuple(params))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {str(e)}")  # log error
        return []


def insert_sightword(word, category, difficulty):
    """Helper function for add_sightword(). Inserts given arguments in database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO sightwords (word, category, difficulty) VALUES (?, ?, ?)""",
                   (word, category, difficulty))
    conn.commit()
    conn.close()


def try_insert(insert_funct, arg1, arg2, arg3):
    """Helper function for add_sightword(). Executes given function while handling errors."""
    try:
        insert_funct(arg1, arg2, arg3)  # call from within try block
        return jsonify({"message": "Sightword added successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Word already exists"}), 409
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/')
def home():
    """Check if the microservice is running."""
    return jsonify({"message": "Sightword Microservice is running"}), 200


@app.route('/sightword/random', methods=['GET'])
def get_random_sightword():
    """Returns a random sightword based on optional filters."""

    categ, difficulty = request.args.get('category'), request.args.get('difficulty')
    query, params = set_query_and_params(categ, difficulty)
    words = execute_query(query, params)

    if not words:
        return jsonify({"error": "No matching words found"}), 404

    selected_word = random.choice(words)[0]     # get first word
    return jsonify({"word": selected_word}), 200


@app.route('/sightword/add', methods=['POST'])
def add_sightword():
    """Adds a new sightword to the database."""
    if not request.is_json:
        return jsonify({"error": "Invalid request, expected JSON"}), 400

    data = request.get_json()
    word, category, difficulty = data.get('word'), data.get('category'), data.get('difficulty')

    if not all([word, category, difficulty]):
        return jsonify({"error": "Missing required fields"}), 400
    if len(word) > 5:
        return jsonify({"error": "Word must be 5 characters or less"}), 400

    return try_insert(insert_sightword, word, category, difficulty)


if __name__ == '__main__':
    initialize_db()
    app.run(host='127.0.0.1', port=5000, debug=True)
