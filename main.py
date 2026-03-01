from fastapi import FastAPI, UploadFile, File
import os
import pdfplumber
from openai import OpenAI
import json

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def root():
    return {"mensaje": "Backend Voltexa funcionando"}

@app.post("/analizar")
async def analizar_factura(file: UploadFile = File(...)):

    # 1️⃣ Leer contenido PDF
    texto = ""
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            texto += page.extract_text()

    # 2️⃣ Enviar texto a OpenAI para estructuración
    prompt = f"""
    Eres un analista energético experto en tarifas eléctricas colombianas.

    Extrae del siguiente texto:
    - consumo_kwh (solo número)
    - valor_total_cop (solo número)
    
    Devuelve únicamente JSON válido.
    
    Texto:
    {texto}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    contenido = response.choices[0].message.content

    try:
        datos = json.loads(contenido)
    except:
        return {"error": "No se pudo interpretar la factura"}

    consumo = float(datos.get("consumo_kwh", 0))
    valor = float(datos.get("valor_total_cop", 0))

    if consumo > 0:
        precio_real = valor / consumo
    else:
        precio_real = 0

    # 3️⃣ Calcular Energy Score simple
    if precio_real < 800:
        score = 90
    elif precio_real < 1000:
        score = 70
    else:
        score = 50

    return {
        "consumo_kwh": consumo,
        "valor_total": valor,
        "precio_real_kwh": precio_real,
        "energy_score": score
    }
    

