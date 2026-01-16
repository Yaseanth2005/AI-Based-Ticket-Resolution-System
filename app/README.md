# AI Powered Knowledge Engine for Support Tickets

This project is a complete AI-powered support ticket system. It allows users to submit tickets, which are then analyzed by a local LLM (Ollama running `phi3:mini`) to categorize the issue and suggest a resolution.

## 📁 Project Structure

```
ai_support_engine/
├── venv/                   # Python Virtual Environment
├── app.py                  # Streamlit Frontend UI
├── database.py            # Database setup and connection
├── llm_engine.py          # AI logic handling Ollama communication
├── ticket_service.py      # Business logic service layer
├── requirements.txt       # Python dependencies
└── support_tickets.db     # SQLite database (auto-created)
```

## 🚀 How to Run the App from Scratch

### Prerequisites
1. **Python 3.10+** installed.
2. **Ollama** installed and running. 
   - Download from: [ollama.com](https://ollama.com)
   - Ensure the Ollama app is running in the background (tray icon visible).
# AI-Powered IT Support Ticket System

## Overview
A smart ticketing system that automatically categorizes issues, suggests resolutions using an LLM (Ollama), and supports **Authentication** and **RAG (Retrieval Augmented Generation)** for context-aware answers.

## Features
- **Auto-Categorization**: Validates and tags tickets (Technical, Billing, etc.).
- **AI Resolution**: Provides step-by-step troubleshooting steps.
- **Authentication**: Secure login with Role-Based Access Control (Admin/User).
- **RAG Support**: Upload PDFs to `data/raw` for the AI to reference company policies.
- **Dashboard**: Admin view for tracking incidents.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install & Run Ollama**:
   - Download [Ollama](https://ollama.ai).
   - Pull the model: `ollama pull tinyllama`

3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## Authentication
- **Default Admin**: `admin` / `admin123`
- **Default User**: `testuser` / `user123`

## RAG (Knowledge Base)
To use custom documents (PDF/Text):
1. Place files in `data/raw`.
2. Run the ingestion script:
   ```bash
   python ingest_data.py
   ```
3. Restart the application to load the new index.

*Note: On the first run, the system will automatically:*
1. *Create the SQLite database.*
2. *Pull the `phi3:mini` model via Ollama (this calls `ollama pull phi3:mini`, so it may take a few minutes if not already downloaded).*

## 💡 Usage

1. **Submit Ticket**: 
   - Go to "Submit New Ticket".
   - Enter a title (e.g., "VPN Connection Failed").
   - Enter a description.
   - Click Submit.
   - The AI will think (spinner will show) and then save the resolution.

2. **View Tickets**:
   - Go to "View Tickets".
   - Use the sidebar dropdown to select a specific ticket.
   - See the AI's Category and Resolution Suggestion.

## 🔧 Common Errors & Fixes

**Error: Connection Refused / LLM Error**
- **Cause**: Ollama is not running.
- **Fix**: Open the Ollama application. Run `ollama serve` in a separate terminal if needed.

**Error: Model not found**
- **Cause**: The `phi3:mini` model failed to pull automatically.
- **Fix**: Manually run `ollama pull phi3:mini` in your terminal.

## 📝 Sample Input

**Title**: `Unable to reset password`
**Description**: `I tried clicking the 'Forgot Password' link on the portal, but I never received the reset email. Checked spam folder too.`

**Expected AI Response**:
- **Category**: `Account`
- **Resolution**: `Possible issue with email delivery service etc...`
