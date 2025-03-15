import sqlite3
import chromadb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# SQLite Database Path
DB_PATH = "data/database/yuna_memory.db"

# Initialize ChromaDB for Vector Storage
chroma_client = chromadb.PersistentClient(path="src/vector_db/")

# Define Chat Data Model
class ChatEntry(BaseModel):
    user_message: str
    ai_response: str

# Ensure DB Schema Exists
def init_db():
    """Create database and table if not exists."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            ai_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.post("/memory/store")
async def store_conversation(chat: ChatEntry):
    """Stores conversation history."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO conversations (user_message, ai_response) VALUES (?, ?)",
                   (chat.user_message, chat.ai_response))
    conn.commit()
    conn.close()
    return {"message": "Stored successfully"}

@app.get("/memory/retrieve")
async def get_recent_conversations(limit: int = 10):
    """Retrieves recent chat history."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_message, ai_response, timestamp FROM conversations ORDER BY timestamp DESC LIMIT ?", (limit,))
    conversations = [{"user_message": row[0], "ai_response": row[1], "timestamp": row[2]} for row in cursor.fetchall()]
    conn.close()
    return conversations
