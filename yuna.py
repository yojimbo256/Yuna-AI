import os
import json
from fastapi import FastAPI
from pydantic import BaseModel
import openai
import chromadb
from chromadb.utils import embedding_functions
from github import Github
import requests
import dropbox
from datetime import datetime, timedelta

# Load API Keys from Render Environment Variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")
PORT = int(os.getenv("PORT", 8000))  # Default to 8000 if not set

# Initialize OpenAI Client
openai.api_key = OPENAI_API_KEY 

# Initialize ChromaDB for Persistent Memory
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("yuna_knowledge")

# Corrected Dropbox file path
DROPBOX_FOLDER_PATH = "/Apps/YunaGPT-Storage/yuna-docs/"

# Define Pydantic models for JSON requests
class DropboxRequest(BaseModel):
    file_name: str
    content: str

class UpdateDropboxRequest(BaseModel):
    file_name: str
    update_content: str

# Define write_to_dropbox to ensure it's available
def write_to_dropbox(file_name: str, content: str):
    """Writes or updates a file in Dropbox."""
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        file_path = f"{DROPBOX_FOLDER_PATH}{file_name}"
        dbx.files_upload(content.encode("utf-8"), file_path, mode=dropbox.files.WriteMode("overwrite"))
        return {"message": f"Successfully written to {file_name} in Dropbox."}
    except Exception as e:
        print(f"Dropbox Write Error: {e}")
        return {"error": str(e)}

# Fetch latest notes from Dropbox, prioritize projects.md
def fetch_latest_notes_with_summary_and_tags():
    """Fetches `projects.md` from Dropbox if it exists, otherwise fetches the most recent text file."""
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        files = dbx.files_list_folder(DROPBOX_FOLDER_PATH).entries
        text_files = [file.name for file in files if file.name.endswith(".md") or file.name.endswith(".txt")]
        
        if "projects.md" in text_files:
            latest_file = "projects.md"
        elif text_files:
            latest_file = sorted(text_files, reverse=True)[0]
        else:
            return {"error": "No text files found in Dropbox."}
        
        _, response = dbx.files_download(f"{DROPBOX_FOLDER_PATH}{latest_file}")
        content = response.content.decode("utf-8")
        
        return {"file": latest_file, "content": content}
    except Exception as e:
        print(f"Dropbox API Error: {e}")
        return {"error": str(e)}

# Retrieve upcoming tasks
def check_upcoming_tasks():
    """Retrieves tasks due within the next 3 days."""
    upcoming_tasks = []
    
    try:
        results = collection.query(query_texts=["*"], n_results=100)
    except Exception as e:
        print(f"ChromaDB Query Error: {e}")
        return {"error": "Failed to retrieve tasks from database."}
    
    if not results or "metadatas" not in results or not results["metadatas"]:
        print("No tasks found in the database.")
        return {"upcoming_tasks": "No tasks found in the database."}
    
    for task in results["metadatas"]:
        if "due_date" in task and isinstance(task["due_date"], str):
            try:
                due_date = datetime.strptime(task["due_date"], "%Y-%m-%d")
                if due_date <= datetime.now() + timedelta(days=3):
                    upcoming_tasks.append(task)
            except ValueError:
                print(f"Invalid date format in task: {task['due_date']}")
                continue  # Skip invalid dates
    
    return {"upcoming_tasks": upcoming_tasks if upcoming_tasks else "No upcoming tasks found."}

# Now define generate_scheduled_summary AFTER write_to_dropbox and fetch_latest_notes_with_summary_and_tags
def generate_scheduled_summary():
    """Generates a daily report of Dropbox updates and upcoming tasks."""
    try:
        notes_response = fetch_latest_notes_with_summary_and_tags()
        tasks_response = check_upcoming_tasks()
        
        summary_content = f"### Daily Report ({datetime.now().strftime('%Y-%m-%d')})\n\n"
        summary_content += "#### Dropbox Updates\n" + json.dumps(notes_response, indent=4) + "\n\n"
        summary_content += "#### Upcoming Tasks\n" + json.dumps(tasks_response, indent=4) + "\n"
        
        write_to_dropbox("daily_report.md", summary_content)  # Now correctly defined
        return {"message": "Daily report generated and saved to Dropbox."}
    except Exception as e:
        print(f"Scheduled Summary Error: {e}")
        return {"error": str(e)}

# FastAPI Web App
app = FastAPI()

@app.get("/fetch_latest_notes_with_summary_and_tags")
def get_latest_notes_with_summary_and_tags():
    """Fetches, prioritizes projects.md, and retrieves Dropbox document."""
    return fetch_latest_notes_with_summary_and_tags()

@app.post("/write_to_dropbox")
def save_to_dropbox(request: DropboxRequest):
    """Writes or updates a file in Dropbox."""
    return write_to_dropbox(request.file_name, request.content)

@app.post("/update_dropbox_file")
def append_to_dropbox(request: UpdateDropboxRequest):
    """Appends updates to an existing Dropbox file."""
    return update_dropbox_file(request.file_name, request.update_content)

@app.post("/check_upcoming_tasks")
def get_upcoming_tasks():
    """Lists tasks due within the next 3 days."""
    return check_upcoming_tasks()

@app.post("/generate_scheduled_summary")
def run_scheduled_summary():
    """Runs the scheduled summary and task reminder process."""
    return generate_scheduled_summary()

@app.on_event("startup")
async def startup_event():
    print("\U0001F680 Yuna API has started successfully on Render!")

# Run FastAPI with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT, reload=True)
