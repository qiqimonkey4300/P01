# no-stall-GICS — Christopher Liu, Ivan Mijacika, Shyne Choi, Gavin McGinley
# SoftDev
# P01 — no-stock-GICS
# 2022-01-04

"""
MediaWiki
"""

import requests, json
import re

class MW:
    def __init__(self, cname: str):
        self.cname = cname

    def get_summary(self) -> str:
        """Uses the MediaWiki API to retrieve a wiki summary based on the given
        company name"""

        api_request = requests.get(
            #f"https://en.wikipedia.org/w/rest.php/v1/search/page?q={self.cname}"  # "&limit={NUMOFRESULTS}" is this needed?
            f"https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&titles={self.cname}&redirects=true"
        )
        try:
            wiki = api_request.json()
            #summary = wiki["pages"][0]["description"]
            id = list(wiki["query"]["pages"])[0]
            summary = wiki["query"]["pages"][id]["extract"]
            """removes the HTML tags from the summary raw text and returns the cleaned version"""
            clean = re.compile('<.*?>')
            summaryClean = re.sub(clean, '', summary)
            """at the end returns the first 400 characters of the full wiki"""
            return summaryClean[:400] + "..."

        except json.decoder.JSONDecodeError:
            return None


if __name__ == "__main__":
    apple = MW("Apple Inc.")
    print(apple.get_summary())
