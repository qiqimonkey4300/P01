# no-stall-GICS — Christopher Liu, Ivan Mijacika, Shyne Choi, Gavin McGinley
# SoftDev
# P01 — no-stock-GICS
# 2022-01-04

"""
MediaWiki
"""

import requests, json

class MW:

    def __init__(self, cname: str):
        self.cname = cname

    #def filter()

    def get_summary(self) -> str:
        """Uses the MediaWiki API to retrieve a wiki summary based on the given
        company name""" #or ticker?

        api_request = requests.get(
            f"https://en.wikipedia.org/w/rest.php/v1/search/page?q={self.cname}" #"&limit={NUMOFRESULTS}" is this needed?
        )
        try:
            wiki = api_request.json()
            summary = wiki['pages'][0]['excerpt'] #needs work, "amazon"'s first result is the people/rainforest
            return summary

        #return filter(summary)
        except json.decoder.JSONDecodeError:
            return None


if __name__ == "__main__":
    apple = MW("Apple Inc.")
    print(apple.get_summary())
