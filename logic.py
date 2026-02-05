from models import SkillLevel, LearningVelocity, RoleReadiness, FitCategory

def experience_score(years: int) -> int:
    return min(5 * years, 25)

def project_score(num_projects: int) -> int:
    return min(4 * num_projects, 25)

def skill_score(level: SkillLevel) -> int:
    mapping = {
        SkillLevel.Low: 5,
        SkillLevel.Medium: 13,
        SkillLevel.High: 20
    }
    return mapping[level]

def learning_score(velocity: LearningVelocity) -> int:
    mapping = {
        LearningVelocity.Low: 3,
        LearningVelocity.Medium: 10,
        LearningVelocity.High: 15
    }
    return mapping[velocity]

def readiness_score(readiness: RoleReadiness) -> int:
    mapping = {
        RoleReadiness.NotReady: 3,
        RoleReadiness.PartiallyReady: 10,
        RoleReadiness.Ready: 15
    }
    return mapping[readiness]

def fit_category(total_score: int) -> FitCategory:
    if total_score < 40:
        return FitCategory.NotReady
    elif total_score < 70:
        return FitCategory.PotentialFit
    else:
        return FitCategory.StrongFit

def explanation(scores: dict, total: int, fit: FitCategory) -> str:
    return (
        f"Candidate scored {total}/100 based on: "
        f"Experience ({scores['experience']}), Projects ({scores['projects']}), "
        f"Skills ({scores['skill']}), Learning Velocity ({scores['learning']}), "
        f"Role Readiness ({scores['readiness']}). "
        f"Result: {fit.value}"
    )

def evaluate_candidate(data):
    exp_score = experience_score(data.years_of_experience)
    proj_score = project_score(data.num_projects)
    sk_score = skill_score(data.skill_level)
    learn_score = learning_score(data.learning_velocity)
    ready_score = readiness_score(data.role_readiness)

    total_score = exp_score + proj_score + sk_score + learn_score + ready_score
    fit = fit_category(total_score)

    scores = {
        "experience": exp_score,
        "projects": proj_score,
        "skill": sk_score,
        "learning": learn_score,
        "readiness": ready_score
    }
    
    exp = explanation(scores, total_score, fit)

    return {
        "scores": scores,
        "total_score": total_score,
        "fit_category": fit,
        "explanation": exp
    }
