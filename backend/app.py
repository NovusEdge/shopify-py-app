# backend/main.py
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jwt
import os
from typing import Optional

app = FastAPI(title="Shopify App Backend")

# CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProcessRequest(BaseModel):
    action: str
    data: Optional[dict] = None

def verify_session_token(authorization: str = Header(None)):
    """Verify Shopify session token from frontend"""
    if not authorization:
        raise HTTPException(status_code=401, detail="No authorization header")
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(
            token, 
            os.getenv("SHOPIFY_API_SECRET"), 
            algorithms=["HS256"]
        )
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
def read_root():
    return {"message": "Shopify App Backend Running"}

@app.post("/api/process")
def process_request(
    request: ProcessRequest,
    session: dict = Depends(verify_session_token)
):
    """Main processing endpoint - customize this for your needs"""
    
    shop_domain = session.get("dest", "").replace("https://", "").replace("/admin", "")
    
    # Your business logic here
    if request.action == "test":
        return {
            "success": True,
            "message": f"Connected to shop: {shop_domain}",
            "data": request.data
        }
    
    # Add more actions as needed
    return {"success": False, "message": "Unknown action"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}