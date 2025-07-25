import streamlit as st
import pandas as pd
from src.header_mapper import map_headers
from src.validation_rules import validate_rows
from src.shopify_csv_handler import export_to_csv

st.set_page_config(page_title="Shopify Importer", layout="wide")
st.title("Smart Shopify CSV Importer & Manager")

from src.template_manager import load_template, save_template, list_templates

st.sidebar.subheader("Templates")

template_list = list_templates()
selected_template = st.sidebar.selectbox("Load Template", ["None"] + template_list)
if selected_template != "None":
    template = load_template(selected_template)
    st.session_state["loaded_template"] = template
    st.success(f"Loaded template: {selected_template}")

if st.sidebar.button("Save Current as Template"):
    name = st.sidebar.text_input("Template Name", key="template_name")
    if name and "original_df" in st.session_state:
        save_template(name, {}, {})  # Placeholder: pass actual header_mapping & formulas
        st.success(f"Saved template as: {name}")

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
