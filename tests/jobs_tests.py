import os
import sys
import json
import unittest
sys.path.append("../get_job/")
import jobs


class TestDB(unittest.TestCase):
    def setUp(self):
        self.job_db = jobs.JobDB()
        self.job_db.dbFile = "data_test.json"

    def test_readData(self):
        """ Test loading data """
        self.job_db.readData()

        self.assertEqual(self.job_db.adds[0].id,
                         "39f99f99f6e69e98b1f6de0815a262b9")

    def test_readData2(self):
        """ Test only loading new data """
        self.job_db.readData()
        self.job_db.readData()

        self.assertEqual(len(self.job_db.adds), 3, "adds list should be 3")

    def test_writeData(self):
        """ Test writing a new db file """

        self.job_db.readData()
        self.job_db.dbFile = "data_testingwrite.json"
        self.job_db.writeData()

        f1 = open("data_test.json")
        f2 = open(self.job_db.dbFile)

        self.assertListEqual(list(f1), list(f2), "Files should be equal")

        # Cleanup
        f1.close()
        f2.close()

        os.remove("./"+self.job_db.dbFile)

    def test_writeData2(self):
        """ Test writing to existing db file """
        from shutil import copyfile

        test_hashes = []
        output_file = "data_testingwrite.json"

        # Load data
        self.job_db.readData()

        # Store old hashes for later use
        for add in self.job_db.adds:
            test_hashes.append(add.id)

        # Make loaded data unique by chaning the one prop and rehashing
        for add in self.job_db.adds:
            add.company = "change"
            add.hash()
            test_hashes.append(add.id)

        # Copy dbfile
        copyfile(self.job_db.dbFile, output_file)
        self.job_db.dbFile = output_file

        self.job_db.writeData()

        with open(self.job_db.dbFile) as json_file:
            data = json.load(json_file)

        self.assertEqual(len(data), 6, "Should be 6")

        # Load hashes from file and check with the ones previously stored
        new_hashes = []

        for add in data:
            new_hashes.append(add["id"])

        self.assertListEqual(test_hashes, new_hashes, "Hashes should be equal")

        os.remove("./"+self.job_db.dbFile)

    def test_getLoadedHashes(self):
        self.job_db.readData()
        hashes = self.job_db._getLoadedHashes()
        expected_hashes = ["39f99f99f6e69e98b1f6de0815a262b9",
                           "cc69355f68edfda7d962d80dc179c441",
                           "c0cf364c725d24b1bf97aa46bdf9467c"]
        self.assertEqual(hashes, expected_hashes)

    def test_getStoredHashes(self):
        hashes = self.job_db._getStoredHashes()
        expected_hashes = ["39f99f99f6e69e98b1f6de0815a262b9",
                           "cc69355f68edfda7d962d80dc179c441",
                           "c0cf364c725d24b1bf97aa46bdf9467c"]
        self.assertEqual(hashes, expected_hashes)


if __name__ == '__main__':
    unittest.main()
