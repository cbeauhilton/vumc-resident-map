import os
import requests
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

    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    d = {}
    d["category"] = []
    d["name"] = []
    d["hometown"] = []
    d["college"] = []
    d["medical-school"] = []
    d["career-plans"] = []
    d["bio"] = []
    d["img"] = []


    for row in rows:

        id = row.attrs['data-history-node-id']
        id_node = {"data-history-node-id": f"{id}"}
        cat_l = []
        for sib in soup.find("div",id_node).previous_siblings:
            s  = str(sib).strip()
            if s:
                try:
                    h = BeautifulSoup(s, "html.parser")
                    cat_l.append(h.a['name'])
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
            d["hometown"].append(row.find("div.field--name-field-hometown")[0].text.split("\n")[-1])
        except:
            d["hometown"].append("missing")

        try:
            d["college"].append(row.find("div.field--name-field-resident-college")[0].text.split("\n")[-1])
        except:
            d["college"].append("missing")

        try:
            d["medical-school"].append(row.find("div.field--name-field-education-1")[0].text)
        except:
            d["medical-school"].append("missing")

        try:
            d["career-plans"].append(row.find("div.field--name-field-career-plans")[0].text.split("\n")[-1])
        except:
            d["career-plans"].append("missing")

        try:
            d["bio"].append(row.find("div.field--name-field-brief-description")[0].text.split("\n")[-1])
        except:
            d["bio"].append("missing")

        try:
            img = row.find("div.field--name-field-barista-photo")[0].find('img')[0].attrs['src']
            # print(img.attrs['src'])
            d["img"].append(f"https://medicine.vumc.org{img}")
        except:
            d["img"].append("missing")
    return d

url = "https://medicine.vumc.org/people/current-internal-medicine-housestaff"

d = get_one_page(url)

df = pd.DataFrame(d)
print(df)

csv_file = "data/00_folks.csv"
df.to_csv(csv_file)
