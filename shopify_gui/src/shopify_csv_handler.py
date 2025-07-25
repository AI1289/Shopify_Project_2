import pandas as pd
from io import StringIO

def export_to_csv(df, mapped_headers):
    renamed_df = df.rename(columns=mapped_headers)
    buffer = StringIO()
    renamed_df.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer.getvalue()
