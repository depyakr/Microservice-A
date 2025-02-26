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


@app.route('/')
def home():
    """Check if the microservice is running."""
    return jsonify({"message": "Sightword Microservice is running"}), 200


@app.route('/sightword/random', methods=['GET'])
def get_random_sightword():
    """Returns a random sightword based on optional filters."""
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT word FROM sightwords WHERE LENGTH(word) <= 5"
        params = []

        if category:
            query += " AND category = ?"
            params.append(category)
        if difficulty:
            query += " AND difficulty = ?"
            params.append(difficulty)

        cursor.execute(query, tuple(params))
        words = cursor.fetchall()
        conn.close()

        if not words:
            return jsonify({"error": "No matching words found"}), 404

        selected_word = random.choice(words)["word"]  # Convert row to dictionary
        return jsonify({"word": selected_word}), 200

    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/sightword/add', methods=['POST'])
def add_sightword():
    """Adds a new sightword to the database."""
    if not request.is_json:
        return jsonify({"error": "Invalid request, expected JSON"}), 400

    data = request.get_json()

    word = data.get('word')
    category = data.get('category')
    difficulty = data.get('difficulty')

    if not all([word, category, difficulty]):
        return jsonify({"error": "Missing required fields"}), 400

    if len(word) > 5:
        return jsonify({"error": "Word must be 5 characters or less"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sightwords (word, category, difficulty)
            VALUES (?, ?, ?)
        """, (word, category, difficulty))
        conn.commit()
        conn.close()
        return jsonify({"message": "Sightword added successfully"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Word already exists"}), 409
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


if __name__ == '__main__':
    initialize_db()
    app.run(host='127.0.0.1', port=5000, debug=True)
