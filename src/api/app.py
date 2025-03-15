from fastapi import FastAPI, HTTPException
import requests
import redis
import os
import subprocess
from pydantic import BaseModel
import httpx  # For async API calls to SSAM

app = FastAPI()

# Initialize Redis for task routing (optional)
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# Cloud GPU API URL (Modify based on provider)
CLOUD_GPU_API_URL = os.getenv("CLOUD_GPU_API_URL", "https://api.runpod.io/v2/inference")

# SSAM Memory API URL
SSAM_API_URL = "http://127.0.0.1:5003/memory/retrieve"
SSAM_STORE_API_URL = "http://127.0.0.1:5003/memory/store"

class Query(BaseModel):
    message: str

def check_local_gpu_usage():
    """Checks GPU usage and decides if the request should be offloaded to the cloud."""
    try:
        output = subprocess.check_output(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"])
        used_memory = int(output.decode().strip().split("\n")[0])  # Get the first GPU's usage
        return used_memory > 7000  # If >7GB used, offload to cloud
    except Exception as e:
        print(f"Error checking GPU usage: {e}")
        return False

@app.get("/")
def home():
    """Root endpoint to verify API is running."""
    return {"message": "Yuna AI CLU is running"}

@app.post("/route")
async def route_request(query: Query):
    """Routes AI requests between local and cloud processing, with memory recall."""

    # Check if similar conversations exist in memory
    async with httpx.AsyncClient() as client:
        response = await client.get(SSAM_API_URL, params={"limit": 5})
        memory = response.json()

    for conversation in memory:
        if query.message.lower() in conversation["user_message"].lower():
            print("Retrieving past memory...")
            return {"response": conversation["ai_response"]}

    # If no memory exists, generate a response
    if check_local_gpu_usage():
        print("GPU overloaded, offloading to cloud...")
        response = requests.post(CLOUD_GPU_API_URL, json={"input": query.message})
        ai_response = response.json()["output"]
    else:
        print("Processing locally on RTX 3060...")
        response = subprocess.run(["ollama", "run", "yuna", query.message], capture_output=True, text=True)
        ai_response = response.stdout.strip()

    # Store the new conversation in memory
    async with httpx.AsyncClient() as client:
        await client.post(SSAM_STORE_API_URL, json={"user_message": query.message, "ai_response": ai_response})

    return {"response": ai_response}
