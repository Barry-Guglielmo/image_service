import sqlite3

def create_db(db = 'plots.db'):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY,
        top_folder TEXT,
        middle_folder TEXT,
        bottom_folder TEXT,
        image_data BLOB
    )
    ''')

