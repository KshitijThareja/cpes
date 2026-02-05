# CPES NoSQL Schema Design

An implementation of the NoSQL schema design for the CPES system is given below.

## Document Structure

**Collection:** `evaluations`

The document represents a single evaluation event but contains the candidate's snapshot at that time.

| Field | Type | Description |
| :--- | :--- | :--- |
| `_id` | ObjectId | Unique identifier for the evaluation. |
| `candidate` | Object | Embedded candidate details. |
| `candidate.email` | String | Unique identifier for the candidate (Indexed). |
| `candidate.name` | String | Name of the candidate. |
| `candidate.phone` | String | Contact number. |
| `profile` | Object | The raw input data used for this evaluation. |
| `profile.years_of_experience` | Integer | Years of experience input. |
| `profile.num_projects` | Integer | Number of projects input. |
| `profile.skill_level` | String | Enum: "Low", "Medium", "High" |
| `profile.learning_velocity` | String | Enum: "Low", "Medium", "High" |
| `profile.role_readiness` | String | Enum: "Not Ready", "Partially Ready", "Ready" |
| `scores` | Object | The calculated partial scores. |
| `scores.experience` | Integer | Score (0-25) |
| `scores.projects` | Integer | Score (0-25) |
| `scores.skills` | Integer | Score (0-20) |
| `scores.learning` | Integer | Score (0-15) |
| `scores.readiness` | Integer | Score (0-15) |
| `result` | Object | The final evaluation outcome. |
| `result.total_score` | Integer | Sum of all scores (0-100). |
| `result.fit_category` | String | Enum: "Not Ready", "Potential Fit", "Strong Fit" |
| `result.explanation` | String | Generated summary text. |
| `created_at` | ISODate | Timestamp of evaluation. |

## Sample JSON

```json
{
  "_id": { "$oid": "64f1a2b3c4d5e6f7a8b9c0d1" },
  "candidate": {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "1234567890"
  },
  "profile": {
    "years_of_experience": 6,
    "num_projects": 10,
    "skill_level": "High",
    "learning_velocity": "High",
    "role_readiness": "Ready"
  },
  "scores": {
    "experience": 25,
    "projects": 25,
    "skills": 20,
    "learning": 15,
    "readiness": 15
  },
  "result": {
    "total_score": 100,
    "fit_category": "Strong Fit",
    "explanation": "Candidate scored 100/100 based on: Experience (25), Projects (25), Skills (20), Learning Velocity (15), Role Readiness (15). Result: Strong Fit"
  },
  "created_at": { "$date": "2023-10-27T10:00:00Z" }
}
```
