# no-stall-GICS -- Christopher Liu, Ivan Mijacika, Shyne Choi, Gavin McGinley
# SoftDev
# P01 -- no-stock-GICS

"""
MediaWiki
"""

import requests


def get_co_wiki(ticker: str) -> dict:
    """Uses the MediaWiki API to retrieve a wiki summary based on the given
    company name"""

    api_request = requests.get(
        f"https://en.wikipedia.org/w/rest.php/v1/search/page?q={CONAME}&limit={NUMOFRESULTS}"
    )
    # should numofresults always be 1?
    return api_request.json()


if __name__ == "__main__":
    print(get_co_wiki("Apple+Inc."))
