from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
import fitz  # PyMuPDF

app = FastAPI()

# Enable CORS so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow frontend to talk (adjust if needed)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the FLAN model pipeline from Hugging Face
flan_model = pipeline("text2text-generation", model="google/flan-t5-base")

# Helper function to extract text from PDF
def extract_pdf_text(uploaded_file: UploadFile):
    file_bytes = uploaded_file.file.read()
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

# LLM Analysis using Hugging Face FLAN model
def analyze_with_llm(text):
    prompt = f"Extract key facts, root cause, and recommendation from the following report:\n\n{text}\n\nReturn the result in JSON with keys: facts, cause, recommendation."
    result = flan_model(prompt, max_new_tokens=512)[0]['generated_text']
    return result.strip()

# This is your endpoint for FLAN-based analysis
@app.post("/analyze_with_llm")
async def analyze_with_llm_endpoint(file: UploadFile = File(...)):
    text = extract_pdf_text(file)
    analysis = analyze_with_llm(text)
    return {"analysis": analysis}
