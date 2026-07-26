# AI Smart Building Optimization System
## Technical Project Report

**Project:** AI Smart Building Optimization System  
**Version:** 1.0.0  
**Type:** Physical AI Proof-of-Concept (PoC)  
**Classification:** Autonomous Closed-Loop Building Energy Management  

---

## Table of Contents

1. Project Overview
2. Hackathon Objective
3. Technical Architecture
4. Requirement 1 — Simulation Engine (EnergyPlus)
5. Requirement 2 — Cognitive Engine (OSS LLM & MCP)
6. Requirement 3 — Closed-Loop Execution Framework
7. Machine Learning Pipeline
8. Frontend Dashboard
9. API Endpoints
10. Tech Stack
11. Simulation Results
12. Energy Savings Evidence
13. How to Run

---

## 1. Project Overview

The AI Smart Building Optimization System is a live, operational Physical AI Proof-of-Concept that automates smart building operations through an autonomous closed-loop control pipeline. Using EnergyPlus as the digital building sandbox and an open-source LLM (Qwen 2.5) as the cognitive brain, the system constructs a dynamic feedback loop where the AI model ingests real-time sensor data from simulation, evaluates variables against comfort and energy targets, and continuously injects forward control actions back into EnergyPlus to prove quantifiable energy and cost savings.

**Key Achievement:** 30.95% energy reduction achieved across 2 closed-loop iterations (6,564 kWh → 4,534 kWh).

---

## 2. Hackathon Objective

> *"You must build a live, operational Physical AI Proof-of-Concept (PoC) that automates smart building operations through an autonomous closed-loop control pipeline. Using EnergyPlus as the digital building sandbox and an open-source LLM (or an MCP server configuration) as the brain, you will construct a dynamic feedback loop. The AI model must ingest real-time sensor data from the simulation, evaluate variables, and continuously inject forward control actions back into EnergyPlus to prove quantifiable energy and cost savings."*

**Status: All requirements implemented and verified.**

---

## 3. Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Vite)                   │
│  Dashboard │ Analytics │ Predictions │ Simulation │ LLM Rec  │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP (port 5173)
┌─────────────────────────▼───────────────────────────────────┐
│                 BACKEND (FastAPI, port 8000)                  │
│  /simulation  /analytics  /ml  /llm  /api/dashboard  /rooms  │
└────────┬──────────────────────────────────────┬─────────────┘
         │                                      │
┌────────▼──────────┐                ┌──────────▼───────────┐
│  EnergyPlus v26   │                │   SQLite Database     │
│  building.idf     │                │   smart_building.db   │
│  weather.epw      │                │   Predictions/Recs    │
│  eplusout.csv     │                └──────────────────────┘
└────────┬──────────┘
         │ eppy + subprocess
┌────────▼──────────┐    ┌─────────────────────────────────┐
│  Closed-Loop      │    │   MCP Server (fastmcp)           │
│  Controller       │◄───│   13 agentic tools               │
│  automation/      │    │   smart_building_mcp/server.py   │
│  controller.py    │    └─────────────────────────────────┘
└────────┬──────────┘
         │
┌────────▼──────────┐    ┌─────────────────────────────────┐
│  OSS LLM (Ollama) │    │   Decision Engine                │
│  Qwen 2.5:1.5b    │    │   decision.py + merger.py        │
│  localhost:11434  │    │   Target evaluation + ECMs       │
└───────────────────┘    └─────────────────────────────────┘
```

---

## 4. Requirement 1 — Simulation Engine (EnergyPlus)

### 4.1 EnergyPlus Integration

| Component | File | Description |
|---|---|---|
| Runner | `energyplus/runner.py` | Subprocess call to `energyplus.exe` with IDF + EPW |
| Simulator | `energyplus/simulator.py` | Orchestrates run + parse |
| Parser | `energyplus/parser.py` | Reads `eplusout.csv` → rows, columns, preview |
| Config | `energyplus/config.py` | Paths to exe, IDF, weather, output dir |

### 4.2 eppy IDF Bridge (Functional Library)

> *"You may use functional libraries (e.g., eppy, PyEnergyPlus, or EMS/BCVTB) to bridge Python with the underlying IDF"*

**Implementation:** `energyplus/idf_editor.py` + `energyplus/idf_reader.py`

- **Primary method:** eppy (`_update_with_eppy`) — loads the IDD file, locates `Clg-SetP-Sch` and `Htg-SetP-Sch` Schedule:Compact objects and writes new setpoint values directly through the eppy API
- **Fallback method:** regex (`_update_with_regex`) — used only if IDD is not found
- **IDF Reader:** `get_idf_summary()`, `get_current_setpoints()`, `list_idf_objects()` — LLM can inspect any IDF object type without touching code

### 4.3 Safety Guards

Every IDF write is safety-clamped **before** execution:

| Parameter | Range | Deadband |
|---|---|---|
| Cooling Setpoint | 22 – 27 °C | ≥ 1°C above heating |
| Heating Setpoint | 16 – 22 °C | — |

- Auto-restore from `building_baseline.idf` on thermostat fatal errors
- `.idf.prev` backup created before every write

### 4.4 Building Model

| Property | Value |
|---|---|
| Building | 5-Zone Air-Cooled Office Building |
| Floor Area | 463.6 m² (5,000 ft²) |
| Floors | 1 story |
| HVAC | VAV with HW Reheat, Electric Chiller |
| Weather | San Francisco TMY3 EPW |
| Simulation Period | Full annual (8,760 hours) |
| EnergyPlus Version | 26.1.0 |

---

## 5. Requirement 2 — Cognitive Engine (OSS LLM & MCP)

### 5.1 Open-Source LLM

| Property | Value |
|---|---|
| LLM Runtime | Ollama (self-hosted, local) |
| Model | Qwen 2.5:1.5b |
| Endpoint | `http://localhost:11434/api/generate` |
| Mode | Non-streaming, JSON-constrained output |
| Timeout | 120 seconds |
| Fallback | Rule-based `recommend_setpoints()` if LLM fails |

Configuration via `.env`:
```
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen2.5:1.5b
```

### 5.2 MCP Server

**File:** `smart_building_mcp/server.py`  
**Framework:** fastmcp 2.10.1  
**Run:** `python -m smart_building_mcp.server`

#### 13 Registered Tools

| # | Tool | Requirement | Description |
|---|---|---|---|
| 1 | `run_simulation` | Req 1 | Run full EnergyPlus simulation |
| 2 | `parse_simulation_output` | Req 1+2 | Parse eplusout.csv without human modification |
| 3 | `inspect_idf` | Req 1+2 | eppy IDF summary (zones, objects, setpoints) |
| 4 | `get_idf_setpoints` | Req 1 | Read current setpoints via eppy |
| 5 | `list_idf_objects` | Req 2 | Inspect any IDF object type |
| 6 | `extract_energyplus_errors` | Req 2 | Parse eplusout.err warnings/severe/fatal |
| 7 | `stream_building_metrics` | Req 3 | Zone temps, IAQ, PMV, PPD, energy |
| 8 | `evaluate_against_targets` | Req 3 | PMV/comfort/peak demand/carbon evaluation |
| 9 | `inject_setpoints` | Req 3 | Forward injection into active IDF |
| 10 | `run_closed_loop_optimisation` | Req 3 | Full 4-step closed-loop execution |
| 11 | `predict_energy_comfort` | ML | Random Forest energy + comfort prediction |
| 12 | `get_building_analytics` | DB | Aggregated prediction analytics |
| 13 | `get_llm_recommendation` | LLM | Free-text LLM recommendation |

---
