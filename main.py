from teams_alert import send_alert
from zip_files import extract_and_delete
from upload_to_blob import upload_to_blob
import re
import time
import os
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common


# this function attempts to clear any popups that happen upon page load
def clear_popup():
    try:
        driver.find_element(By.ID, "btnid").click()
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
chrome_options.add_argument("--headless")
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = r"C:\filepath\chrome.exe"

chrome_prefs = {"download.default_directory": r"C:\filepath"}
chrome_options.experimental_options["prefs"] = chrome_prefs

driver = webdriver.Chrome(service=serv, options=chrome_options)
driver.implicitly_wait(60)
driver.set_page_load_timeout(600)

# open the site and log in, attempts to clear any popups
driver.get("https://www.website.com")
driver.maximize_window()
clear_popup()

search = driver.find_element(By.ID, "USERNAME FIELD")
search.send_keys("username")

search = driver.find_element(By.ID, "PASSWORD FIELD")
search.send_keys("password")

search.send_keys(Keys.RETURN)
time.sleep(5)

# gets the selection values from the drop-down and add the text to a list, removes "please select"
dropdown = driver.find_element(By.NAME, "elementname")
dropdown_list_items = dropdown.text.splitlines()
dropdown_list_items.pop(0)

print(dropdown_list_items)
print(str(len(dropdown_list_items)) + " items in dropdown")

send_alert("Website login successful", "Logged into site and obtained list items")

i = 0
current_program = ""


# selects values from dropdown, toggle radio button, searches query and toggles export
for program in dropdown_list_items:
    try:
        dropdown = Select(driver.find_element(By.NAME, "elementname"))
        dropdown.select_by_visible_text(dropdown_list_items[i])

        current_program = dropdown_list_items[i]
        print(f"selected value {dropdown_list_items[i]} from dropdown")

        radial = driver.find_element(By.NAME, "elementname")
        radial.click()

        open_query = driver.find_element(By.ID, "elementid")
        open_query.click()

        time.sleep(10)

        # scrolls to bottom of page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        export_query = driver.find_element(By.ID, "btnid")
        export_query.click()

        time.sleep(10)

        link = driver.find_element(By.XPATH, '//*[@xpath]')
        link.click()

        time.sleep(5)

        # Additional wait time required for these programs because of poor site and VM performance

        if current_program == "first program":
            time.sleep(30)
        if current_program == "second program":
            time.sleep(30)

        # removes special character from dropdown list value
        new_file_name = re.sub(r":", "", dropdown_list_items[i])

        # unzips the downloaded content, renames csv file and deletes the zip file
        extract_and_delete(new_file_name)

        if current_program == "first program":
            time.sleep(60)
        if current_program == "second program":
            time.sleep(60)

        # upload to blob storage
        upload_to_blob(new_file_name)

        # delete file from download folder
        os.remove(rf"C:\filepath\{new_file_name}.csv")

        i += 1

    except selenium.common.NoSuchElementException as no_element:
        send_alert(f"Error when processing {current_program}", f"{no_element}\n moving to next program.")
        link = driver.find_element(By.LINK_TEXT, "link text")
        link.click()
        time.sleep(5)
        i += 1
        continue

    except FileNotFoundError as not_found:
        send_alert(f"File Not Found error for {current_program}",
                   "Check if the program downloads from the site (the website gives an error)"
                   " or if issue with file extraction/name - moving to next program.")
        link = driver.find_element(By.LINK_TEXT, "link text")
        link.click()
        time.sleep(5)
        i += 1
        continue

    except:
        tb = traceback.format_exc()
        send_alert(f"An unexpected error has occurred when processing program {current_program}. "
                   f"Terminating process.",
                   f"{tb}")
        break

# outside of for loop - sends message to teams and quits chrome driver
send_alert("Process has completed.", "Please review any errors.")
driver.quit()
