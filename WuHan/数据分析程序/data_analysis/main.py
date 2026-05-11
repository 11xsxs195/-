from __future__ import annotations

import argparse
import os
import runpy
from pathlib import Path

import matplotlib.pyplot as plt

from analysis_common import CITY_NAME, export_standard_data


BASE_DIR = Path(__file__).resolve().parent
LATLNG_FILE = BASE_DIR / "artifacts" / "latlng.csv"


def run_script(relative_path: str) -> None:
    script_path = BASE_DIR / relative_path
    print(f"[RUN] {relative_path}")
    runpy.run_path(str(script_path), run_name="__main__")
    plt.close("all")


def has_nonempty_file(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def main() -> None:
    parser = argparse.ArgumentParser(description=f"{CITY_NAME}二手房数据分析主入口")
    parser.add_argument("--skip-map", action="store_true", help="跳过地理编码和地图文件生成")
    parser.add_argument("--skip-cluster", action="store_true", help="跳过聚类分析")
    parser.add_argument("--only-standardize", action="store_true", help="只生成标准化数据文件")
    args = parser.parse_args()

    print(f"开始执行{CITY_NAME}二手房数据分析流程")
    standard_file = export_standard_data()
    print(f"标准化数据已生成: {standard_file}")

    if args.only_standardize:
        return

    run_script("preprocessing/test_clean.py")
    run_script("analysis/price_and_area.py")
    run_script("analysis/house_attr.py")
    run_script("analysis/business_attr.py")
    run_script("analysis/test_ana.py")
    run_script("analysis/ciyun.py")

    if not args.skip_map:
        if os.environ.get("BAIDU_MAP_AK"):
            run_script("analysis/baidu_map.py")
            map_generated = True
        else:
            print("[SKIP] 未设置 BAIDU_MAP_AK，跳过地理编码和地图文件生成")
            map_generated = False
    else:
        map_generated = False

    if not args.skip_cluster and map_generated and has_nonempty_file(LATLNG_FILE):
        run_script("clustering/run.py")
    elif not args.skip_cluster:
        print("[SKIP] 未生成本次可用的坐标文件，跳过聚类分析")

    print("分析流程执行完成")


if __name__ == "__main__":
    main()