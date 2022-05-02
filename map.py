import requests
from requests_html import HTMLSession
import pandas as pd


def google_lat_lon(query: str, session):

    url = "https://www.google.com/maps/search/?api=1"
    params = {}
    params["query"] = query

    r = session.get(url, params=params)

    reg = "APP_INITIALIZATION_STATE=[[[{}]"
    res = r.html.search(reg)[0]
    lat = res.split(",")[2]
    lon = res.split(",")[1]

    return lat, lon


if __name__ == "__main__":

    residents = pd.read_csv("bio.csv")
    lats = []
    lons = []

    for name, hometown in zip(residents["name"], residents["hometown"]):
        lat, lon = google_lat_lon(hometown, HTMLSession())
        lats.append(lat)
        lons.append(lon)
        print(f"Name: {name} \nHometown: {hometown} \nLatitude: {lat} \nLongitude: {lon} \n\n---")

    residents["latitude"] = lats
    residents["longitude"] = lons

    residents.to_csv("bio_map.csv")