import os
import random
import time
import pickle
import warnings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from selenium.webdriver.common.by import By 
import requests

warnings.filterwarnings("ignore")
load_dotenv()

EMAIL = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")
COOKIE_FILE = r"linkedin_cookies.pkl"
MY_TELEGRAM_ID = os.getenv("MY_TELEGRAM_ID")

def create_driver():
    try:
        options = webdriver.ChromeOptions()
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        print(f"[create_driver] Xəta: {e}")
        raise

def save_cookies(driver, path=COOKIE_FILE):
    try:
        with open(path, "wb") as file:
            pickle.dump(driver.get_cookies(), file)
        print("\n✅ Cookie-lər yadda saxlanıldı.")
    except Exception as e:
        print(f"[save_cookies] Xəta: {e}")
        raise

def load_cookies(driver, path=COOKIE_FILE):
    try:
        with open(path, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                if 'expiry' in cookie:
                    del cookie['expiry']
                driver.add_cookie(cookie)
    except Exception as e:
        print(f"[load_cookies] Xəta: {e}")
        raise

def login_and_save_cookies():
    try:
        driver = create_driver()
        driver.get("https://www.linkedin.com/login")

        email_input = driver.find_element("id", "username")
        pass_input = driver.find_element("id", "password")

        email_input.send_keys(EMAIL)
        pass_input.send_keys(PASSWORD)

        pass_input.submit()

        print("\n➡ LinkedInə daxil olundu. Tam yüklənməsini gözləyirik...")
        time.sleep(10)

        save_cookies(driver)
        return driver
    except Exception as e:
        print(f"[login_and_save_cookies] Xəta: {e}")
        raise

def login_with_cookies():
    try:
        driver = create_driver()
        driver.get("https://www.linkedin.com")
        load_cookies(driver)
        driver.get("https://www.linkedin.com/feed/")
        print("\n🟢 Cookie ilə daxil olundu.")
        return driver
    except Exception as e:
        print(f"[login_with_cookies] Xəta: {e}")
        raise

# Hesab məlumatı üçün mock cavab


# Linklər üçün mock cavab

def get_account_type(telegram_id):
    url = f"{os.getenv('LINKEDIN_BACKEND_URL')}/account_type/{telegram_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error fetching account_type: {response.status_code}")
        return None

def get_all_links():
    url = f"{os.getenv('LINKEDIN_BACKEND_URL')}/all_links"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error fetching links: {response.status_code}")
        return []

def like_link(driver,link: str):
    try:
        print(f"🔗 Linkə daxil olunur: {link}")
        driver.get(link)
        time.sleep(5)

        # Like düyməsini tap və klik et
        like_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Like')]")
        is_liked = like_button.get_attribute("aria-pressed") == "true"
        if is_liked:
            print("👍 Artıq like olunub — keçilir.")
        else:
            like_button.click()
            print("✅ Like edildi!")
        time.sleep(5)
        # Sonunda cookie-ləri saxla və driver-i bağla
        
    except Exception as e:
        print(f"⚠️ Like etmə zamanı xəta: {e}")

def like_and_comment(driver, link: str):
    try:
        print(f"🔗 Linkə daxil olunur: {link}")
        driver.get(link)
        time.sleep(5)
        like_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Like')]")
        is_liked = like_button.get_attribute("aria-pressed") == "true"
        if is_liked:
            print("👍 Artıq like olunub — keçilir.")
        else:
            like_button.click()
            print("✅ Like edildi!")
        time.sleep(5)
        
        
        # Comment sahəsini tap və "interesting 👍" yaz
        comment_box = driver.find_element(By.XPATH, "//div[@aria-label='Text editor for creating content']//p")
        if os.path.exists("comments.txt"):
            with open("comments.txt", "r", encoding="utf-8") as f:
                comments = [line.strip() for line in f if line.strip()]
            emoji_comment = random.choice(comments)
        else:
            emoji_comment = "interesting 👍"
        script = f"arguments[0].innerText += '{emoji_comment}';"
        driver.execute_script(script, comment_box)
        time.sleep(1)

        # Submit düyməsini tap və kliklə
        submit_button = driver.find_element(By.XPATH, "//*[contains(@class, 'comments-comment-box__submit-button--cr') and contains(@class, 'artdeco-button') and contains(@class, 'artdeco-button--primary')]")
        submit_button.click()
        print(f"💬 Comment yazıldı: {emoji_comment}")

        time.sleep(2)

    except Exception as e:
        print(f"⚠️ Comment zamanı xəta: {e}")

def load_processed_links(path="processed_links.txt"):
    if not os.path.exists(path):
        return set()
    with open(path, "r") as f:
        return set(line.strip() for line in f.readlines())

def save_processed_link(link, path="processed_links.txt"):
    with open(path, "a") as f:
        f.write(link + "\n")

def main():
    processed_links = load_processed_links()

    try:
        if not os.path.exists(COOKIE_FILE):
            print("❌ Cookie faylı yoxdur. Login olunur...")
            driver = login_and_save_cookies()
        else:
            driver = login_with_cookies()
            links = get_all_links()
            account_info = get_account_type(MY_TELEGRAM_ID)
            account_type = account_info.get("account_type") if account_info else None
            for link in links:
                link_url = link["link"] 
                link_owner = link["telegram_id"]
                if link_url in processed_links or MY_TELEGRAM_ID == link_owner:
                    continue
                if account_type == "like" and not MY_TELEGRAM_ID==link["telegram_id"]:
                    like_link(driver,link["link"])
                elif account_type == "like_comment" and not MY_TELEGRAM_ID==link["telegram_id"]:
                    like_and_comment(driver, link["link"])
                save_processed_link(link_url)     
                time.sleep(60)

        save_cookies(driver)
        driver.quit()
    except Exception as e:
        print(f"[main] Xəta: {e}")

if __name__ == "__main__":
    main()