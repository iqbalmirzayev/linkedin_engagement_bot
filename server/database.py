import sqlite3

def get_db_connection():
    conn = sqlite3.connect("/root/updated_linkedin_server/updated_linkedin_server/central.db")
    conn.row_factory = sqlite3.Row
    return conn


