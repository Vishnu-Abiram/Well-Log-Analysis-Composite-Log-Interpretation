"""Helpers for loading LAS and CSV well-log files for the analysis notebook."""

from pathlib import Path

import pandas as pd


def load_well(path: str | Path) -> pd.DataFrame:
    """Load a LAS or CSV file and return a numeric dataframe with a Depth column.

    LAS support uses the optional ``lasio`` package. Curve mnemonics are
    normalized to uppercase so the notebook's standard names work regardless
    of capitalization in the source file.
    """
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".las":
        try:
            import lasio
        except ImportError as exc:
            raise ImportError("LAS input requires lasio. Install it with `pip install lasio`.") from exc
        las = lasio.read(path)
        frame = las.df().reset_index()
        frame = frame.rename(columns={frame.columns[0]: "Depth"})
    elif suffix in {".csv", ".txt"}:
        frame = pd.read_csv(path)
    else:
        raise ValueError(f"Unsupported file type {suffix!r}; use .las or .csv.")

    frame.columns = [str(column).strip().upper() for column in frame.columns]
    # Common depth-curve aliases found in LAS exports.
    if "DEPTH" not in frame.columns:
        for alias in ("DEPT", "MD", "TDEP"):
            if alias in frame.columns:
                frame = frame.rename(columns={alias: "DEPTH"})
                break
    if "DEPTH" not in frame.columns:
        raise ValueError("No depth column found. Expected DEPTH, DEPT, MD, or TDEP.")

    frame = frame.rename(columns={"DEPTH": "Depth"})
    frame = frame.apply(pd.to_numeric, errors="coerce")
    frame = frame.replace([-999.25, -999.0, -9999.0], float("nan"))
    frame = frame.dropna(subset=["Depth"]).sort_values("Depth").reset_index(drop=True)
    if frame.empty:
        raise ValueError("The input contains no usable depth samples.")
    return frame
