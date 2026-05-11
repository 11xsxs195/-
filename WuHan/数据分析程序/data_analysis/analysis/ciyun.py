from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib import image as mpimg
from wordcloud import WordCloud
import jieba

sys.path.append(str(Path(__file__).resolve().parents[1]))

from analysis_common import CITY_NAME, build_wordcloud_text, configure_matplotlib, load_analysis_data


configure_matplotlib(plt)

BASE_DIR = Path(__file__).resolve().parents[1]
backpicture = BASE_DIR / "assets" / "house2.jpg"
savepicture = BASE_DIR / "analysis" / "picture" / f"{CITY_NAME}二手房数据词云.png"
fontpath = BASE_DIR / "assets" / "simhei.ttf"
stopwords = ["null", "暂无", "数据", "上传", "照片", "房本", CITY_NAME, "二手房"]

df = load_analysis_data()
comment_text = build_wordcloud_text(df)
color_mask = mpimg.imread(str(backpicture))

ershoufang_words = jieba.cut(comment_text)
ershoufang_words = [word for word in ershoufang_words if word not in stopwords]
cut_text = " ".join(ershoufang_words)

cloud = WordCloud(
    font_path=str(fontpath),
    background_color="white",
    mask=color_mask,
    max_words=2000,
    max_font_size=60,
)
word_cloud = cloud.generate(cut_text)
savepicture.parent.mkdir(parents=True, exist_ok=True)
word_cloud.to_file(str(savepicture))