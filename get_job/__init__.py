#!/bin/python3
import sys
import json
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


class JobAdd():
    add_url     = ""
    company_url = ""
    company     = ""
    add_heading = ""
    add_content = ""

    """
    Distill object into a dictionary and return it
    """
    def get_dict(self):
        dict = {
                "add_url"    : self.add_url,
                "company_url": self.company_url,
                "company"    : self.company,
                "add_heading": self.add_heading,
                "add_content": self.add_content
                }
        return dict


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
    driver.find_element_by_xpath("//div[contains(@class,'show-on-load')]" +
                                 "//button[@class='close']").click()

adds = driver.find_elements_by_xpath("//div[@class='PaidJob']")

for add in adds:
    # Create job object
    job = JobAdd()

    html = add.get_attribute('innerHTML')
    soup = BeautifulSoup(html, 'html.parser')

    # Extract add details
    links = soup.find_all("a")
    job.company_url = links[0].get('href')
    job.add_url     = links[1].get('href')
    job.company     = links[2].string
    job.add_heading = links[1].string

    # Extract job add content
    content = ""
    for text in soup.find_all('p'):
        content = content + text.get_text().strip() + '\n'
    job.add_content = content

    # Write to file
    with open("data.json", "a") as write_file:
        json.dump(job.get_dict(), write_file, indent=4, separators=(',', ': '))
