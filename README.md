# Well Log Data Analysis

This project is a Jupyter notebook for exploratory analysis and plotting of
wireline well-log curves against measured depth. It includes basic summaries,
missing-value inspection, curve crossplots and histograms, individual log
tracks, and a composite multi-track plot.

## Project files

- `Well Log Data Analysis.ipynb` — the analysis notebook.
- `tntlog.csv` — the example dataset loaded by default.
- `well_log_utils.py` — CSV/LAS loader used by the notebook.
- `requirements.txt` — Python packages needed to run the project.

## Run it

From this folder, install dependencies and launch Jupyter:

```bash
python -m pip install -r requirements.txt
jupyter lab
```

Open the notebook and run its cells from top to bottom. It loads `tntlog.csv`
by default. To use your own file, put it in this folder and change the path in
the data-loading cell, for example:

```python
well = load_well("my_well.las")  # or "my_well.csv"
```

LAS files are read with `lasio`. The loader uses the LAS depth index and
normalizes curve mnemonics to uppercase. It recognizes `DEPTH`, `DEPT`, `MD`,
and `TDEP` for depth. The notebook's later plots refer to the example curve
names (`GR`, `SP`, `RILD`, `RLL3`, `RHOB`, `MCAL`, `DCAL`, `DPOR`, `CNLS`), so
your LAS file needs those curves or you must update the plot cells to use your
file's mnemonics. A missing curve is not scientifically interchangeable with
another curve; map aliases only when you have confirmed their meaning and units.

The example data uses depth values in the first column and has a 0.5-unit
sampling step. Some notebook plots still shade example intervals and use
example-specific axis limits; adjust those to your well's depth range and
units. The notebook is exploratory and does not perform lithology or
hydrocarbon classification.
