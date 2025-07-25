import streamlit as st
import pandas as pd
from src.template_manager import load_template, save_template, list_templates

st.set_page_config(page_title="Shopify Importer", layout="wide")
st.title("Smart Shopify CSV Importer & Manager")

uploaded_file = st.file_uploader("Upload a product file (.csv/.xlsx)", type=["csv", "xlsx"])

# Template UI
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
        save_template(name, {}, {})  # Placeholder
        st.success(f"Saved template as: {name}")

# Main logic
if uploaded_file:
    df_raw = pd.read_excel(uploaded_file) if uploaded_file.name.endswith("xlsx") else pd.read_csv(uploaded_file)
    st.session_state["original_df"] = df_raw.copy()

    st.subheader("Raw Data (Editable)")
    df = st.data_editor(df_raw, num_rows="dynamic", use_container_width=True)

    # Column Formula Assignment UI
    st.sidebar.subheader("Column Formulas")
    if "column_formulas" not in st.session_state:
        st.session_state["column_formulas"] = {}

    column_to_edit = st.sidebar.selectbox("Select Column", df.columns)
    current_formula = st.session_state["column_formulas"].get(column_to_edit, "")
    formula_input = st.sidebar.text_input("Formula (Python expr)", value=current_formula, key="formula_input")

    if st.sidebar.button("Apply Formula"):
        from src.formula_engine import apply_formula
        st.session_state["column_formulas"][column_to_edit] = formula_input
        df = apply_formula(df, column_to_edit, formula_input)

    # Header Mapping (after editing)
    st.subheader("Header Mapping")
    from src.header_mapper import map_headers
    mapped_headers = map_headers(df.columns.tolist())
    st.json(mapped_headers)

    # Validation (after mapping)
    st.subheader("Validation Results")
    from src.validation_rules import validate_rows
    errors = validate_rows(df, mapped_headers)
    if errors:
        st.error("Validation Issues Detected:")
        st.write(errors)
    else:
        st.success("All rows passed validation!")

    # Export (after formula and mapping)
    if st.button("Export Shopify CSV"):
        from src.shopify_csv_handler import export_to_csv
        csv_data = export_to_csv(df, mapped_headers)
        st.download_button("Download CSV", csv_data, file_name="shopify_export.csv", mime="text/csv")
