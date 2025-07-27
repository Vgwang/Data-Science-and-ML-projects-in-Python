import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Spreadsheet Query Tool", layout="wide")

st.title("📊 Spreadsheet Query Tool")

uploaded_files = st.file_uploader(
    "Upload one or more Excel files", type=["xlsx", "xls", "csv"], accept_multiple_files=True
)

if uploaded_files:
    all_data = []

    for file in uploaded_files:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file, engine='openpyxl')
        df["Source File"] = file.name  # track file origin
        all_data.append(df)

    combined_df = pd.concat(all_data, ignore_index=True)

    st.success(f"Loaded {len(combined_df)} rows from {len(uploaded_files)} files.")

    columns = combined_df.columns.tolist()

    selected_column = st.selectbox("Choose a column to search:", options=columns)

    query = st.text_input(f"Enter value to search in '{selected_column}':")

    if query:
        filtered_df = combined_df[combined_df[selected_column].astype(str).str.contains(query, case=False, na=False)]
        st.write(f"🔍 Found {len(filtered_df)} matching rows:")
        st.dataframe(filtered_df)

        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download results as CSV", csv, "filtered_results.csv", "text/csv")

else:
    st.info("Upload spreadsheets to begin.")
