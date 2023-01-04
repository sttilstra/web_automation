from teams_alert import send_alert
from zip_files import extract_and_delete
from bulk_upload import bulk_upload
import re
import time
import traceback
import selenium.common
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert


# this function attempts to clear any popups that happen upon page load
def clear_popup():
    try:
        driver.find_element(By.ID, "btnMessagePopupDontShow").click()
    except:
        pass
    try:
        alert = Alert(driver)
        alert.accept()
    except:
        pass
    try:
        alert = Alert(driver)
        alert.dismiss()
    except:
        pass

    return

send_alert("Process has Started", "Commencing launch of Chrome Browser")

# create web driver, set chrome options, implicit wait time and timeout values.
serv = Service(r"C:\filepath\chromedriver.exe")
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.binary_location = r"C:\Chrome Portable\GoogleChromePortable\App\Chrome-bin\chrome.exe"

driver = webdriver.Chrome(service=serv, options=chrome_options)
driver.implicitly_wait(60)
driver.set_page_load_timeout(600)

# open the ahri site and log in, attempts to clear any popups on the site
driver.get("https://www.website.com/page")
driver.maximize_window()
clear_popup()

search = driver.find_element(By.ID, "<username>")
search.send_keys("<username>")

search = driver.find_element(By.ID, "<password>")
search.send_keys("<password>")

search.send_keys(Keys.RETURN)
time.sleep(5)

# gets the selection values from the drop down and add the text to a list, removes "please select"
dropdown = driver.find_element(By.NAME, "drpProgram")
dropdown_list_items = dropdown.text.splitlines()
dropdown_list_items.pop(0)

send_alert("Website login successful", "No issues logging into site and getting list items")

i = 0
current_program = ""

# selects values from dropdown, toggle radio button, searches query and toggles export
for program in dropdown_list_items:
    try:
        dropdown = Select(driver.find_element(By.NAME, "drpProgram"))
        dropdown.select_by_visible_text(dropdown_list_items[i])

        current_program = dropdown_list_items[i]
        print(f"selected value {dropdown_list_items[i]} from dropdown")

        radial = driver.find_element(By.NAME, "QueryID")
        radial.click()

        open_query = driver.find_element(By.ID, "btnNext")
        open_query.click()
        time.sleep(7)

        # scrolls to bottom of page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        export_query = driver.find_element(By.ID, "btnSearch")
        export_query.click()
        time.sleep(10)

        link = driver.find_element(By.LINK_TEXT, "<LINK TEXT>")
        link.click()
        time.sleep(3)

        # removes special character from dropdown list value
        new_file_name = re.sub(r":", "", dropdown_list_items[i])
        # unzips the downloaded content, renames csv file and deletes the zip file
        extract_and_delete(new_file_name)

        i += 1

    except selenium.common.NoSuchElementException as no_element:
        # sends alert to teams via webhook with traceback info
        send_alert(f"Error when processing {current_program}", f"{no_element}\n moving to next program.")
        link = driver.find_element(By.LINK_TEXT, "<LINK TEXT>")
        link.click()
        time.sleep(3)
        i += 1
        continue
    except FileNotFoundError as not_found:
        send_alert(f"Zip Error for program {current_program}",
                   "unable to locate zip file - moving to next program.")
        link = driver.find_element(By.LINK_TEXT, "<LINK TEXT>")
        link.click()
        time.sleep(3)
        i += 1
        continue
    except:
        tb = traceback.format_exc()
        send_alert(f"An unexpected error has occurred when processing program {current_program}. "
                   f"Moving to next program",
                   f"{tb}")
        link = driver.find_element(By.LINK_TEXT, "<LINK TEXT>")
        link.click()
        time.sleep(3)
        i += 1
        continue

# 
# outside of for loop - quits chrome driver, uploads files to blob storage and sends messages to teams
driver.quit()

send_alert("Upload Process has begun", "Attempting to upload all files to blob storage")

bulk_upload()

send_alert("Process has completed.", "Please review any errors.")




