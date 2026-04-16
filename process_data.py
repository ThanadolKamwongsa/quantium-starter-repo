import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_FILE = Path(__file__).parent / "formatted_sales_data.csv"

input_files = sorted(DATA_DIR.glob("daily_sales_data_*.csv"))
frames = [pd.read_csv(f) for f in input_files]
df = pd.concat(frames, ignore_index=True)

df = df[df["product"].str.lower() == "pink morsel"].copy()

df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)
df["sales"] = df["price"] * df["quantity"]

result = df[["sales", "date", "region"]].rename(columns={"sales": "Sales", "date": "Date", "region": "Region"})
result.to_csv(OUTPUT_FILE, index=False)

print(f"Wrote {len(result)} rows to {OUTPUT_FILE}")
