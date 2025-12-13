import sqlite3
import os
def create_config_db():
    # Ensure userData directory exists
    if not os.path.exists('userData'):
        os.makedirs('userData')
    conn = sqlite3.connect('userData/config.db')
    cursor = conn.cursor()

    # Create songs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT,
            album TEXT,
            duration INTEGER,
            url TEXT UNIQUE,
            thumbnail TEXT
        )
    ''')

    # Create playlists table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS playlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create playlist_songs table (many-to-many)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS playlist_songs (
            playlist_id INTEGER,
            song_id INTEGER,
            position INTEGER,
            PRIMARY KEY (playlist_id, song_id),
            FOREIGN KEY (playlist_id) REFERENCES playlists(id) ON DELETE CASCADE,
            FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()

def add_song_to_library(title, artist, album, duration, url, thumbnail):
    conn = sqlite3.connect('userData/config.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO songs (title, artist, album, duration, url, thumbnail)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, artist, album, duration, url, thumbnail))
    conn.commit()
    conn.close()

def add_playlist(name, description):
    conn = sqlite3.connect('userData/config.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO playlists (name, description)
        VALUES (?, ?)
    ''', (name, description))
    conn.commit()
    conn.close()

def add_song_to_playlist(playlist_id, song_id, position):
    conn = sqlite3.connect('userData/config.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO playlist_songs (playlist_id, song_id, position)
        VALUES (?, ?, ?)
    ''', (playlist_id, song_id, position))
    conn.commit()
    conn.close()