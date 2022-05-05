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
    residents.drop(columns=['bio'], errors="ignore", inplace=True)
    places_df = pd.read_csv("places.csv")
    residents = residents.merge(places_df, left_on="hometown", right_on="place", how="outer")
    print(residents)
    lats = []
    lons = []
    places = []

    df = residents[residents["longitude"].isnull()]

    if len(df.index) > 0:
        for name, place in zip(df["name"], df["hometown"]):
            lat, lon = google_lat_lon(place, HTMLSession())
            lats.append(lat)
            lons.append(lon)
            places.append(place)
            print(f"Name: {name} \nHometown: {place} \nLatitude: {lat} \nLongitude: {lon} \n\n---")

        df["latitude"] = lats
        df["longitude"] = lons

        residents = pd.concat([df, residents])

        new_places = pd.DataFrame(list(zip(places, lats, lons)), columns=['place', 'latitude', 'longitude'])
        places_df = pd.concat([places_df, new_places]).drop_duplicates()
        places_df.to_csv("places.csv", index=False)

    residents = residents.drop_duplicates()
    residents.drop(columns=['place'], errors="ignore", inplace=True)
    residents["image"] = residents["image"].apply(lambda x: f"https://github.com/cbeauhilton/vumc-resident-map/raw/main/{x}")
    residents["popup"] = residents.apply(lambda x: f'{{"image": "{x["image"]}", "alt": "{x["name"]}","title": "{x["name"]}","description": "<em>Hometown</em>: {x["hometown"]}\n Undergraduate School: {x["undergrad"]}\n Medical School: {x["med_school"]}\n Career Plans: {x["career_plans"]}"}}',
                                         axis=1)
    print(residents["popup"])
    residents.to_csv("bio_map.csv", index=False)
    # print(list(residents))
    # print(residents)
    # print(residents.head(50))
