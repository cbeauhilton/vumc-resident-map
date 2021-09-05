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

    url = f"{api}{index}"
    patch_response = requests.patch(url, json={lat_col: lat, lon_col: lon})

    return patch_response


if __name__ == "__main__":

    from datetime import datetime
    from random import randint
    from time import sleep

    start = datetime.now()
    session = HTMLSession()

    api = "http://127.0.0.1:9000/residents/"
    response = requests.get(api).json()
    lenlen = len(f"{len(response)}")
    print(f"N:", len(response))
    response = [r for r in response if r["hometownlatitude"] == None]
    print("N remaining:", len(response), "\n")

    if not response:
        exit()

    for i, resident in enumerate(response):

        res_id = resident["id"]
        query = resident["hometown"]
        lat, lon = google_lat_lon(query)

        lat_col = "hometownlatitude"
        lon_col = "hometownlongitude"

        print(
            f"{i+1:0{lenlen}d}/{len(response):0{lenlen}d}",
            "|",
            resident["name"],
            "|",
            query,
            f"lat: {lat}",
            f"lon: {lon}",
        )

        patch_response = commit_lat_lon(api, res_id, lat_col, lon_col, lat, lon)

        # github allows up to 6h of execution time, we'll do 4h to be safe

        now = datetime.now()
        rundiff = now - start
        runtime = rundiff.total_seconds()
        print(f"\n Runtime: {runtime} seconds \n")

        allowed_time = 60 * 60 * 4
        if runtime > allowed_time:
            exit()

        sleep(randint(5, 15))
