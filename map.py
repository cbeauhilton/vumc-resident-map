import os
from pathlib import Path
from random import randint
from time import sleep

import requests
from requests_html import HTMLSession


def google_lat_lon(query: str):

    url = "https://www.google.com/maps/search/?api=1"
    params = {}
    params["query"] = query

    r = session.get(url, params=params)

    reg = "APP_INITIALIZATION_STATE=[[[{}]"
    res = r.html.search(reg)[0]
    lat = res.split(",")[2]
    lon = res.split(",")[1]

    return lat, lon


def commit_lat_lon(
    api: str, index: int, lat_col: str, lon_col: str, lat: float, lon: float
):

    url = f"{api}{index+1}"
    patch_response = requests.patch(url, json={lat_col: lat, lon_col: lon})

    return patch_response


if __name__ == "__main__":

    session = HTMLSession()

    api = "http://127.0.0.1:8000/residents/"
    response = requests.get(api).json()
    print("N:", len(response))
    response = [r for r in response if r["hometownlatitude"] == None]
    print("N remaining:", len(response))

    for i, resident in enumerate(response):

        query = resident["hometown"]
        lat, lon = google_lat_lon(query)

        lat_col = "hometownlatitude"
        lon_col = "hometownlongitude"

        print(f"{i+1}/{len(response)} |", query, f"| lat: {lat}", f"lon: {lon}")

        patch_response = commit_lat_lon(api, i, lat_col, lon_col, lat, lon)

        sleep(randint(5, 15))
