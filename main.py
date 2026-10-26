from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="Aura Enforcer API", version="0.1")

# Simple in-memory "database" for the demo
state = {"scanning": "Notepad.exe", "fixes": 12, "mode": "IDLE", "persona": "voyager"}

PERSONAS = {
    "voyager": {"label": "The Voyager (Color Blind)", "accent": "#3b82f6"},
    "beacon": {"label": "The Beacon (Low Vision)", "accent": "#fbbf24"},
}


class EnforceRequest(BaseModel):
    persona: str = "voyager"
    fixes: int = 12  # number of elements the front end tagged


@app.get("/api/personas")
def personas():
    return PERSONAS


@app.get("/api/status")
def status():
    return state


@app.post("/api/enforce")
def enforce(req: EnforceRequest):
    if req.persona not in PERSONAS:
        raise HTTPException(status_code=400, detail="Unknown persona")
    state.update(mode="ENFORCING", persona=req.persona, fixes=req.fixes)
    return state


@app.post("/api/stop")
def stop():
    state["mode"] = "IDLE"
    return state


@app.get("/")
def index():
    return FileResponse("static/index.html")


app.mount("/static", StaticFiles(directory="static"), name="static")
