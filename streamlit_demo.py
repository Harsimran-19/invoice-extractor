import streamlit as st
import uvicorn
import os
from ingest import run_ingestion
from engine import extract_info


data_folder = "data"  # Change this if needed

def ingest_pdf(uploaded_file):
  if not uploaded_file:
    return st.error("Please upload a PDF file")
  try:
    # Ensure data folder exists
    if not os.path.exists(data_folder):
      os.makedirs(data_folder)
    
    # Clear existing PDFs (optional)
    for filename in os.listdir(data_folder):
      file_path = os.path.join(data_folder, filename)
      if os.path.isfile(file_path):
        os.unlink(file_path)

    # Save uploaded file
    with open(os.path.join(data_folder, uploaded_file.name), "wb") as buffer:
      buffer.write(uploaded_file.getvalue())
    try:
        run_ingestion()
    except Exception as e:
        print(e)
    st.success("PDF file ingested successfully!")
    extracted_text = extract_info()
    st.write("Extracted Text:")
    st.text(extracted_text)
    # Call your text extraction function (if implemented)
    # if extract_info:
    #   extracted_text = extract_info(os.path.join(data_folder, uploaded_file.name))
    #   st.write("Extracted Text:")
    #   st.text(extracted_text)
  except Exception as e:
    st.error(f"An error occurred: {str(e)}")

st.title("PDF Ingestion and Text Extraction App")
uploaded_file = st.file_uploader("Choose a PDF file to upload")

if uploaded_file:
  ingest_pdf(uploaded_file)