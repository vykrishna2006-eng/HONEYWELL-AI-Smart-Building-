# Installation Guide

This document explains how to install and run the **AI Smart Building Optimization System** on a local machine.

---

# System Requirements

## Operating System

- Windows 10/11 (Recommended)
- Ubuntu 22.04+
- macOS (Supported)

---

# Software Requirements

Install the following software before running the project.

| Software | Version |
|-----------|---------|
| Python | 3.11+ |
| Node.js | 18+ |
| npm | Latest |
| Git | Latest |
| EnergyPlus | 24.x (or compatible version) |

---

# Clone the Repository

```bash
git clone https://github.com/<YOUR_USERNAME>/AI-Smart-Building.git

cd AI-Smart-Building
```

---

# Create a Python Virtual Environment

Windows

```bash
python -m venv .venv
```

Activate

Command Prompt

```bash
.venv\Scripts\activate
```

PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

Linux / macOS

```bash
source .venv/bin/activate
```

---

# Install Python Dependencies

```bash
pip install -r requirements.txt
```

Verify installation

```bash
pip list
```

---

# Install Frontend Dependencies

Navigate to the frontend folder.

```bash
cd frontend
```

Install packages.

```bash
npm install
```

Return to the project root.

```bash
cd ..
```

---

# Install EnergyPlus

Download EnergyPlus from the official website.

https://energyplus.net/downloads

Install EnergyPlus using the default installation settings.

After installation, verify that:

- EnergyPlus executable is available
- Weather (.epw) files are present
- Building (.idf) files are available in the project

---

# Configure Environment Variables

Create a file named:

```
.env
```

Example:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
DATABASE_URL=sqlite:///database.db
```

Replace `YOUR_GEMINI_API_KEY` with your Google Gemini API key.

---

# Running the Backend

Start the FastAPI server.

```bash
uvicorn backend.main:app --reload
```

Backend API

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

---

# Running the Frontend

Open another terminal.

Navigate to the frontend directory.

```bash
cd frontend
```

Start the React development server.

```bash
npm run dev
```

Frontend URL

```
http://localhost:5173
```

---

# Running the MCP Server

Open another terminal.

Run:

```bash
python -m smart_building_mcp.server
```

If successful, you should see a message similar to:

```
Starting MCP server 'AI Smart Building MCP'
```

---

# Running MCP Inspector

Launch the MCP Inspector.

```bash
npx @modelcontextprotocol/inspector
```

Configure the following:

Transport

```
STDIO
```

Command

```
python
```

Arguments

```
-m
smart_building_mcp.server
```

Working Directory

```
<Project Root>
```

Click **Connect**.

Available tools should include:

- dashboard
- predict_energy
- run_simulation
- ai_recommendation

---

# Project Startup Order

Start the application in the following order:

1. Backend (FastAPI)
2. Frontend (React)
3. MCP Server
4. MCP Inspector (Optional)

---

# Verifying Installation

Open the frontend.

Verify that the following features work correctly:

- Dashboard loads successfully
- Energy prediction works
- EnergyPlus simulation runs
- AI recommendation is generated
- MCP tools respond correctly

---

# Troubleshooting

## Python packages not found

Run:

```bash
pip install -r requirements.txt
```

---

## Frontend dependencies missing

Run:

```bash
cd frontend
npm install
```

---

## EnergyPlus not detected

Verify that:

- EnergyPlus is installed
- Correct installation path is configured
- Required `.idf` and `.epw` files are present

---

## Gemini API errors

Verify:

- `.env` file exists
- `GEMINI_API_KEY` is valid
- Internet connection is available

---

## MCP Server not starting

Check that:

- Python virtual environment is activated
- FastMCP is installed
- The command below runs successfully:

```bash
python -m smart_building_mcp.server
```

---

## API Documentation

FastAPI automatically generates API documentation.

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

# Project Structure

```
AI-Smart-Building/

├── backend/
├── frontend/
├── smart_building_mcp/
├── database/
├── energyplus/
├── ml/
├── reports/
├── datasets/
├── requirements.txt
├── README.md
├── INSTALLATION.md
└── .env
```

---

# Successfully Installed

The installation is complete when:

- Backend is running
- Frontend is accessible
- Dashboard loads correctly
- Energy prediction works
- Simulation executes successfully
- Gemini recommendations are generated
- MCP Inspector connects and all tools execute successfully