import streamlit as st
import pdfplumber
import pandas as pd
import re

st.title("📄 AI Invoice Data Extractor")

uploaded_file = st.file_uploader("Upload an Invoice PDF", type="pdf")

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # Default values
    invoice_number = "Not Found"
    invoice_date = "Not Found"
    total = "Not Found"

    # Regex-based search (more reliable than split)
   
    invoice_number_match = re.search(r"Invoice Number\s*(.+)", page_text)
    invoice_date_match = re.search(r"Invoice Date\s*(.+)", page_text)
    total_match = re.search(r"Total Due\s*\$(.+)", page_text)
    
    invoice_number = invoice_number_match.group(1).strip() if invoice_number_match else None
    invoice_date = invoice_date_match.group(1).strip() if invoice_date_match else None
    total = total_match.group(1).strip() if total_match else None

    df = pd.DataFrame([{"Invoice Number": invoice_number, "Date": invoice_date, "Total": total}])
    
    st.subheader("Extracted Data")
    st.write(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "invoice_data.csv", "text/csv")


