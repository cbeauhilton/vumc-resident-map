import os

from deta import Deta
from sqlite_utils import Database

project_id = os.environ.get("DETA_ID_RESIDENTS")
base_name = os.environ.get("DETA_BASE_NAME_RESIDENTS")
API_key = os.environ.get("DETA_TOKEN_RESIDENTS")

deta = Deta(API_key)
db = deta.Base("residents")
grab = db.fetch()
response = grab.items

# fetch until last is 'None'
while grab.last:
    grab = db.fetch(last=grab.last)
    response += grab.items

print(response)

db_file = "data/db.db"
db = Database(db_file, recreate=True)

db["hometowns"].insert_all(response, alter=True, pk="key")
