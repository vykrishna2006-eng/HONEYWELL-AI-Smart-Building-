# System Architecture

# AI Smart Building Optimization System

## Overview

The AI Smart Building Optimization System is an intelligent building management platform designed to reduce energy consumption while maintaining occupant thermal comfort.

The system integrates:

- Machine Learning for energy prediction
- EnergyPlus for building simulation
- Google Gemini LLM for intelligent recommendations
- FastAPI for backend services
- React for visualization
- FastMCP for AI tool calling

The complete workflow forms a closed-loop optimization system where simulation, prediction, and AI recommendations continuously improve building operation.

---

# High-Level Architecture

```text
                        User
                          │
                          ▼
                 React Dashboard
                          │
                          ▼
                   FastAPI Backend
                          │
      ┌───────────────────┼────────────────────┐
      │                   │                    │
      ▼                   ▼                    ▼
 Machine Learning     EnergyPlus         Gemini LLM
 Energy Prediction    Simulation     AI Recommendation
      │                   │                    │
      └───────────────────┼────────────────────┘
                          │
                          ▼
                  SQLite Database
                          │
                          ▼
                    FastMCP Server
                          │
                          ▼
                    MCP Inspector
```

---

# Detailed System Architecture

```text
                      +----------------------+
                      |     React Frontend   |
                      | Dashboard & Charts   |
                      +----------+-----------+
                                 |
                                 |
                                 ▼
                  +-------------------------------+
                  |        FastAPI Backend        |
                  | REST API + Business Logic     |
                  +---------------+---------------+
                                  |
       --------------------------------------------------------
       |                     |                     |           |
       ▼                     ▼                     ▼           ▼
+---------------+   +----------------+   +----------------+  +-----------+
| ML Prediction |   | EnergyPlus     |   | Gemini AI      |  | Database  |
| Scikit-Learn  |   | Simulation     |   | Recommendations|  | SQLite    |
+---------------+   +----------------+   +----------------+  +-----------+
       |                     |                     |
       -----------------------+---------------------
                               |
                               ▼
                     +----------------------+
                     | FastMCP Server       |
                     | AI Tool Interface    |
                     +----------+-----------+
                                |
                                ▼
                        MCP Inspector
```

---

# Component Description

## 1. React Frontend

Responsibilities

- Interactive dashboard
- Sensor visualization
- Energy charts
- Simulation results
- Recommendation display

Technologies

- React
- Vite
- JavaScript
- CSS

---

## 2. FastAPI Backend

Acts as the central controller.

Responsibilities

- API endpoints
- Data validation
- ML invocation
- EnergyPlus execution
- Gemini communication
- Database management

Technologies

- FastAPI
- SQLAlchemy
- Pydantic

---

## 3. Machine Learning Module

Predicts future building energy consumption.

Input

- Indoor Temperature
- Outdoor Temperature
- Occupancy
- HVAC Settings
- Lighting Level
- CO₂
- Weather
- Time Features

Output

- Predicted Energy Consumption

Algorithms

- Scikit-Learn Regression Model

---

## 4. EnergyPlus Simulation

Provides high-fidelity building simulation.

Input

- IDF File
- Weather File
- Building Parameters

Output

- Electricity Consumption
- HVAC Load
- Cooling Load
- Heating Load
- Indoor Comfort

---

## 5. Gemini AI

Generates intelligent building optimization strategies.

Receives

- ML Prediction
- Simulation Results
- Current Sensor Data

Returns

- HVAC Recommendations
- Lighting Optimization
- Energy Saving Suggestions
- Comfort Improvements

---

## 6. Database

Stores

- Sensor Data
- Predictions
- Simulation Results
- Recommendations
- Analytics

Technology

SQLite

---

## 7. FastMCP

Provides AI Tool Calling.

Available Tools

- dashboard
- predict_energy
- run_simulation
- ai_recommendation

Supports

- MCP Inspector
- AI Clients

---

# Data Flow

```text
Sensors
   │
   ▼
Database
   │
   ▼
FastAPI
   │
   ├────────► ML Prediction
   │
   ├────────► EnergyPlus
   │
   ├────────► Gemini
   │
   ▼
Analytics
   │
   ▼
React Dashboard
```

---

# AI Closed Loop

```text
Building Sensors
        │
        ▼
Machine Learning
        │
        ▼
Energy Prediction
        │
        ▼
EnergyPlus Simulation
        │
        ▼
Gemini AI
        │
        ▼
Optimization Decision
        │
        ▼
Updated Building Parameters
        │
        ▼
Next Simulation
```

This feedback loop continuously improves building efficiency.

---

# Prompt Engineering Strategy

The Gemini LLM receives structured prompts containing:

- Current building conditions
- Machine learning prediction
- EnergyPlus simulation outputs
- Occupancy information
- Environmental conditions

The prompt instructs Gemini to:

- Reduce energy usage
- Maintain thermal comfort
- Avoid unnecessary HVAC operation
- Provide concise recommendations

---

# Prompt Latency Management

To minimize LLM response time:

- Only essential simulation outputs are included.
- Large EnergyPlus logs are summarized before being sent.
- Structured prompts reduce unnecessary token usage.
- Cached data is reused where possible.

---

# Handling Large Simulation Logs

EnergyPlus generates extensive simulation logs.

Instead of sending the complete output to the LLM:

1. Parse the simulation output.
2. Extract key performance indicators.
3. Remove unnecessary diagnostic logs.
4. Send only summarized metrics.

This approach significantly reduces latency and token consumption.

---

# Security Considerations

- API keys are stored in environment variables.
- Sensitive configuration is excluded from GitHub.
- Input validation is performed using Pydantic.
- SQLAlchemy prevents SQL injection.
- Backend and frontend are separated by REST APIs.

---

# Scalability

The architecture supports future extensions including:

- PostgreSQL
- Docker deployment
- Cloud deployment
- IoT sensors
- Multiple buildings
- Reinforcement Learning
- Real-time monitoring
- Edge AI

---

# Technologies Used

| Layer | Technology |
|---------|------------|
| Frontend | React |
| Backend | FastAPI |
| Machine Learning | Scikit-Learn |
| Simulation | EnergyPlus |
| LLM | Google Gemini |
| AI Tools | FastMCP |
| Database | SQLite |
| Language | Python |
| Visualization | React Charts |

---

# Conclusion

The proposed architecture combines simulation, machine learning, and generative AI into a unified intelligent building optimization framework.

The integration of EnergyPlus, Gemini, FastAPI, and MCP enables an automated decision-making workflow capable of improving energy efficiency while preserving occupant comfort.