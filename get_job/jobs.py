import os
import sys
import json
import hashlib
import scraper


class JobDB:
    def __init__(self):
        # List containing JobAdd objects
        self.adds = []

        self.dbFile = "data.json"

    def fetchData(self, target):
        # Initiate scraper
        if target == "jobindex":
            scr = scraper.Jobindex()
        else:
            sys.exit("Invalid scraper")

        # Parse html, copy data and write to disk
        scr.parse_adds()
        self.adds = scr.adds
        self.writeData()

    def readData(self):
        """ Read adds from json file """

        loadedIDs = self._getLoadedHashes()

        with open(self.dbFile) as json_file:

            data = json.load(json_file)
            for add in data:

                if add["id"] not in loadedIDs:
                    job = JobAdd(add["add_owner"])

                    job.id          = add["id"]
                    job.add_url     = add["add_url"]
                    job.company_url = add["company_url"]
                    job.company     = add["company"]
                    job.add_heading = add["add_heading"]
                    job.add_content = add["add_content"]

                    self.adds.append(job)

    def writeData(self):
        """ Write loaded adds to json file """

        # If data exist on disk guard for duplicates
        if os.path.isfile("./"+self.dbFile):
            # Get hash-ids of stored adds
            storedIDs = self._getStoredHashes()

            # Prepare loaded data (in self.adds) to be written to disk - check-
            # ing that the data don't already exist
            newdata = []
            for add in self.adds:
                if add.id not in storedIDs:
                    newdata.append(add.get_dict())

            # Read what is already stored and concatenate it
            olddata = []
            with open(self.dbFile) as json_file:
                olddata = json.load(json_file)
            data = olddata+newdata
        else:
            data = [add.get_dict() for add in self.adds]

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

    def _getLoadedHashes(self):
        """ Get ids from all of the currently-loaded adds """
        ids = []

        for add in self.adds:
            ids.append(add.id)

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
