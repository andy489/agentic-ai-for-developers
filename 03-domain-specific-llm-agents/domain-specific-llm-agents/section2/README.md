# Section 2 — Data Preparation and Preprocessing

Cleans, formats, and annotates a raw GPU metrics CSV (DCGM) to produce a training-ready dataset for fine-tuning domain-specific LLMs.

## Script

| File | Purpose |
|------|---------|
| `data-prep.py` | Full pipeline: load → clean → format → annotate → save |

## Input data

The script expects a file named `dcgm.csv` in the same directory.

**DCGM** (Data Center GPU Manager) metrics CSV — typical columns:

| Column | Description |
|--------|-------------|
| `gpu_id` | GPU identifier (dropped during prep) |
| `avgsmutilization_pct` | Average SM utilisation (%) |
| `totalexecutiontime_sec` | Total execution time (seconds) |
| *(other numeric GPU metrics)* | Power, memory, temperature, etc. |

> The file is not included in this repo (course asset). Replace it with any CSV containing GPU metrics, or adapt the column references in the script to match your own schema.

## Setup

```bash
pip install pandas numpy
```

## Run

```bash
python data-prep.py
```

Expected output:

```
🔹 Step 1: Loading dataset...
 Dataset loaded successfully.
...
🔹 Step 5: Saving the prepared dataset...
 Prepared dataset saved as 'prepared_dcgm.csv'.
```

## Pipeline steps

| Step | What happens |
|------|-------------|
| **Load** | Read `dcgm.csv` with `pandas.read_csv` |
| **Clean** | Fill NaN → 0, drop duplicates, drop `gpu_id` column |
| **Format** | Cast `totalexecutiontime_sec` to float; convert all numeric columns to float32 |
| **Annotate** | Add `gpu_utilization_category` column (`Idle` / `Low` / `Medium` / `High`) based on `avgsmutilization_pct` |
| **Save** | Write `prepared_dcgm.csv` (no index) |

## Output

| File | Description |
|------|-------------|
| `prepared_dcgm.csv` | Cleaned and annotated dataset, ready for downstream use |

## Adapting to your own data

1. Replace `dcgm.csv` with your file, or change `file_path` at the top of the script.
2. Update `columns_to_drop` if different columns are redundant.
3. Update the `annotate_utilization` column reference (`avgsmutilization_pct`) to match your schema.
4. The float32 cast applies to all numeric columns — safe to leave as-is.

## Notes

- Missing `dcgm.csv` causes an early exit with a clear error message — no silent failures.
- Large CSVs (>1 M rows) may take several seconds; progress is not printed per-row by design.
- The output CSV uses the same column order as the input minus any dropped columns, plus the new annotation column appended at the end.
