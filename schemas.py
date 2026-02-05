from pydantic import BaseModel, EmailStr, Field, field_validator
from enum import Enum
from typing import Optional

class SkillLevel(str, Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"

class LearningVelocity(str, Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"

class RoleReadiness(str, Enum):
    NotReady = "Not Ready"
    PartiallyReady = "Partially Ready"
    Ready = "Ready"

class CandidateProfileCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    phone: Optional[str] = None
    years_of_experience: int = Field(..., ge=0)
    num_projects: int = Field(..., ge=0)
    skill_level: SkillLevel
    learning_velocity: LearningVelocity
    role_readiness: RoleReadiness

class EvaluationResponse(BaseModel):
    candidate_name: str
    total_score: int
    fit_category: str
    explanation: str
    breakdown: dict

    class Config:
        from_attributes = True

class CandidateResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    
    class Config:
        from_attributes = True
