from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db, Base
import models
import schemas
import logic

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Candidate Profile Evaluation System (CPES)")

@app.post("/evaluate", response_model=schemas.EvaluationResponse)
def evaluate_candidate(profile_data: schemas.CandidateProfileCreate, db: Session = Depends(get_db)):
    candidate = db.query(models.Candidate).filter(models.Candidate.email == profile_data.email).first()
    if not candidate:
        candidate = models.Candidate(
            name=profile_data.name,
            email=profile_data.email,
            phone=profile_data.phone
        )
        db.add(candidate)
        db.commit()
        db.refresh(candidate)

    db_profile = models.CandidateProfile(
        candidate_id=candidate.id,
        years_of_experience=profile_data.years_of_experience,
        num_projects=profile_data.num_projects,
        skill_level=profile_data.skill_level,
        learning_velocity=profile_data.learning_velocity,
        role_readiness=profile_data.role_readiness
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)

    eval_result = logic.evaluate_candidate(profile_data)
    
    db_evaluation = models.Evaluation(
        profile_id=db_profile.id,
        experience_score=eval_result["scores"]["experience"],
        project_score=eval_result["scores"]["projects"],
        skill_score=eval_result["scores"]["skill"],
        learning_score=eval_result["scores"]["learning"],
        readiness_score=eval_result["scores"]["readiness"],
        total_score=eval_result["total_score"],
        fit_category=eval_result["fit_category"],
        explanation=eval_result["explanation"]
    )
    db.add(db_evaluation)
    db.commit()
    db.refresh(db_evaluation)

    return {
        "candidate_name": candidate.name,
        "total_score": eval_result["total_score"],
        "fit_category": eval_result["fit_category"],
        "explanation": eval_result["explanation"],
        "breakdown": eval_result["scores"]
    }

@app.get("/evaluations/{evaluation_id}", response_model=schemas.EvaluationResponse)
def get_evaluation(evaluation_id: int, db: Session = Depends(get_db)):
    evaluation = db.query(models.Evaluation).filter(models.Evaluation.id == evaluation_id).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    candidate_name = evaluation.profile.candidate.name
    
    return {
        "candidate_name": candidate_name,
        "total_score": evaluation.total_score,
        "fit_category": evaluation.fit_category,
        "explanation": evaluation.explanation,
        "breakdown": {
            "experience": evaluation.experience_score,
            "projects": evaluation.project_score,
            "skill": evaluation.skill_score,
            "learning": evaluation.learning_score,
            "readiness": evaluation.readiness_score
        }
    }
@app.get("/candidate/{candidate_id}", response_model=schemas.CandidateResponse)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate
