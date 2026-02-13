import json
import time
import pandas as pd
from pytrends.request import TrendReq
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# --- Setup ---
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def get_google_trends():
    """Mission 1: Get Top 5 Trending Search Terms"""
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        df = pytrends.trending_searches(pn='united_states')
        return df[0].head(5).tolist()
    except:
        return ["Shopping Deals", "New Gadgets"]

def get_aliexpress():
    """Mission 2: Get AliExpress Trending Items"""
    driver.get("https://www.aliexpress.com")
    time.sleep(5)
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

def get_cj_dropshipping():
    """Mission 3: Get CJdropshipping Hot Sellers"""
    driver.get("https://cjdropshipping.com")
    time.sleep(5)
    # CJ uses different tags; we look for product titles
    items = driver.find_elements(By.CLASS_NAME, 'product-name')[:5]
    results = []
    for item in items:
        results.append({
            "name": item.text,
            "source": "CJdropshipping"
        })
    return results

# --- Run & Merge ---
final_data = {
    "last_updated": time.ctime(),
    "search_trends": get_google_trends(),
    "products": get_aliexpress() + get_cj_dropshipping()
}

with open("trending.json", "w") as f:
    json.dump(final_data, f, indent=4)

driver.quit()
