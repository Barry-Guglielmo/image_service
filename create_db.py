import sqlite3
from config import *

def create_db(db = IMAGE_DB):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY,
        first TEXT,
        second TEXT,
        file_name TEXT,
        image_data BLOB
    )
    ''')

if __name__ == '__main__':
    create_db()