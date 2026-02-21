import glob
from pathlib import Path
from typing import List

import pandas as pd


def find_excel_files(dir_path: Path) -> List[Path]:
    patterns = [str(dir_path / "*.xlsx"), str(dir_path / "*.xls")]
    files = []
    for pattern in patterns:
        files.extend(Path(p) for p in glob.glob(pattern))
    files = [path for path in files if not path.name.startswith("~")]
    return sorted(files)


def read_excel_file(path: Path) -> pd.DataFrame:
    try:
        df = pd.read_excel(path, engine="openpyxl")
    except Exception:
        df = pd.read_excel(path)
    df.columns = [str(column).strip().lower() for column in df.columns]
    return df
