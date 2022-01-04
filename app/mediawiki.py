# no-stall-GICS — Christopher Liu, Ivan Mijacika, Shyne Choi, Gavin McGinley
# SoftDev
# P01 — no-stock-GICS
# 2022-01-04

"""
MediaWiki
"""

import json
import re
import urllib.parse

import requests


def get_summary(company_name: str) -> str:
    """Uses the MediaWiki API to retrieve a wiki summary based on the given
    company name"""

    api_request = requests.get(
        f"https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&titles={urllib.parse.quote(company_name)}&redirects=true"
    )
    try:
        wiki = api_request.json()
        id = list(wiki["query"]["pages"])[0]

        if "extract" not in wiki["query"]["pages"][id]:
            return "No description available."

        summary = wiki["query"]["pages"][id]["extract"]
        # Removes the HTML tags from the summary raw text and returns the cleaned version
        clean = re.compile("<.*?>")
        summary_clean = re.sub(clean, "", summary)
        # At the end returns the first 500 characters of the full wiki
        if len(summary_clean) > 500:
            return summary_clean[:500] + "..."
        return {
            "summary": summary_clean,
            "id": wiki["query"]["pages"][id]["pageid"],
        }

    except json.decoder.JSONDecodeError:
        return None
