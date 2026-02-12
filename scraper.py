from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Set up the invisible browser
options = Options()
options.add_argument("--headless") # Run without a screen
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Tell it where to go (Put your AliExpress link here)
driver.get("https://www.aliexpress.com")

# Take a picture of what it sees (This proves it worked!)
print(driver.title)
driver.quit()
