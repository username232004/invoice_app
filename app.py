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
    date = "Not Found"
    total = "Not Found"

    # Regex-based search (more reliable than split)
    invoice_match = re.search(r"(Invoice\s*#?:?\s*)(\w+)", text, re.IGNORECASE)
    date_match = re.search(r"(Date\s*:?)(\s*\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", text, re.IGNORECASE)
    total_match = re.search(r"(Total\s*:?)(\s*\$?\s*\d+[.,]?\d*)", text, re.IGNORECASE)

    if invoice_match:
        invoice_number = invoice_match.group(2).strip()
    if date_match:
        date = date_match.group(2).strip()
    if total_match:
        total = total_match.group(2).strip()

    df = pd.DataFrame([{"Invoice Number": invoice_number, "Date": date, "Total": total}])
    
    st.subheader("Extracted Data")
    st.write(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "invoice_data.csv", "text/csv")
