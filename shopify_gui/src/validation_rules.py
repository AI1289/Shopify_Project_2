import pandas as pd

def validate_rows(df, mapped_headers):
    errors = []
    required_fields = ["Title", "Handle", "Variant Price"]
    for idx, row in df.iterrows():
        for raw_col, shopify_col in mapped_headers.items():
            if shopify_col in required_fields:
                val = row.get(raw_col)
                if pd.isna(val) or str(val).strip() == "":
                    errors.append(f"Row {idx+1}: Missing value for required field '{shopify_col}' (source column: '{raw_col}')")
    return errors
