from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))

from analysis_common import CITY_NAME, configure_matplotlib, load_analysis_data


configure_matplotlib(plt)
df = load_analysis_data()


"""武汉各区域二手房平均单价"""
groups_unitprice_area = df["unitPriceValue"].groupby(df["areaName"])
mean_unitprice = groups_unitprice_area.mean()
mean_unitprice.index.name = "各区域名称"

fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(111)
ax.set_ylabel("单价(元/平米)")
ax.set_title(f"{CITY_NAME}各区域二手房平均单价")
mean_unitprice.plot(kind="bar")


"""武汉各区域二手房平均建筑面积"""
groups_area_jzmj = df["jzmj"].groupby(df["areaName"])
mean_jzmj = groups_area_jzmj.mean()
mean_jzmj.index.name = "各区域名称"

fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(111)
ax.set_ylabel("建筑面积(㎡)")
ax.set_title(f"{CITY_NAME}各区域二手房平均建筑面积")
mean_jzmj.plot(kind="bar")


"""武汉各区域平均单价和平均建筑面积"""
groups_unitprice_area = df["unitPriceValue"].groupby(df["areaName"])
mean_unitprice = groups_unitprice_area.mean()
mean_unitprice.index.name = ""

groups_area_jzmj = df["jzmj"].groupby(df["areaName"])
mean_jzmj = groups_area_jzmj.mean()
mean_jzmj.index.name = "各区域名称"

fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax1.set_ylabel("单价(元/平米)")
ax1.set_title(f"{CITY_NAME}各区域二手房平均单价")
ax2 = fig.add_subplot(2, 1, 2)
ax2.set_ylabel("建筑面积(㎡)")
ax2.set_title(f"{CITY_NAME}各区域二手房平均建筑面积")
plt.subplots_adjust(hspace=0.4)

mean_unitprice.plot(kind="bar", ax=ax1)
mean_jzmj.plot(kind="bar", ax=ax2)


"""武汉各区域二手房房源数量"""
groups_area = df["id"].groupby(df["areaName"])
count_area = groups_area.count()
count_area.index.name = "各区域名称"

fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(111)
ax.set_ylabel("房源数量(套)")
ax.set_title(f"{CITY_NAME}各区域二手房房源数量")
count_area.plot(kind="bar")


"""武汉二手房单价最高Top10"""
unitprice_top = df.sort_values(by="unitPriceValue", ascending=False)[:10]
unitprice_top.set_index(unitprice_top["communityName"], inplace=True)
unitprice_top.index.name = ""

fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(111)
ax.set_ylabel("单价(元/平米)")
ax.set_title(f"{CITY_NAME}二手房单价最高Top10")
unitprice_top["unitPriceValue"].plot(kind="bar")


"""武汉二手房房屋户型占比情况"""
count_fwhx = df["fwhx"].value_counts()[:10]
count_other_fwhx = pd.Series({"其他": df["fwhx"].value_counts()[10:].count()})
count_fwhx = pd.concat([count_fwhx, count_other_fwhx])
count_fwhx.index.name = ""
count_fwhx.name = ""

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111)
ax.set_title(f"{CITY_NAME}二手房房屋户型占比情况")
count_fwhx.plot(kind="pie", cmap=plt.cm.rainbow, autopct="%3.1f%%")


"""武汉二手房房屋朝向分布情况"""
count_fwcx = df["fwcx"].value_counts()[:15]
count_other_fwcx = pd.Series({"其他": df["fwcx"].value_counts()[15:].count()})
count_fwcx = pd.concat([count_fwcx, count_other_fwcx])

fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(111)
ax.set_title(f"{CITY_NAME}房源朝向分布情况")
count_fwcx.plot(kind="bar")


"""武汉二手房建筑面积分布区间"""
area_level = [0, 50, 100, 150, 200, 250, 300, 500]
label_level = ["小于50", "50-100", "100-150", "150-200", "200-250", "250-300", "300-350"]
jzmj_cut = pd.cut(df["jzmj"], area_level, labels=label_level)
jzmj_result = jzmj_cut.value_counts()

fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(111)
ax.set_ylabel("建筑面积(㎡)")
ax.set_title(f"{CITY_NAME}二手房建筑面积分布区间")
jzmj_result.plot(kind="barh")