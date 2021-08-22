import os
import requests
import json
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd

session = HTMLSession(
    browser_args=[
        "--no-sandbox",
        "--user-agent=Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",  # noqa
    ]
)


def get_one_page(url: str):

    r = session.get(url)
    r.html.render(reload=False)
    rows = r.html.find("div.node--type-person")

    soup = BeautifulSoup(requests.get(url).text, "html.parser")

    d = {}
    d["category"] = []
    d["name"] = []
    d["hometown"] = []
    d["college"] = []
    d["medical-school"] = []
    d["career-plans"] = []
    d["bio"] = []
    d["img"] = []
    d["popup"] = []

    for row in rows:

        id = row.attrs["data-history-node-id"]
        id_node = {"data-history-node-id": f"{id}"}
        cat_l = []
        for sib in soup.find("div", id_node).previous_siblings:
            s = str(sib).strip()
            if s:
                try:
                    h = BeautifulSoup(s, "html.parser")
                    cat_l.append(h.a["name"])
                except:
                    pass
        try:
            category = "".join(cat_l).strip()
            d["category"].append(category)
        except:
            d["category"].append("missing")

        try:
            d["name"].append(row.find("div.field--name-node-title")[0].text)
        except:
            d["name"].append("missing")

        try:
            d["hometown"].append(
                row.find("div.field--name-field-hometown")[0].text.split("\n")[-1]
            )
        except:
            d["hometown"].append("missing")

        try:
            d["college"].append(
                row.find("div.field--name-field-resident-college")[0].text.split("\n")[
                    -1
                ]
            )
        except:
            d["college"].append("missing")

        try:
            d["medical-school"].append(
                row.find("div.field--name-field-education-1")[0].text
            )
        except:
            d["medical-school"].append("missing")

        try:
            d["career-plans"].append(
                row.find("div.field--name-field-career-plans")[0].text.split("\n")[-1]
            )
        except:
            d["career-plans"].append("missing")

        try:
            bio = row.find("div.field--name-field-brief-description")[0].text.split(
                "\n"
            )[-1]
            d["bio"].append(bio)
        except:
            d["bio"].append("missing")

        try:
            root_url = "https://medicine.vumc.org"
            try:
                src = (
                    root_url
                    + row.find("div.field--name-field-barista-photo")[0]
                    .find("img")[0]
                    .attrs["src"]
                )
            except:
                src = ""
            try:
                href = (
                    root_url
                    + row.find("div.field--name-field-barista-photo")[0]
                    .find("a")[0]
                    .attrs["href"]
                )
            except:
                href = ""
            try:
                alt = (
                    row.find("div.field--name-field-barista-photo")[0]
                    .find("img")[0]
                    .attrs["alt"]
                )
            except:
                alt = ""

            img_dict = {
                "img_src": f"{src}",
                "href": f"{href}",
                "alt": f"{alt}",
                "width": 100,
            }
            img_json = json.dumps(img_dict)
            d["img"].append(img_json)

            popup_dict = {
                "image": src,
                "alt": alt,
                "title": alt,
                "description": bio,
                "link": href,
            }

            popup_json = json.dumps(popup_dict)
            d["popup"].append(popup_json)

        except:
            d["img"].append("missing")

    return d


url = "https://medicine.vumc.org/people/current-internal-medicine-housestaff"

d = get_one_page(url)

df = pd.DataFrame(d)
print(df.head())

csv_file = "data/00_folks.csv"
df.to_csv(csv_file)
