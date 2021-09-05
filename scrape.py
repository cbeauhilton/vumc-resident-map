import json
import os
import sqlite3 as sql

import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession


def get_one_page(url: str):

    r = session.get(url)
    r.html.render(reload=False)
    rows = r.html.find("div.node--type-person")

    soup = BeautifulSoup(requests.get(url).text, "html.parser")

    return soup, rows


def get_category(row, soup):
    category = ""
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
    if cat_l:
        category = "".join(cat_l).strip()

    return category


def get_name(row):
    name = row.find("div.field--name-node-title")[0].text.strip()
    return name


def get_hometown(row):
    hometown = (
        row.find("div.field--name-field-hometown")[0].text.split("\n")[-1].strip()
    )
    return hometown


def get_college(row):  # [-1]
    *_, college = row.find("div.field--name-field-resident-college")[0].text.split("\n")
    return college


def get_med_school(row):
    *_, med_school = row.find("div.field--name-field-education-1")[0].text.split("\n")
    return med_school


def get_career_plans(row):
    *_, career_plans = row.find("div.field--name-field-career-plans")[0].text.split(
        "\n"
    )
    # [-1]
    return career_plans


def get_bio(row):
    *_, bio = row.find("div.field--name-field-brief-description")[0].text.split("\n")
    # [-1]
    return bio


def get_img_popup(row, bio):
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

    popup_dict = {
        "image": src,
        "alt": alt,
        "title": alt,
        "description": bio,
        "link": href,
    }

    popup_json = json.dumps(popup_dict)

    return img_json, popup_json


if __name__ == "__main__":
    session = HTMLSession(
        browser_args=[
            "--no-sandbox",
            "--user-agent=Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",  # noqa
        ]
    )

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

    url = "https://medicine.vumc.org/people/current-internal-medicine-housestaff"
    soup, rows = get_one_page(url)

    for row in rows:
        try:
            d["category"].append(get_category(row=row, soup=soup))
        except:
            d["category"].append("")

        try:
            d["name"].append(get_name(row))
        except:
            d["name"].append("")

        try:
            d["hometown"].append(get_hometown(row))
        except:
            d["hometown"].append("")

        try:
            d["college"].append(get_college(row))
        except:
            d["college"].append("")

        try:
            d["medical-school"].append(get_med_school(row))
        except:
            d["medical-school"].append("")

        try:
            d["career-plans"].append(get_career_plans(row))
        except:
            d["career-plans"].append("")

        try:
            bio = get_bio(row)
            img_json, popup_json = get_img_popup(row=row, bio=bio)
            d["bio"].append(get_bio(row))
            d["img"].append(img_json)
            d["popup"].append(popup_json)
        except:
            d["img"].append("")
            d["popup"].append("")
            d["bio"].append("")

    df = pd.DataFrame(d)
    print(df.head())

    csv_file = "data/00_folks.csv"
    df.to_csv(csv_file)

# ---

# db_path = "data/test.db"
# create_sql_db(db_path)

# def create_connection(db_file):
#     """ create a database connection to the SQLite database
#         specified by db_file
#     :param db_file: database file
#     :return: Connection object or None
#     """
#     conn = None
#     try:
#         conn = sql.connect(db_file)
#     except Error as e:
#         print(e)
#
# return conn

# def create_sql_db(db_path):
#
#     conn = sql.connect(db_path)
#     cur = conn.cursor()
#
#     cur.execute(
#         """
#         CREATE TABLE residents(
#         name TEXT PRIMARY KEY,
#         category TEXT,
#         hometown TEXT,
#         college TEXT,
#         medical-school TEXT,
#         career-plans TEXT,
#         bio TEXT,
#         img TEXT,
#         popup TEXT,
#         )
#         """
#     )
#
#     conn.commit()
#
#
# def insert_into_db():
#     pass

# id = row.attrs["data-history-node-id"]
# id_node = {"data-history-node-id": f"{id}"}
# cat_l = []
# for sib in soup.find("div", id_node).previous_siblings:
#     s = str(sib).strip()
#     if s:
#         try:
#             h = BeautifulSoup(s, "html.parser")
#             cat_l.append(h.a["name"])
#         except:
#             pass
# try:
#     category = "".join(cat_l).strip()
#     d["category"].append(category)
# except:
#     d["category"].append("missing")

# try:
#     name = row.find("div.field--name-node-title")[0].text.strip()
#     d["name"].append(name)
# except:
#     d["name"].append("missing")

# try:
#     d["hometown"].append(
#         row.find("div.field--name-field-hometown")[0]
#         .text.split("\n")[-1]
#         .strip()
#     )
# except:
#     d["hometown"].append("missing")

# try:
#     d["college"].append(
#         row.find("div.field--name-field-resident-college")[0].text.split("\n")[
#             -1
#         ]
#     )
# except:
#     d["college"].append("missing")

# try:
#     d["medical-school"].append(
#         row.find("div.field--name-field-education-1")[0].text
#     )
# except:
#     d["medical-school"].append("missing")

# try:
#     d["career-plans"].append(
#         row.find("div.field--name-field-career-plans")[0].text.split("\n")[-1]
#     )
# except:
#     d["career-plans"].append("missing")

#     try:
#         bio = row.find("div.field--name-field-brief-description")[0].text.split("\n")[
#             -1
#         ]
#         d["bio"].append(bio)
#     except:
#         d["bio"].append("missing")
#
#     try:
#         root_url = "https://medicine.vumc.org"
#         try:
#             src = (
#                 root_url
#                 + row.find("div.field--name-field-barista-photo")[0]
#                 .find("img")[0]
#                 .attrs["src"]
#             )
#         except:
#             src = ""
#         try:
#             href = (
#                 root_url
#                 + row.find("div.field--name-field-barista-photo")[0]
#                 .find("a")[0]
#                 .attrs["href"]
#             )
#         except:
#             href = ""
#         try:
#             alt = (
#                 row.find("div.field--name-field-barista-photo")[0]
#                 .find("img")[0]
#                 .attrs["alt"]
#             )
#         except:
#             alt = ""
#
#         img_dict = {
#             "img_src": f"{src}",
#             "href": f"{href}",
#             "alt": f"{alt}",
#             "width": 100,
#         }
#         img_json = json.dumps(img_dict)
#         d["img"].append(img_json)
#
#         popup_dict = {
#             "image": src,
#             "alt": alt,
#             "title": alt,
#             "description": bio,
#             "link": href,
#         }
#
#         popup_json = json.dumps(popup_dict)
#         d["popup"].append(popup_json)
#
#     except:
#         d["img"].append("missing")
#         d["popup"].append("missing")

# return d
