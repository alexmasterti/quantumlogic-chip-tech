from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
from .service import compute_quantum_score, estimate_amplitude, protect_payload, restore_payload

app = FastAPI(title="QuantumLogic Chip Technology API", version="0.1.0")

class ScoreReq(BaseModel):
    bits: int
    target: int
class AmpReq(BaseModel):
    bits: int
    target: int
    shots: int = 2000
class ProtectReq(BaseModel):
    payload: Dict[str, Any]
class RestoreReq(BaseModel):
    ciphertext_hex: str

@app.post("/score")
def score(req: ScoreReq):
    return {"score": compute_quantum_score(req.bits, req.target)}
@app.post("/amplitude")
def amplitude(req: AmpReq):
    return {"estimated_probability": estimate_amplitude(req.bits, req.target, req.shots), "shots": req.shots}
@app.post("/protect")
def protect(req: ProtectReq):
    return protect_payload(req.payload)
@app.post("/restore")
def restore(req: RestoreReq):
    return {"restored": restore_payload(req.ciphertext_hex)}
