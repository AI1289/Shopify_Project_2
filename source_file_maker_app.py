import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Source File Maker", layout="wide")
st.title("🧩 Source File Maker – Shopify Format Generator")

# --- Sidebar Template Configuration ---
st.sidebar.header("Configuration")
def_fields = ["Model", "SKU", "Price", "Weight (lbs)", "Voltage", "Power HP"]
selected_fields = st.sidebar.multiselect("Select Fields to Include", def_fields, default=def_fields)

row_count = st.sidebar.number_input("Number of Rows", min_value=1, max_value=100, value=10, step=1)

if st.sidebar.button("Generate Blank Table"):
    st.session_state.df = pd.DataFrame(columns=selected_fields, index=range(row_count))

# --- Table Editor ---
if "df" in st.session_state:
    edited_df = st.data_editor(st.session_state.df, use_container_width=True, num_rows="dynamic")

    # --- Export Buttons ---
    st.markdown("### Export")
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
else:
    st.info("Use the sidebar to configure and generate your source file.")
