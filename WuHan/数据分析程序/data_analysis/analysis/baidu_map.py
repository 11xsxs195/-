from pathlib import Path
import json
import os
import sys
from urllib.parse import quote

import matplotlib.pyplot as plt
import pandas as pd
import requests

sys.path.append(str(Path(__file__).resolve().parents[1]))

from analysis_common import CITY_NAME, configure_matplotlib, load_analysis_data


def getlnglat(address):
    url_base = "http://api.map.baidu.com/geocoder/v2/"
    output = "json"
    ak = os.environ.get("BAIDU_MAP_AK", "")
    if not ak:
        return None, None
    address = quote(address)
    url = url_base + "?" + "address=" + address + "&output=" + output + "&ak=" + ak
    try:
        res = requests.get(url, timeout=10)
        temp = json.loads(res.text)
    except Exception:
        return None, None
    if temp.get("status") == 0:
        lat = temp["result"]["location"]["lat"]
        lng = temp["result"]["location"]["lng"]
        return lat, lng
    return None, None


configure_matplotlib(plt)
df = load_analysis_data()
BASE_DIR = Path(__file__).resolve().parents[1]


id_values = []
name_values = []
lat_values = []
lng_values = []

for item_id, name in zip(list(df["id"]), list(df["communityName"])):
    lat, lng = getlnglat(f"{CITY_NAME}市{name}")
    if lat is not None and lng is not None:
        id_values.append(item_id)
        name_values.append(name)
        lat_values.append(lat)
        lng_values.append(lng)
        print(item_id)

frame_test = pd.DataFrame({"id": id_values, "communityName": name_values, "lat": lat_values, "lng": lng_values})
latlng_path = BASE_DIR / "artifacts" / "latlng.csv"
latlng_path.parent.mkdir(parents=True, exist_ok=True)
if frame_test.empty:
    raise RuntimeError("未获取到任何有效经纬度，请检查 BAIDU_MAP_AK、IP 白名单或网络连接")
frame_test.to_csv(latlng_path, index=False, encoding="utf-8-sig")

df_latlng = pd.read_csv(latlng_path)
df_merge = pd.merge(df, df_latlng, on="id")

xiaoyu = df_merge[df_merge["total"] < 201]

out_map = BASE_DIR / "artifacts" / "star.txt"
with open(out_map, "w", encoding="utf-8") as file_out:
    for lng, lat in zip(list(xiaoyu["lng"]), list(xiaoyu["lat"])):
        file_out.write(f"{lng},{lat}\n")
