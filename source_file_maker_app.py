import streamlit as st
import pandas as pd
import re
from io import BytesIO

st.set_page_config(page_title="Source File Maker", layout="wide")
st.title("🛠️ Shopify Source File Creator")
st.caption("Build and edit clean Shopify product data files from scratch or supplier input.")

# --- Sidebar Configuration ---
st.sidebar.header("Configuration")
def_fields = ["Model", "SKU", "Price", "Weight (lbs)", "Voltage", "Power HP"]
template_shopify_fields = ["Handle", "Title", "Body (HTML)", "Vendor", "Type", "Tags", "Published"] + def_fields

selected_template = st.sidebar.selectbox("Select Template", ["Custom", "Shopify Basic"])
selected_fields = template_shopify_fields if selected_template == "Shopify Basic" else st.sidebar.multiselect("Select Fields to Include", def_fields, default=def_fields)

row_count = st.sidebar.number_input("Number of Rows", min_value=1, max_value=100, value=10, step=1)
if st.sidebar.button("Generate Blank Table"):
    st.session_state.df = pd.DataFrame(columns=selected_fields, index=range(row_count))

# --- File Import Function ---
st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("Import Existing File", type=["csv", "xlsx"])
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            st.session_state.df = pd.read_csv(uploaded_file)
        else:
            st.session_state.df = pd.read_excel(uploaded_file)
        st.success("File imported successfully.")
    except Exception as e:
        st.error(f"Error loading file: {e}")

# --- Delete Column Function ---
if "df" in st.session_state:
    st.sidebar.markdown("---")
    col_to_delete = st.sidebar.selectbox("Delete Column", st.session_state.df.columns.tolist())
    if st.sidebar.button("Remove Column"):
        if len(st.session_state.df.columns) > 1:
            st.session_state.df.drop(columns=[col_to_delete], inplace=True)
            st.success(f"Column '{col_to_delete}' removed.")
        else:
            st.warning("You must have at least one column remaining.")

# --- Table Editor ---
if "df" in st.session_state:
    edited_df = st.session_state.df.copy()

    # --- Formula Assignment ---
    column_formulas = st.session_state.get("column_formulas", {})
    with st.expander("🧮 Assign Column Formulas", expanded=False):
        formula_col = st.selectbox("Select Column to Assign Formula", options=edited_df.columns, key="formula_col")
        current_formula = column_formulas.get(formula_col, "")
        new_formula = st.text_input("Formula for column (Python-style, use column names)", value=current_formula, key="formula_input")
        if st.button("Assign Formula"):
            column_formulas[formula_col] = new_formula
            st.session_state.column_formulas = column_formulas
            st.success(f"Formula assigned to '{formula_col}': {new_formula}")

    # Apply formulas after edit_df is initialized
    for col, expr in st.session_state.get("column_formulas", {}).items():
        try:
            edited_df[col] = edited_df.eval(expr)
        except Exception as e:
            st.warning(f"Could not evaluate formula for '{col}': {e}")

    # --- Batch Edit Tools ---
    with st.expander("⚙️ Bulk Actions", expanded=False):
        selected_column = st.selectbox("Select Column for Action", edited_df.columns, key="action_col")
        action = st.selectbox("Action", ["Fill All", "Clear All", "Duplicate First Value"], key="bulk_action")

        if action == "Fill All":
            fill_value = st.text_input("Enter value to fill", key="fill_value")
        else:
            fill_value = None

        if st.button("Apply to Column"):
            if action == "Fill All" and fill_value:
                edited_df[selected_column] = fill_value
                st.success(f"All values in '{selected_column}' filled with '{fill_value}'")
            elif action == "Clear All":
                edited_df[selected_column] = ""
                st.success(f"All values in '{selected_column}' cleared.")
            elif action == "Duplicate First Value":
                first_val = edited_df[selected_column].iloc[0]
                edited_df[selected_column] = first_val
                st.success(f"All values in '{selected_column}' copied from first row.")

    edited_df = st.data_editor(edited_df, use_container_width=True, num_rows="dynamic", key="editor")

    # --- Basic Validation (SKU, Price) ---
    def validate(df):
        errors = []
        if "SKU" in df.columns:
            invalid_skus = df[~df["SKU"].astype(str).str.match(r"^[A-Za-z0-9\-]+$")].index.tolist()
            duplicates = df[df.duplicated("SKU", keep=False)].index.tolist()
            if invalid_skus:
                errors.append(f"Invalid SKU format in rows: {invalid_skus}")
            if duplicates:
                errors.append(f"Duplicate SKUs in rows: {duplicates}")
        if "Price" in df.columns:
            invalid_prices = df[~df["Price"].apply(lambda x: pd.notnull(x) and isinstance(x, (int, float)) and x >= 0)].index.tolist()
            if invalid_prices:
                errors.append(f"Invalid Price values in rows: {invalid_prices}")
        return errors

    validation_errors = validate(edited_df)
    if validation_errors:
        st.warning("Validation issues found:\n" + "\n".join(validation_errors))
    else:
        st.success("All validations passed.")

    # --- Export Buttons ---
    st.markdown("### Export")
    st.caption("Export your product table in the format Shopify accepts (CSV or Excel).")
    col1, col2 = st.columns(2)

    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode("utf-8")

    def convert_df_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Products')
        return output.getvalue()

    with col1:
        csv = convert_df_to_csv(edited_df)
        st.download_button("Download as CSV", data=csv, file_name="source_template.csv", mime="text/csv")

    with col2:
        excel = convert_df_to_excel(edited_df)
        st.download_button("Download as Excel", data=excel, file_name="source_template.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Update session state
    st.session_state.df = edited_df.copy()

else:
    st.info("Use the sidebar to configure and generate your source file.")
