from http.client import HTTPResponse
from importlib.resources import contents
import json
from urllib.request import urlopen
import time
import pandas as pd

data = pd.read_csv('data/id_test.csv')
ids = data['id'][2200:]

url = "https://store.steampowered.com/api/appdetails?appids="

with open("data/detail_test_korean.json", "r", encoding="utf8") as f:
    contents = f.read()
    detail_list = json.loads(contents)

print(len(detail_list))


for id in ids:
    id = str(id)

    try:
        HTTPResponse = urlopen(url+id+"&l=korean")
        detail_data = json.load(HTTPResponse)
    except:
        print("Except", id)
        HTTPResponse = urlopen(url+id)
        detail_data = json.load(HTTPResponse)

    if detail_data[id]["success"] == True:
        detail_list[id] = detail_data[id]
    else:
        print(id, "Success == False")

with open('data/detail_test_korean.json', 'w', encoding='utf-8') as outfile:
    json.dump(detail_list, outfile, indent='\t', ensure_ascii=False)

print(len(detail_list))
