from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
import enum
from database import Base

class SkillLevel(str, enum.Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"

class LearningVelocity(str, enum.Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"

class RoleReadiness(str, enum.Enum):
    NotReady = "Not Ready"
    PartiallyReady = "Partially Ready"
    Ready = "Ready"

class FitCategory(str, enum.Enum):
    NotReady = "Not Ready"
    PotentialFit = "Potential Fit"
    StrongFit = "Strong Fit"

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)

    profile = relationship("CandidateProfile", back_populates="candidate", uselist=False)

class CandidateProfile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    years_of_experience = Column(Integer)
    num_projects = Column(Integer)
    skill_level = Column(SQLEnum(SkillLevel))
    learning_velocity = Column(SQLEnum(LearningVelocity))
    role_readiness = Column(SQLEnum(RoleReadiness))

    candidate = relationship("Candidate", back_populates="profile")
    evaluations = relationship("Evaluation", back_populates="profile")

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    experience_score = Column(Integer)
    project_score = Column(Integer)
    skill_score = Column(Integer)
    learning_score = Column(Integer)
    readiness_score = Column(Integer)
    total_score = Column(Integer)
    fit_category = Column(SQLEnum(FitCategory))
    explanation = Column(String)

    profile = relationship("CandidateProfile", back_populates="evaluations")
