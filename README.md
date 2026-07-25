# 🏢 AI Smart Building Optimization System

An AI-powered Smart Building Optimization System that combines **EnergyPlus**, **Machine Learning**, **LLMs (Gemini)**, and **Model Context Protocol (MCP)** to optimize building energy consumption while maintaining occupant comfort.

---

# 📌 Overview

Buildings consume a significant portion of global electricity. Traditional Building Management Systems (BMS) generally rely on static rules and manual configuration, leading to unnecessary energy consumption.

This project introduces an AI-driven optimization framework that:

- Predicts energy consumption using Machine Learning
- Simulates building performance using EnergyPlus
- Generates intelligent optimization recommendations using Google's Gemini LLM
- Supports AI tool-calling through Model Context Protocol (MCP)
- Visualizes energy analytics through an interactive dashboard

The system continuously analyses building sensor data and recommends optimized HVAC and lighting strategies to reduce energy usage without compromising thermal comfort.

---

# 🚀 Features

## Energy Prediction

- Machine Learning based energy consumption prediction
- Real-time prediction from sensor inputs
- Feature engineering for building analytics

---

## EnergyPlus Simulation

- Executes EnergyPlus simulations
- Reads simulation outputs
- Compares baseline vs optimized building performance

---

## AI Recommendation Engine

Powered by **Google Gemini**

Generates recommendations such as:

- HVAC optimization
- Lighting optimization
- Occupancy-based control
- Temperature adjustments
- Comfort improvement strategies

---

## MCP (Model Context Protocol)

The project exposes AI tools through FastMCP.

Available tools:

- dashboard
- predict_energy
- run_simulation
- ai_recommendation

These tools can be accessed from:

- MCP Inspector
- MCP-compatible AI clients

---

## Interactive Dashboard

Displays:

- Total Energy Consumption
- HVAC Energy
- Lighting Energy
- Comfort Score
- CO₂ Levels
- Indoor Temperature
- Energy Savings
- Simulation Results

---

# 🏗 System Architecture

```
                  React Dashboard
                         │
                         ▼
                  FastAPI Backend
                         │
     ┌───────────────────┼────────────────────┐
     ▼                   ▼                    ▼
Machine Learning     EnergyPlus        Gemini LLM
 Prediction          Simulation      Recommendations
     │                   │                    │
     └───────────────────┼────────────────────┘
                         │
                    SQLite Database
                         │
                         ▼
                    FastMCP Server
                         │
                         ▼
                  MCP Inspector / AI Client
```

---

# ⚙ Technology Stack

## Backend

- FastAPI
- Python
- SQLAlchemy
- SQLite
- Pydantic

---

## Frontend

- React
- Vite
- JavaScript
- CSS

---

## Artificial Intelligence

- Google Gemini API
- Prompt Engineering

---

## Machine Learning

- Scikit-Learn
- Pandas
- NumPy
- Joblib

---

## Simulation

- EnergyPlus

---

## AI Integration

- FastMCP
- MCP Inspector

---

## Database

- SQLite

---

# 📂 Project Structure

```
AI-Smart-Building/

│
├── backend/
├── frontend/
├── smart_building_mcp/
├── database/
├── ml/
├── energyplus/
├── reports/
├── datasets/
├── sensors/
├── dashboard/
├── architecture/
├── docs/
├── requirements.txt
├── README.md
└── main.py
```

---

# 📊 Machine Learning Features

Numerical Features

- Indoor Temperature
- Outdoor Temperature
- Humidity
- CO₂
- Occupancy
- HVAC Setpoint
- Lighting Level
- Equipment Load
- Solar Radiation
- Wind Speed
- Electricity Price
- Renewable Generation
- Floor
- Hour
- Day
- Month
- Year
- Day Of Week
- Week Of Year
- Quarter
- Weekend Flag

Categorical Features

- Building ID
- Zone
- Room ID
- Day Type
- Season
- HVAC Status
- HVAC Mode

---

# 🤖 AI Workflow

```
Sensor Data
      │
      ▼
Feature Engineering
      │
      ▼
ML Energy Prediction
      │
      ▼
EnergyPlus Simulation
      │
      ▼
Gemini AI Analysis
      │
      ▼
Optimization Recommendation
      │
      ▼
Dashboard
```

---

# 🔄 MCP Workflow

```
User

↓

MCP Client

↓

FastMCP Server

↓

Backend Services

↓

Machine Learning

↓

EnergyPlus

↓

Gemini

↓

Response
```

---

# 📈 Dashboard Analytics

The dashboard provides:

- Building Overview
- Energy Consumption
- HVAC Usage
- Lighting Usage
- Indoor Temperature
- CO₂ Monitoring
- Occupancy Analysis
- Energy Savings
- AI Recommendations
- Simulation Results

---

# 📉 Energy Optimization Strategy

The optimization engine analyses:

- Occupancy
- Weather Conditions
- HVAC Settings
- Indoor Temperature
- Outdoor Temperature
- Renewable Energy Availability
- Electricity Pricing

It then recommends optimized operating conditions to minimize electricity consumption while maintaining occupant comfort.

---

# 🧠 Prompt Engineering Strategy

The Gemini LLM receives:

- Current sensor readings
- Machine Learning prediction
- Simulation results
- Building conditions

It generates:

- Energy-saving recommendations
- HVAC optimisation strategies
- Lighting optimisation
- Comfort improvement suggestions

---

# 🛠 Installation

## Clone Repository

```bash
git clone https://github.com/<YOUR_USERNAME>/AI-Smart-Building.git

cd AI-Smart-Building
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file.

Example:

```env
GEMINI_API_KEY=YOUR_API_KEY
DATABASE_URL=sqlite:///database.db
```

---

# ▶ Running the Backend

```bash
uvicorn backend.main:app --reload
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

# ▶ Running the Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# ▶ Running MCP Server

```bash
python -m smart_building_mcp.server
```

---

# ▶ Running MCP Inspector

```bash
npx @modelcontextprotocol/inspector
```

Configure

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

---

# 📸 Screenshots

Add screenshots here.

- Dashboard
- Prediction
- EnergyPlus Simulation
- Gemini Recommendation
- MCP Inspector

---

# 📈 Results

The proposed system demonstrates:

- Reduced building energy consumption
- Intelligent HVAC optimisation
- Improved thermal comfort
- AI-assisted decision making
- Automated simulation analysis

---

# 🔮 Future Improvements

- Docker Deployment
- Cloud Deployment
- PostgreSQL
- Real-time IoT Sensor Integration
- WebSocket Live Dashboard
- Multi-building Support
- Reinforcement Learning
- Edge AI Deployment

---

# 👨‍💻 Authors

**Yaswanth Krishna**

AI Smart Building Optimization System

---

# 📄 License

This project is developed for educational and research purposes.

---

# 🙏 Acknowledgements

- Honeywell
- EnergyPlus
- Google Gemini
- FastAPI
- React
- FastMCP
- Model Context Protocol (MCP)