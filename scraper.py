import json
import time
import os
import pandas as pd
from pytrends.request import TrendReq
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# --- 1. THE SAFETY NET ---
# This creates a placeholder so the Robot (GitHub Action) doesn't crash 
# if the websites are being mean and blocking us today.
def create_safety_file():
    if not os.path.exists("trending.json"):
        with open("trending.json", "w") as f:
            json.dump({"status": "starting", "last_updated": time.ctime()}, f)

create_safety_file()

# --- Setup ---
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def get_google_trends():
    """Mission 1: Get Top 5 Trending Search Terms"""
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        df = pytrends.trending_searches(pn='united_states')
        # Fix for pytrends dataframe structure
        return df[0].head(5).tolist()
    except Exception as e:
        print(f"Google Trends error: {e}")
        return ["Shopping Deals", "New Gadgets"]

def get_aliexpress():
    """Mission 2: Get AliExpress Trending Items"""
    try:
        driver.get("https://www.aliexpress.com")
        time.sleep(7) # Extra sleep for slow loading
        items = driver.find_elements(By.CSS_SELECTOR, 'div[class*="item--container"]')[:5]
        results = []
        for item in items:
            try:
                results.append({
                    "name": item.find_element(By.CSS_SELECTOR, 'h3').text,
                    "price": item.find_element(By.CSS_SELECTOR, 'div[class*="price--current"]').text,
                    "source": "AliExpress"
                })
            except: continue
        return results
    except: return []

def get_cj_dropshipping():
    """Mission 3: Get CJdropshipping Hot Sellers"""
    try:
        driver.get("https://cjdropshipping.com")
        time.sleep(7)
        items = driver.find_elements(By.CLASS_NAME, 'product-name')[:5]
        results = []
        for item in items:
            results.append({
                "name": item.text,
                "source": "CJdropshipping"
            })
        return results
    except: return []

# --- Run & Merge ---
try:
    final_data = {
        "last_updated": time.ctime(),
        "search_trends": get_google_trends(),
        "products": get_aliexpress() + get_cj_dropshipping()
    }

    # --- THE FINAL SAVE ---
    with open("trending.json", "w") as f:
        json.dump(final_data, f, indent=4)
    print("Success! trending.json has been written.")

except Exception as e:
    print(f"Main Loop Error: {e}")

finally:
    driver.quit()
