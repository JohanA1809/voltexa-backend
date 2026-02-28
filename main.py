from fastapi import FastAPI, UploadFile, File
import os
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def root():
    return {"mensaje": "Backend Voltexa funcionando"}

@app.post("/analizar")
async def analizar_factura(file: UploadFile = File(...)):
    contenido = await file.read()

    # Aquí luego pondremos extracción PDF
    return {
        "energy_score": 75,
        "nivel": "Bueno",
        "mensaje": "Simulación inicial funcionando"
    }