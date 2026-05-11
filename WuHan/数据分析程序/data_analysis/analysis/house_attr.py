from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))

from analysis_common import CITY_NAME, configure_matplotlib, load_analysis_data


configure_matplotlib(plt)
df = load_analysis_data()


"""武汉二手房房屋户型占比情况"""
count_fwhx = df["fwhx"].value_counts()[:10]
count_other_fwhx = pd.Series({"其他": df["fwhx"].value_counts()[10:].count()})
count_fwhx = pd.concat([count_fwhx, count_other_fwhx])
count_fwhx.index.name = ""
count_fwhx.name = ""

fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(111)
ax.set_title(f"{CITY_NAME}二手房房屋户型占比情况", fontsize=18)
count_fwhx.plot(kind="pie", cmap=plt.cm.rainbow, autopct="%3.1f%%", fontsize=12)


"""武汉二手房房屋朝向分布情况"""
count_fwcx = df["fwcx"].value_counts()[:15]
count_other_fwcx = pd.Series({"其他": df["fwcx"].value_counts()[15:].count()})
count_fwcx = pd.concat([count_fwcx, count_other_fwcx])

fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(111)
ax.set_title("房源朝向分布情况", fontsize=18)
count_fwcx.plot(kind="bar", fontsize=12)


"""武汉二手房建筑面积分布区间"""
area_level = [0, 50, 100, 150, 200, 250, 300, 500]
label_level = ["小于50", "50-100", "100-150", "150-200", "200-250", "250-300", "300-350"]
jzmj_cut = pd.cut(df["jzmj"], area_level, labels=label_level)
jzmj_result = jzmj_cut.value_counts()

fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(111)
ax.set_ylabel("建筑面积(㎡)", fontsize=14)
ax.set_title(f"{CITY_NAME}二手房建筑面积分布区间", fontsize=18)
jzmj_result.plot(kind="barh", fontsize=12)
