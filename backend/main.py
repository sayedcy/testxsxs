from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import uvicorn
from datetime import timedelta
from typing import Optional
import os

from database import SessionLocal, engine, Base
from models import User, ScanJob
from schemas import UserCreate, UserResponse, Token, ScanJobCreate, ScanJobResponse
from auth import get_password_hash, verify_password, create_access_token, get_current_user
from scanner import create_scan_job, get_scan_job, list_scan_jobs, run_scan_workflow

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Security Scanner API", version="1.0.0")

# CORS middleware - Allow VPS IP and localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://37.60.241.19:5173",
        "http://37.60.241.19:3000",
        "http://37.60.241.19",
        "*"  # Allow all origins for development (remove in production)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/api/scans", response_model=ScanJobResponse)
def create_scan(
    scan: ScanJobCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_scan = create_scan_job(db, scan, current_user.id)
    # Start scan in background
    background_tasks.add_task(run_scan_workflow, db_scan.id, scan.domain)
    return ScanJobResponse.model_validate(db_scan)

@app.get("/api/scans", response_model=list[ScanJobResponse])
def list_scans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    scans = list_scan_jobs(db, current_user.id, skip, limit)
    return [ScanJobResponse.model_validate(scan) for scan in scans]

@app.get("/api/scans/{scan_id}", response_model=ScanJobResponse)
def get_scan(
    scan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    scan = get_scan_job(db, scan_id, current_user.id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return ScanJobResponse.model_validate(scan)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

