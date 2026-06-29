import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from dotenv import load_dotenv

# 1. LOAD ENVIRONMENT CONFIGURATION
load_dotenv()
RAW_API_KEY = os.getenv("GEMINI_API_KEY")

if not RAW_API_KEY:
    raise RuntimeError("CRITICAL ERROR: GEMINI_API_KEY is missing from your .env file!")

# 2. INITIALIZE APP WITH DISABLED ROOT DOCS OVERRIDE
# We explicitly tell FastAPI to get out of the way of our root URL
app = FastAPI(
    title="Zero-Cost Portfolio AI Engine",
    docs_url="/docs",       # Swagger stays on /docs
    redoc_url=None          # Disable redoc to avoid endpoint hijacking
)

# 3. CONFIGURE CORS SECURITY
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GUEST_GATEWAY_PASSWORD = "PortfolioGuest2026"

# ==========================================
# ROUTE A: SERVE THE VISUAL FRONTEND PANEL
# ==========================================
@app.get("/", response_class=HTMLResponse)
async def read_index():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    html_file_path = os.path.join(current_directory, "index.html")
    
    if not os.path.exists(html_file_path):
        return HTMLResponse(
            content=f"<h1>Backend online!</h1><p>But could not find your 'index.html' file at: {html_file_path}</p>", 
            status_code=404
        )
        
    with open(html_file_path, "r", encoding="utf-8") as f:
        return f.read()

# ==========================================
# ROUTE B: PROCESS THE AI PDF STREAM
# ==========================================
@app.post("/api/summarize")
async def summarize_pdf_stream(
    file: UploadFile = File(...),
    query: str = Form(...),
    guest_password: str = Form(...)
):
    if guest_password != GUEST_GATEWAY_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid format.")

    try:
        pdf_bytes = await file.read()
        client = genai.Client(api_key=RAW_API_KEY)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
                f"Analyze the document: {query}"
            ]
        )
        return {"success": True, "analysis": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))