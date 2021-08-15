from requests_html import HTMLSession
from pathlib import Path
import pandas as pd
import os

df = pd.read_csv("data/00_folks.csv", index_col=0)
# print(list(df))
cols = [
    "category",
    "img",
    "name",
    "hometown",
    "college",
    "medical-school",
    "career-plans",
    "bio",
]
df = df[cols]

d = {}
d["name"] = df["name"]
d["hometown"] = df["hometown"]
d["longitude"] = []
d["latitude"] = []

session = HTMLSession()

url = "https://www.google.com/maps/search/?api=1"

params = {
    "query": None,
}

for name, hometown in zip(d["name"], d["hometown"]):
    params["query"] = hometown
    r = session.get(url, params=params)
    reg = "APP_INITIALIZATION_STATE=[[[{}]"
    res = r.html.search(reg)[0]
    lon = res.split(",")[1]
    lat = res.split(",")[2]
    d["longitude"].append(lon)
    d["latitude"].append(lat)
    # print(name)
    # print(hometown)
    # print(lon)
    # print(lat)
    # print("\n")


df["longitude"] = d["longitude"]
df["latitude"] = d["latitude"]

print(df.head())

csv_file = "data/01_folks_and_map.csv"
df.to_csv(csv_file, index=False)

db_file_name = "data/residents.db"
db_file = Path(db_file_name)
db_file.unlink(missing_ok=True)
os.system(f"sqlite-utils insert {db_file_name} residents {csv_file} --csv")
