# YunaGPT-Render

## Overview
YunaGPT-Render is an AI-powered assistant that automates task management, document summarization, and project tracking using OpenAI, Dropbox, and ChromaDB. This service runs on FastAPI and is deployed on Render for seamless cloud-based automation.

## Features
### ✅ **Dropbox Integration**
- Reads and writes files to Dropbox.
- Automatically updates `projects.md` and `tasks.txt`.
- Saves AI-generated summaries to Dropbox.

### ✅ **Task Management**
- Stores and retrieves tasks from Dropbox.
- Checks for upcoming tasks due within 3 days.
- Appends new tasks instead of overwriting files.

### ✅ **AI-Powered Summarization & Memory Recall**
- Fetches latest notes and projects from Dropbox.
- Uses OpenAI to summarize and tag documents.
- Stores summaries and memories in ChromaDB for easy retrieval.

### ✅ **Scheduled Reports**
- Generates and saves a `daily_report.md` to Dropbox.
- Includes latest Dropbox updates and upcoming tasks.

## API Endpoints
### **📂 Dropbox File Management**
#### Fetch Latest Notes:
```sh
curl "https://yunagpt-render.onrender.com/fetch_latest_notes_with_summary_and_tags"
```
#### Write a New File to Dropbox:
```sh
curl -X POST "https://yunagpt-render.onrender.com/write_to_dropbox" \
     -H "Content-Type: application/json" \
     -d '{"file_name": "tasks.txt", "content": "Complete final edits on YunaGPT."}'
```
#### Update an Existing File in Dropbox:
```sh
curl -X POST "https://yunagpt-render.onrender.com/update_dropbox_file" \
     -H "Content-Type: application/json" \
     -d '{"file_name": "tasks.txt", "update_content": "Added another task: Review AI model improvements."}'
```

### **📋 Task Management**
#### Check Upcoming Tasks:
```sh
curl "https://yunagpt-render.onrender.com/check_upcoming_tasks"
```
#### Auto-Delete Old Tasks & Projects:
```sh
curl -X POST "https://yunagpt-render.onrender.com/auto_delete_old_entries"
```

### **📊 Reports & Summaries**
#### Generate a Scheduled Summary:
```sh
curl -X POST "https://yunagpt-render.onrender.com/generate_scheduled_summary"
```

## Deployment
### **🚀 Deploy on Render**
1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-repo/YunaGPT-Render.git
   cd YunaGPT-Render
   ```
2. **Set up environment variables:**
   - `OPENAI_API_KEY`
   - `GITHUB_ACCESS_TOKEN`
   - `DROPBOX_ACCESS_TOKEN`
3. **Deploy to Render:**
   - Create a new **Web Service** on [Render](https://render.com/)
   - Use `Python 3.9+` as the runtime
   - Deploy from GitHub
   - Set the environment variables in the **Render Dashboard**
4. **Start the service:**
   ```sh
   uvicorn yuna:app --host 0.0.0.0 --port 8000 --reload
   ```

## Future Enhancements
- **Automated Scheduling**: Run reports and clean up old tasks on a schedule.
- **Slack/Telegram Integration**: Receive task reminders and summaries via messaging apps.
- **Voice Commands**: Interact with Yuna using voice commands.

## License
This project is licensed under the MIT License.

## Contributors
- **[Keith Alexander]** - Developer
- **Yuna AI** - Automation & AI Assistant

---

