from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import time
import json

# Setup WebDriver
options = Options()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # Uncomment if you want to run headlessly

# Replace with your local path to chromedriver
service = Service(r"C:\Users\divya\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# Step 1: Fetch the Top 10 Restaurant Links
driver.get("https://www.zomato.com/kanpur/dine-out")
time.sleep(5)

restaurant_links = []
try:
    # Locate restaurant containers
    links = driver.find_elements(By.CSS_SELECTOR, "a.sc-hqGPoI")
    restaurant_links = []

    for link in links[:11]:  # Top 10 restaurants
        href = link.get_attribute("href")
        # Add domain if href is relative
        if href.startswith("/"):
            href = "https://www.zomato.com" + href
        restaurant_links.append(href)

    print(restaurant_links)
except Exception as e:
    print(f"Error fetching restaurant links: {e}")

all_data = []

# Step 2 and 3: Extract Restaurant and Dish Details
for rest_link in restaurant_links:
    driver.get(rest_link)
    time.sleep(5)

    restaurant_data = {}

    # Extract Restaurant Details
    try:
        name_elem = driver.find_element(By.CLASS_NAME, "fwzNdh")
        restaurant_data["Name"] = name_elem.text.strip()
    except NoSuchElementException:
        restaurant_data["Name"] = None

    try:
        address_elem = driver.find_element(By.CLASS_NAME, "sc-clNaTc")
        restaurant_data["Address"] = address_elem.text.strip()
    except NoSuchElementException:
        restaurant_data["Address"] = None

    try:
        days_elem = driver.find_element(By.CSS_SELECTOR, "span.sc-bCCsHx.gGSXVi")
        hours_elem = driver.find_element(By.CSS_SELECTOR, "span.sc-buGlAa.cdXLKq")
        restaurant_data["Opening Hours"] = f"{days_elem.text.strip()}: {hours_elem.text.strip()}"
    except NoSuchElementException:
        restaurant_data["Opening Hours"] = None

    try:
        contact_elem = driver.find_element(By.CLASS_NAME, "leEVAg")
        restaurant_data["Contact Number"] = contact_elem.text.strip()
    except NoSuchElementException:
        restaurant_data["Contact Number"] = None

    try:
        rating_elem = driver.find_element(By.CLASS_NAME, "sc-1q7bklc-1")
        restaurant_data["Delivery Rating"] = rating_elem.text.strip()
    except NoSuchElementException:
        restaurant_data["Delivery Rating"] = None

    try:
        cuisines = driver.find_elements(By.CLASS_NAME, "cMFgfA")
        restaurant_data["Cuisines"] = ', '.join([c.text for c in cuisines if c.text.strip()])
    except NoSuchElementException:
        restaurant_data["Cuisines"] = None

    try:
        remarks = driver.find_elements(By.CLASS_NAME, "sc-bFADNz.inYxf")
        restaurant_data["Remarks"] = ', '.join([r.text for r in remarks if r.text.strip()])
    except NoSuchElementException:
        restaurant_data["Remarks"] = None
        
    try:
        facilities = driver.find_elements(By.CLASS_NAME, "sc-1hez2tp-0.cunMUz")
        restaurant_data["Facilities"] = ', '.join([c.text for c in facilities if c.text.strip()])
    except NoSuchElementException:
        restaurant_data["Facilities"] = None

    try:
        top_dishes = driver.find_elements(By.CLASS_NAME, "sc-bFADNz.grcEwO")
        restaurant_data["Top_dishes"] = ', '.join([c.text for c in top_dishes if c.text.strip()])
    except NoSuchElementException:
        restaurant_data["Top_dishes"] = None
    # Navigate to Order Page
    try:
        order_url = rest_link.replace("/info", "/order")
        driver.get(order_url)
        time.sleep(5)

        # Click all "Read More" buttons to reveal full descriptions
        read_more_buttons = driver.find_elements(By.CLASS_NAME, "sc-VuRhl")
        for btn in read_more_buttons:
            try:
                ActionChains(driver).move_to_element(btn).perform()
                btn.click()
                time.sleep(0.3)
            except ElementClickInterceptedException:
                continue
            except Exception:
                continue

        # Scrape dishes
        containers = driver.find_elements(By.CLASS_NAME, "sc-jhLVlY")
        dishes_data = []
        for container in containers:
            try:
                name = container.find_element(By.CLASS_NAME, "sc-cGCqpu").text.strip()
                desc = container.find_element(By.CLASS_NAME, "sc-gsxalj").text.strip()
                price = container.find_element(By.CLASS_NAME, "sc-17hyc2s-1").text.strip()
                dishes_data.append({
                    "Dish": name,
                    "Description": desc,
                    "Price": price
                })
            except Exception:
                continue

        restaurant_data["Dishes"] = dishes_data

    except Exception as e:
        print(f"Error navigating to order page: {e}")
        restaurant_data["Dishes"] = []

    all_data.append(restaurant_data)

# Step 4: Save Data in JSON Format
with open("zomato_kanpur_data.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

driver.quit()
