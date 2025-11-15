from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import EstimateRequest, EstimateResponse
from services.estimator import calculate_estimate

app = FastAPI(title="RoadSafeCost AI - Stage 1 Demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "National Road Safety Hackathon 2025 - PS 1.1",
        "project": "RoadSafeCost AI - Estimator Tool for Intervention",
        "status": "Stage 1 Demo"
    }

@app.post("/api/estimate", response_model=EstimateResponse)
def create_estimate(request: EstimateRequest):
    try:
        estimates = []
        grand_total = 0.0
        
        for intervention in request.interventions:
            est = calculate_estimate(intervention)
            estimates.append(est)
            grand_total += est.total_material_cost
        
        return EstimateResponse(
            road_id=request.road_id,
            estimates=estimates,
            grand_total=round(grand_total, 2)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/interventions")
def list_interventions():
    import sqlite3
    conn = sqlite3.connect('roadsafe.db')
    c = conn.cursor()
    c.execute("SELECT name, category, description FROM interventions")
    rows = c.fetchall()
    conn.close()
    return [{"name": r[0], "category": r[1], "description": r[2]} for r in rows]
