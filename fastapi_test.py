import os
from typing import Optional
from ingest import run_ingestion
from engine import extract_info
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import requests
from utils import create_index,clear_data

app = FastAPI()

data_folder = "data"

@app.get('/')
def hello():
    return {"message":"Hello brother"}


@app.post("/ingest/")
async def ingest_pdf(file: UploadFile = File(...)):
    try:
        with open(os.path.join(data_folder, file.filename), "wb") as buffer:
            buffer.write(file.file.read())
        create_index()
        run_ingestion()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    print("Ingestion Successful")
    clear_data(data_folder)
    return {"message": "PDF file ingested successfully"}

@app.p("/extract/")
async def extract_data():
    try:
        extracted_text =extract_info()
        return JSONResponse(content=extracted_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)