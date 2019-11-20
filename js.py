#!/bin/python3
import sys
from bs4 import BeautifulSoup
"""
Selenium imports
webdriver       : used for launcing the browser
By              : search using the By parameter
WebDriverWait   : wait for page load
EC              : specify what to look for
TimeoutException: handle timeout
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

url = "https://www.jobindex.dk/jobsoegning/ingenioer/maskiningenioer/" + \
      "storkoebenhavn"

# Setup webdriver
option = webdriver.ChromeOptions()
option.add_argument(" — incognito")
driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver',
                          chrome_options=option)

# Open page
driver.get(url)

# Wait for page to load
timeout = 10
try:
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(
        (By.XPATH, "//div[@class='PaidJob']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    driver.quit()

print("Finished loading")

# Check if modal appears and close it
if driver.find_element_by_class_name('show-on-load'):
    print("shadow")
    driver.find_element_by_xpath("//div[contains(@class,'show-on-load')]" +
                                 "//button[@class='close']").click()

jobs = driver.find_elements_by_xpath("//div[@class='PaidJob']")

for job in jobs:
    html = job.get_attribute('innerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())
    sys.exit()
