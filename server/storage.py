import sqlite3

# Verilənlər bazasına bağlantı funksiyası
# Hər ikisində
def get_connection(): return sqlite3.connect("central.db")


# Cədvəli yaradın (əgər mövcud deyilsə)
def create_links_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id TEXT,
            link TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Yeni link əlavə et
def save_link(telegram_id: str, link: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO links (telegram_id, link) VALUES (?, ?)", (telegram_id, link))
    conn.commit()
    conn.close()

# Bütün məlumatları gətir
def get_all_links():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT telegram_id, link, created_at FROM links")
    rows = cur.fetchall()
    conn.close()
    return rows

# Fayl işlədikdə avtomatik cədvəl yaratsın
if __name__ == "__main__":
    create_links_table()
    print("✅ links.db yaradıldı və links cədvəli hazırdır.")
