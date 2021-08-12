import base64
from PIL import Image
from io import BytesIO
import pandas as pd

with open("img/lee.jpg", "rb") as image_file:
    data = base64.b64encode(image_file.read())

df = pd.read_csv("interns.csv")
df["pic"] = data
df.to_csv("interns_pics.csv")
