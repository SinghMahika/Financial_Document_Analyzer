from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
import fitz  # PyMuPDF
import logging
import traceback
 
# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
 
app = FastAPI()
 
# Enable CORS so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
# Load the FLAN model pipeline from Hugging Face
flan_model = pipeline("text2text-generation", model="google/flan-t5-base")
 
# Extract text from raw PDF bytes
def analyze_text_from_pdf_bytes(file_bytes):
    try:
        logger.debug("Starting PDF text extraction...")
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])
        logger.debug("PDF text extraction successful")
        return analyze_with_llm(text)
    except Exception as e:
        logger.error(f"Error during PDF text extraction: {e}")
        logger.error(f"Stack trace: {traceback.format_exc()}")
        raise Exception("Error extracting text from PDF")
 
# LLM Analysis using Hugging Face FLAN model
def analyze_with_llm(text):
    try:
        logger.debug("Starting LLM analysis...")
        prompt = f"Extract key facts, root cause, and recommendation from the following report:\n\n{text}\n\nReturn the result in JSON with keys: facts, cause, recommendation."
        result = flan_model(prompt, max_new_tokens=512)[0]['generated_text']
        logger.debug("LLM analysis successful")
        return result.strip()
    except Exception as e:
        logger.error(f"Error during LLM analysis: {e}")
        logger.error(f"Stack trace: {traceback.format_exc()}")
        raise Exception("Error during LLM analysis")
 
@app.get("/ping")
async def ping():
    logger.debug("Ping request received")
    return {"status": "ok"}
 
@app.post("/analyze_with_llm")
async def analyze_with_llm_endpoint(file: UploadFile = File(...)):
    try:
        logger.debug(f"Received file for analysis: {file.filename}")
        file_bytes = await file.read()
        analysis = analyze_text_from_pdf_bytes(file_bytes)
        logger.debug("Analysis completed successfully")
        return {"analysis": analysis}
    except Exception as e:
        logger.error(f"Error during file analysis: {e}")
        logger.error(f"Stack trace: {traceback.format_exc()}")
        return {"error": "An error occurred while processing the file"}
 
@app.post("/invocations")
async def invocations(request: Request):
    try:
        logger.debug("Received request for invocation")
        file_bytes = await request.body()
        analysis = analyze_text_from_pdf_bytes(file_bytes)
        logger.debug("Invocation analysis completed successfully")
        return {"analysis": analysis}
    except Exception as e:
        logger.error(f"Error during invocation analysis: {e}")
        logger.error(f"Stack trace: {traceback.format_exc()}")
        return {"error": "An error occurred during invocation"}