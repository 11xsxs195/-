from pathlib import Path
import sys

import matplotlib.pyplot as plt

sys.path.append(str(Path(__file__).resolve().parents[1]))

from analysis_common import CITY_NAME, configure_matplotlib, load_analysis_data


configure_matplotlib(plt)
df = load_analysis_data()


"""武汉二手房房屋用途占水平柱状图"""
count_fwyt = df["fwyt"].value_counts(ascending=True)
count_fwyt.name = ""

fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(111)
ax.set_xlabel("房源数量(套)", fontsize=14)
ax.set_title(f"{CITY_NAME}二手房房屋用途水平柱状图", fontsize=18)
count_fwyt.plot(kind="barh", fontsize=12)