# no-stall-GICS — Christopher Liu, Ivan Mijacika, Shyne Choi, Gavin McGinley
# SoftDev
# P01 — no-stock-GICS
# 2022-01-04

import requests, json

from flask import Flask, render_template, redirect, session, url_for, request

with open("api_keys/yahoofinance.txt", "r", encoding="utf-8") as key:
    YFA_KEY = key.read().strip()

url = "https://yfapi.net/v6/finance/autocomplete"

querystring = {"lang":"en","query":"apple"}

headers = {'x-api-key': YFA_KEY}

response = requests.request("GET", url, headers=headers, params=querystring)
data = json.loads(response.content)

print(response.text)
