import streamlit as st
import pdfplumber
import pandas as pd

st.title("📄 AI Invoice Data Extractor")

uploaded_file = st.file_uploader("Upload an Invoice PDF", type="pdf")

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    # Dummy extraction logic (replace with regex/logic as needed)
    invoice_number = "Not Found"
    date = "Not Found"
    total = "Not Found"

    if "Invoice" in text:
        invoice_number = text.split("Invoice")[1].split()[0]
    if "Date" in text:
        date = text.split("Date")[1].split()[0]
    if "Total" in text:
        total = text.split("Total")[1].split()[0]

    df = pd.DataFrame([{"Invoice Number": invoice_number, "Date": date, "Total": total}])
    
    st.subheader("Extracted Data")
    st.write(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "invoice_data.csv", "text/csv")
