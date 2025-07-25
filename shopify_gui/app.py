import streamlit as st
import pandas as pd
from src.header_mapper import map_headers
from src.validation_rules import validate_rows
from src.shopify_csv_handler import export_to_csv

st.set_page_config(page_title="Shopify Importer", layout="wide")
st.title("Smart Shopify CSV Importer & Manager")

uploaded_file = st.file_uploader("Upload a product file (.csv/.xlsx)", type=["csv", "xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith("xlsx") else pd.read_csv(uploaded_file)
    st.session_state["original_df"] = df.copy()
    st.subheader("Raw Data")
    st.dataframe(df, use_container_width=True)

    st.subheader("Header Mapping")
    mapped_headers = map_headers(df.columns.tolist())
    st.json(mapped_headers)

    st.subheader("Validation Results")
    errors = validate_rows(df, mapped_headers)
    if errors:
        st.error("Validation Issues Detected:")
        st.write(errors)
    else:
        st.success("All rows passed validation!")

    if st.button("Export Shopify CSV"):
        csv_data = export_to_csv(df, mapped_headers)
        st.download_button("Download CSV", csv_data, file_name="shopify_export.csv", mime="text/csv")
