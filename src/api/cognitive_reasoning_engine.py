from fastapi import FastAPI, HTTPException
import requests
import subprocess
from pydantic import BaseModel

app = FastAPI()

# Define API URLs
SSAM_API_URL = "http://127.0.0.1:5003/memory/store"

# Define request model
class Query(BaseModel):
    message: str

def call_yuna_llm(message: str) -> str:
    """
    Calls Yuna's LLM (Mistral 7B) to generate reasoning responses.
    """
    try:
        response = subprocess.run(["ollama", "run", "yuna", message], capture_output=True, text=True, timeout=30)
        if response.returncode != 0:
            raise RuntimeError(f"LLM error: {response.stderr}")
        return response.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Error: LLM request timed out."
    except Exception as e:
        print(f"Error calling Yuna's LLM: {e}")
        return "Error processing request."

@app.post("/cre/process")
def process_reasoning(query: Query):
    """
    Processes reasoning request using Yuna's LLM and stores the reasoning result in memory.
    """
    print(f"[CRE] Processing query: {query.message}")
    
    # Call Yuna's LLM for reasoning
    response_text = call_yuna_llm(query.message)
    print(f"[CRE] LLM Response: {response_text}")
    
    # Store reasoning result in SSAM
    ssam_payload = {"user_message": query.message, "ai_response": response_text}
    try:
        response = requests.post(SSAM_API_URL, json=ssam_payload)
        response.raise_for_status()  # Raise exception for failed requests
        print("[CRE] Successfully stored response in SSAM.")
    except requests.RequestException as e:
        print(f"[CRE] Error storing memory in SSAM: {e}")
    
    return {"response": response_text}
