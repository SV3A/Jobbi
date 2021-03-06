import sys
import jobs
from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException
from contextlib import closing


class _Scraper:
    adds     = []    # List containing JobAdd objects
    url      = None  # Url to soruce
    html_obj = None  # BeautifulSoup object

    def _get_html(self):
        """
        Creates Soup object from raw html source
        """
        raw_html      = download_src(self.url)
        self.html_obj = BeautifulSoup(raw_html, 'html.parser')


class Jobindex(_Scraper):

    def __init__(self, url):
        self.url = url

        # Instantiate Soup object
        self._get_html()

        # Populate list containing the inner html of the divs with PaidJob
        # class
        self.adds_html = self.html_obj.find_all("div", class_="PaidJob")

    def parse_adds(self):
        for add in self.adds_html:
            # Create job object
            job = jobs.JobAdd("jobindex")

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

            # Calculate hash and assign it to the job object
            job.hash()

            # Append to JobAdd objects list
            self.adds.append(job)


class Jobfinder(_Scraper):
    def __init__(self, url):
        self.url = url

        # Instantiate Soup object
        self._get_html()

        # Populate list containing the inner html of the divs with PaidJob
        # class
        self.adds_html = self.html_obj.find_all("div", class_="user-jobs__" +
                                                "content-item")

    def parse_adds(self):
        for add in self.adds_html:
            # Create job object
            job = jobs.JobAdd("jobfinder")

            # Extract add details
            title = add.find("h2")
            company = add.find("div", class_=
                               "node-list__item-recruiter")
            workplace = add.find("div", class_=
                                 "node-list__item-location").contents[1]
            job.company_url = "https://www.jobfinder.dk"+company.a.get("href")
            job.add_url     = "https://www.jobfinder.dk"+title.a.get("href")
            job.company     = company.a.string
            job.add_heading = title.a.string

            # Extract job add content
            content = "Job location: " + workplace + "\n"
            content = content+add.find("div", class_=
                                       "node-list__item-description").p.string
            job.add_content = content

            # Calculate hash
            job.hash()

            # Append to JobAdd objects list
            self.adds.append(job)


def download_src(url):
    """
    Downloads raw html from given url
    """
    try:
        with closing(get(url, stream=True)) as resp:
            return resp.content
    except RequestException as e:
        sys.exit('Error during requests to {0} : {1}'.format(url, str(e)))


# Entry point for debugging purposes
if __name__ == '__main__':
    scraper = Jobfinder()
    scraper.parse_adds()
