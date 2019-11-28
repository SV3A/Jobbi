import os
import sys
import json
import hashlib
import scraper


class JobDB:
    def __init__(self):
        self.dbFile = "data.json"

    def fetchData(self, src_target):
        """ Scrape source and write new data"""

        # Initiate scraper
        if src_target == "jobindex":
            scr = scraper.Jobindex()
        else:
            sys.exit("Invalid scraper")

        # Parse html
        scr.parse_adds()

        # If data exists guard for duplicate adds
        if os.path.isfile("./"+self.dbFile):
            # Get hash-ids of stored adds
            storedIDs = self._getStoredHashes()

            # Prepare loaded data to be written to disk - checking that the
            # data does not already exist
            new_data = []
            for add in scr.adds:
                if add.id not in storedIDs:
                    new_data.append(add)
        else:
            new_data = scr.adds

        if len(new_data) == 0:
            return None
        else:
            self._writeData(new_data)
            return new_data

    def readData(self):
        """ Read adds from json file """

        if not os.path.isfile("./"+self.dbFile):
            return None

        adds = []
        with open(self.dbFile) as json_file:

            data = json.load(json_file)

            for add in data:
                job = JobAdd(add["add_owner"])

                job.id          = add["id"]
                job.add_url     = add["add_url"]
                job.company_url = add["company_url"]
                job.company     = add["company"]
                job.add_heading = add["add_heading"]
                job.add_content = add["add_content"]

                adds.append(job)
        return adds

    def _writeData(self, new_data):
        """ Write loaded adds to json file """

        data = [add.get_dict() for add in new_data]

        # If data exist on disk prepend and concatenate
        if os.path.isfile("./"+self.dbFile):

            with open(self.dbFile) as json_file:
                old_data = json.load(json_file)

            data = data+old_data

        # Write data to json file
        with open(self.dbFile, "w", encoding="utf8") as write_file:
            json.dump(data, write_file, indent=4,
                      separators=(',', ': '), ensure_ascii=False)

    def _getStoredHashes(self):
        """ Load ids from all of the stores adds """
        ids = []

        with open(self.dbFile) as json_file:

            for add in json.load(json_file):
                ids.append(add["id"])

        return ids


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
