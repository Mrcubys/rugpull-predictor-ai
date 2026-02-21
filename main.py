from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Rug Pull Predictor AI")

class TokenData(BaseModel):
    token_name: str
    liquidity: float
    holders: int
    dev_wallet_percent: float
    locked_liquidity: bool

def rugpull_score(data):
    score = 0
    if data.liquidity < 5000: score += 30
    if data.holders < 100: score += 20
    if data.dev_wallet_percent > 20: score += 30
    if not data.locked_liquidity: score += 20
    
    risk = "LOW"
    if score > 30: risk = "MEDIUM"
    if score > 60: risk = "HIGH"
    return score, risk

@app.get("/", response_class=HTMLResponse)
def home():
    return "<h1>Rug Pull Predictor AI Running</h1>"

@app.post("/predict")
def predict(data: TokenData):
    score, risk = rugpull_score(data)
    return {"token": data.token_name, "score": score, "risk": risk}
