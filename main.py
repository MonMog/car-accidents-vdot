import os
import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

output_directory = os.path.abspath("output")
os.makedirs(output_directory, exist_ok=True)


options = webdriver.ChromeOptions()
options.add_argument("--headless") 
options.add_argument("--window-size=1320,780")
options.add_experimental_option("prefs", {
    "download.default_directory": output_directory,
    "download.prompt_for_download": False,
    "safebrowsing.enabled": True
})
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get("https://511.vdot.virginia.gov/")

    wait = WebDriverWait(driver, 15)
    traffic_tables_tab = wait.until(EC.element_to_be_clickable((By.ID, "trafficTables")))
    traffic_tables_tab.click()
    print("clicked")

    incidents_option = wait.until(EC.element_to_be_clickable((By.ID, "tblIncd")))
    incidents_option.click()
    print("2clicked")

    search_box = wait.until(EC.presence_of_element_located((By.ID, "incSearchText")))
    search_box.send_keys("incident")
    print("3clicked")

    download_button = wait.until(EC.element_to_be_clickable((By.ID, "download_incd_table_info")))
    download_button.click()
    print("4clicked")

    time.sleep(5)
    print("Slept")

    list_of_files = glob.glob(f'{output_directory}/*.csv')
    latest_file = max(list_of_files, key=os.path.getctime)
    print(f"Latest downloaded file: {latest_file}")


finally:
    driver.quit()
