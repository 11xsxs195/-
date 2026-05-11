from pathlib import Path

import numpy as np
import pandas as pd


CITY_NAME = "武汉"
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parents[1]
RAW_SOURCE_FILE = PROJECT_ROOT / "二手房挂牌信息内容_2026-05-04.csv"
STANDARD_DATA_FILE = BASE_DIR / "artifacts" / "ershoufang-wuhan-standard.csv"


def configure_matplotlib(plt):
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False


def load_wuhan_raw_data(source_path=RAW_SOURCE_FILE):
    df = pd.read_csv(source_path)
    df = df.copy()

    if "data_up_uuid" in df.columns:
        df["id"] = df["data_up_uuid"].fillna("").astype(str)
        empty_id_mask = df["id"].str.strip() == ""
        if empty_id_mask.any():
            df.loc[empty_id_mask, "id"] = df.index[empty_id_mask].astype(str)
    else:
        df["id"] = df.index.astype(str)

    rename_map = {
        "小区": "communityName",
        "所属区名称": "areaName",
        "发布价格_万元": "total",
        "房型": "fwhx",
        "朝向": "fwcx",
        "用途": "fwyt",
        "面积": "jzmj",
        "发布日期": "gpsj",
        "摘牌时间": "scjy",
        "有效期": "fwnx",
    }

    for source_col, target_col in rename_map.items():
        if source_col in df.columns:
            df[target_col] = df[source_col]

    if "total" in df.columns:
        df["total"] = pd.to_numeric(df["total"], errors="coerce")
    if "jzmj" in df.columns:
        df["jzmj"] = pd.to_numeric(df["jzmj"], errors="coerce")

    if "total" in df.columns and "jzmj" in df.columns:
        df["unitPriceValue"] = np.where(
            df["jzmj"] > 0,
            (df["total"] * 10000 / df["jzmj"]).round(0),
            np.nan,
        )

    text_columns = ["communityName", "areaName", "fwhx", "fwcx", "fwyt", "gpsj", "scjy", "fwnx"]
    for column in text_columns:
        if column in df.columns:
            df[column] = df[column].replace({"nan": np.nan, "None": np.nan})

    return df


def load_analysis_data(source_path=RAW_SOURCE_FILE):
    df = load_wuhan_raw_data(source_path)

    required_columns = ["id", "communityName", "areaName", "total", "unitPriceValue", "fwhx", "fwcx", "fwyt", "jzmj"]
    for column in required_columns:
        if column not in df.columns:
            df[column] = np.nan

    df = df.dropna(subset=["total", "jzmj", "communityName", "areaName"])
    df = df.loc[df["jzmj"] > 0]
    df = df.loc[df["total"] >= 0]
    return df


def export_standard_data(output_path=STANDARD_DATA_FILE, source_path=RAW_SOURCE_FILE):
    df = load_analysis_data(source_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    return output_path


def build_wordcloud_text(df):
    columns = [column for column in ["communityName", "areaName", "fwhx", "fwcx", "fwyt", "gpsj", "scjy"] if column in df.columns]
    text_parts = []
    for column in columns:
        text_parts.extend(df[column].dropna().astype(str).tolist())
    return " ".join(text_parts)