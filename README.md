# Ticket Analysis UI with Flask + Streamlit + Azure OpenAI

## Overview
This project provides a UI for analyzing IT tickets using an LLM (Azure OpenAI).
- **Backend:** Flask API
- **Frontend:** Streamlit UI
- **LLM:** Azure OpenAI (Chat Completions)
- **Data:** Excel catalog with Assignment Group, Service, Service Offering, Definition

## Setup

### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
