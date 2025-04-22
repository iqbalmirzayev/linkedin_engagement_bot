import sqlite3

# Hər ikisində
def get_connection():
    return sqlite3.connect(r"central.db")


# Telegram ID-yə əsaslanan sadə account məlumatları cədvəli
def create_account_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            telegram_id INTEGER PRIMARY KEY,
            account_type TEXT CHECK(account_type IN ('like', 'like_comment')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Yeni account əlavə et
def add_account(telegram_id: int, account_type: str):
    if account_type not in ('like', 'like_comment'):
        raise ValueError("account_type yalnız 'like' və ya 'like_comment' ola bilər.")
    
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO accounts (telegram_id, account_type) VALUES (?, ?)", (telegram_id, account_type))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Bu Telegram ID artıq mövcuddur.")
    finally:
        conn.close()

# Bütün account-ları al
def get_all_accounts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT telegram_id, account_type, created_at FROM accounts")
    rows = cur.fetchall()
    conn.close()
    return rows

# Telegram ID ilə account-u sil
def remove_account_by_telegram_id(telegram_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM accounts WHERE telegram_id = ?", (telegram_id,))
    conn.commit()
    conn.close()

# Bütün account-ları sıfırla
def reset_accounts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM accounts")
    conn.commit()
    conn.close()

# Fayl birbaşa işlədilərsə – cədvəli yaradacaq
if __name__ == "__main__":
    create_account_table()
    print("✅ bot_storage.db yaradıldı və accounts cədvəli hazırdır.")
