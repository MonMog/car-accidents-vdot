import os
import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

output_directory = "output"
renamed_file = os.path.join(output_directory, "data.csv")

os.makedirs(output_directory, exist_ok=True)

for file in glob.glob(os.path.join(output_directory, "*.csv")):
    if file.endswith(".csv"):
        os.remove(file)

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1320,780")
options.add_experimental_option("prefs", {
    "download.default_directory": output_directory,
    "download.prompt_for_download": False,
    "safebrowsing.enabled": True
})
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get("https://511.vdot.virginia.gov/")

    wait = WebDriverWait(driver, 10)
    traffic_tables_tab = wait.until(EC.element_to_be_clickable((By.ID, "trafficTables")))
    traffic_tables_tab.click()

    incidents_option = wait.until(EC.element_to_be_clickable((By.ID, "tblIncd")))
    incidents_option.click()

    search_box = wait.until(EC.presence_of_element_located((By.ID, "incSearchText")))
    search_box.send_keys("incident")

    download_button = wait.until(EC.element_to_be_clickable((By.ID, "download_incd_table_info")))
    download_button.click()

    time.sleep(15)

    downloaded_files = glob.glob(os.path.join(output_directory, "*.csv"))
    if downloaded_files:
        os.rename(downloaded_files[0], renamed_file)
        print(f"::set-output name=csv_file::{renamed_file}")

finally:
    driver.quit()
