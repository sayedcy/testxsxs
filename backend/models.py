from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base

class ScanStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    scan_jobs = relationship("ScanJob", back_populates="owner")

class ScanJob(Base):
    __tablename__ = "scan_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, index=True)
    status = Column(SQLEnum(ScanStatus), default=ScanStatus.PENDING)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Results storage
    subfinder_results = Column(Text, nullable=True)
    httpx_results = Column(Text, nullable=True)
    nuclei_results = Column(Text, nullable=True)
    katana_results = Column(Text, nullable=True)
    xss_results = Column(Text, nullable=True)
    dalfox_results = Column(Text, nullable=True)
    
    # Progress tracking
    current_step = Column(String, default="")
    progress = Column(Integer, default=0)  # 0-100
    
    owner = relationship("User", back_populates="scan_jobs")

