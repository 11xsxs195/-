from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from analysis_common import export_standard_data


export_standard_data()
