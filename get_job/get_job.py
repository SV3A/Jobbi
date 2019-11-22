#!/bin/python3
import json
import scraper


# Initiate scraper
scraper = scraper.Jobindex()

# Parse
scraper.parse_adds()

# Write adds to json file
for add in scraper.adds:
    with open("data.json", "a", encoding="utf8") as write_file:
        json.dump(add.get_dict(), write_file, indent=4, separators=(',', ': '),
                  ensure_ascii=False)
