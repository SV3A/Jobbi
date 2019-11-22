#!/bin/python3
import sys
import json
import hashlib
from requests import get
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from contextlib import closing


class JobAdd():
    add_url     = ""
    company_url = ""
    company     = ""
    add_heading = ""
    add_content = ""

    """
    Hashing function to create an unique job id
    """
    def get_hash(self):
        add_data = self.add_url+self.company_url+self.company + \
                   self.add_heading+self.add_content
        return hashlib.md5(add_data.encode()).hexdigest()

    """
    Distill object into a dictionary and return it
    """
    def get_dict(self):
        return {
                "id"         : self.get_hash(),
                "add_url"    : self.add_url,
                "company_url": self.company_url,
                "company"    : self.company,
                "add_heading": self.add_heading,
                "add_content": self.add_content
                }


url = "https://www.jobindex.dk/jobsoegning/ingenioer/maskiningenioer/" + \
      "storkoebenhavn"

try:
    with closing(get(url, stream=True)) as resp:
        resp.content
except RequestException as e:
    sys.exit('Error during requests to {0} : {1}'.format(url, str(e)))

html = BeautifulSoup(resp.content, 'html.parser')
adds = html.find_all("div", class_="PaidJob")

for add in adds:
    # Create job object
    job = JobAdd()

    # Extract add details
    links = add.find_all("a")
    job.company_url = links[0].get('href')
    job.add_url     = links[1].get('href')
    job.company     = links[2].string
    job.add_heading = links[1].string

    # Extract job add content
    content = ""
    for text in add.find_all('p'):
        content = content + text.get_text().strip() + '\n'
    job.add_content = content

    # Write to file
    with open("data.json", "a", encoding="utf8") as write_file:
        json.dump(job.get_dict(), write_file, indent=4, separators=(',', ': '),
                  ensure_ascii=False)
