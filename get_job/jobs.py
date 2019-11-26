import sys
import json
import hashlib
import scraper


class JobDB:
    def __init__(self):
        self.adds = []

    def fetchJobs(self, target):
        # Initiate scraper
        if target == "jobindex":
            scr = scraper.Jobindex()
        else:
            sys.exit("Invalid scraper")

        # Parse html, copy data and write to disk
        scr.parse_adds()
        self.adds = scr.adds
        self._writeData()

    def _readData(self):
        pass

    def _writeData(self):
        """ Write adds to json file """
        for add in self.adds:
            with open("data.json", "a", encoding="utf8") as write_file:
                json.dump(add.get_dict(), write_file, indent=4,
                          separators=(',', ': '), ensure_ascii=False)


class JobAdd:
    id          = ""
    add_url     = ""
    company_url = ""
    company     = ""
    add_heading = ""
    add_content = ""

    def __init__(self, owner):
        self.add_owner = owner

    def hash(self):
        """
        Hashing function to create an unique job id
        """
        add_data = self.add_url+self.company_url+self.company + \
            self.add_heading+self.add_content
        self.id = hashlib.md5(add_data.encode()).hexdigest()

    def get_dict(self):
        """
        Distill object into a dictionary and return it
        """
        return {
                "id"         : self.id,
                "add_url"    : self.add_url,
                "company_url": self.company_url,
                "company"    : self.company,
                "add_heading": self.add_heading,
                "add_content": self.add_content,
                "add_owner"  : self.add_owner
                }
