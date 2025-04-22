# LinkedIn Engagement Automation Bot

This system automates engagement (likes and comments) on LinkedIn posts shared in Telegram groups. Predefined bot accounts perform these actions based on their role, and the entire process is managed via an admin panel.

---

## 📌 Components

### 1. **Telegram Admin Bot (Aiogram)**
- `/add_like_account` – adds an account that only likes
- `/add_like_comment_account` – adds an account that likes and comments
- `/remove_account` – removes an account
- `/list_accounts` – shows all added accounts

🔒 Only admin Telegram IDs can execute these commands.

---

### 2. **Link Collector Bot**
- Monitors a specific thread in a Telegram group.
- Automatically detects and stores LinkedIn post links in the SQLite database.

---

### 3. **FastAPI Backend**
- `/account_type/{telegram_id}` → returns the account type (like / like_comment)
- `/all_links` → returns all stored links
- `/all_accounts` → returns list of accounts via API

---

### 4. **Local LinkedIn Automation Bot (`scraper.py`)**
- Logs into LinkedIn using Selenium (via login or cookie)
- Fetches links and account type from the backend
- If `like` → likes the post
- If `like_comment` → likes and comments (from `comments.txt`)
- Skips the user's own posts
- Uses `processed_links.txt` to avoid duplicate actions




## ⚠️ Disclaimer

This project is intended for educational and personal use only. Please ensure you comply with LinkedIn's terms of service and avoid unauthorized automation.
