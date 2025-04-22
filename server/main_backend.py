from fastapi import FastAPI, HTTPException
from database import get_db_connection

app = FastAPI()

# 🔹 1. Telegram ID-yə görə account_type qaytarır
@app.get("/account_type/{telegram_id}")
def get_account_type(telegram_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    row = cursor.execute(
        "SELECT account_type FROM accounts WHERE telegram_id = ?", (telegram_id,)
    ).fetchone()

    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Telegram ID not found")

    return {"telegram_id": telegram_id, "account_type": row[0]}


# 🔹 2. links cədvəlindən bütün məlumatları qaytarır (telegram_id + link)
@app.get("/all_links")
def get_all_links():
    conn = get_db_connection()
    cursor = conn.cursor()

    rows = cursor.execute("SELECT telegram_id, link FROM links").fetchall()
    conn.close()

    # Nəticəni dictionary listi şəklində qaytarırıq
    return [{"telegram_id": row[0], "link": row[1]} for row in rows]
app.get("/all_accounts")
def get_all_accounts():
    conn = get_db_connection()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM accounts").fetchall()
    conn.close()
    return [dict(row) for row in rows]
