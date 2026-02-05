from fastapi.testclient import TestClient
from main import app
from models import FitCategory

client = TestClient(app)

def test_evaluation():
    # Test Data 1: Strong Fit
    print("Running Test 1: Strong Fit")
    payload1 = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "phone": "1234567890",
        "years_of_experience": 6,  # 5*6 = 30 -> min(30, 25) = 25
        "num_projects": 10,        # 4*10 = 40 -> min(40, 25) = 25
        "skill_level": "High",     # 20
        "learning_velocity": "High", # 15
        "role_readiness": "Ready"  # 15
    } # Total: 25+25+20+15+15 = 100
    
    response = client.post("/evaluate", json=payload1)
    assert response.status_code == 200
    data = response.json()
    assert data["total_score"] == 100
    assert data["fit_category"] == FitCategory.StrongFit.value

    # Test Data 2: Potential Fit
    print("Running Test 2: Potential Fit")
    payload2 = {
        "name": "John Smith",
        "email": "john@example.com",
        "phone": "0987654321",
        "years_of_experience": 2,  # 5*2 = 10
        "num_projects": 3,         # 4*3 = 12
        "skill_level": "Medium",   # 13
        "learning_velocity": "Medium", # 10
        "role_readiness": "Partially Ready" # 10
    } # Total: 10+12+13+10+10 = 55
    
    response = client.post("/evaluate", json=payload2)
    assert response.status_code == 200
    assert response.json()["total_score"] == 55

    # ---------------------------------------------------------
    # EDGE CASE 1: Boundary Values (39 vs 40, 69 vs 70)
    # ---------------------------------------------------------
    print("Running Edge Case 1: Boundary Values")
    
    # 39 Points (Not Ready)
    payload_39 = {
        "name": "Boundary 39",
        "email": "b39@example.com",
        "years_of_experience": 4, # 20
        "num_projects": 0,        # 0
        "skill_level": "Medium",  # 13
        "learning_velocity": "Low", # 3
        "role_readiness": "Not Ready" # 3
    } # Total 39
    resp = client.post("/evaluate", json=payload_39)
    assert resp.json()["total_score"] == 39
    assert resp.json()["fit_category"] == FitCategory.NotReady.value

    # 40 Points (Potential Fit)
    payload_40 = {
        "name": "Boundary 40",
        "email": "b40@example.com",
        "years_of_experience": 2, # 10
        "num_projects": 1,        # 4
        "skill_level": "Medium",  # 13
        "learning_velocity": "Medium", # 10
        "role_readiness": "Not Ready" # 3
    } # Total 40
    resp = client.post("/evaluate", json=payload_40)
    assert resp.json()["total_score"] == 40
    assert resp.json()["fit_category"] == FitCategory.PotentialFit.value

    # 69 Points (Potential Fit)
    payload_69 = {
        "name": "Boundary 69",
        "email": "b69@example.com",
        "years_of_experience": 4, # 20
        "num_projects": 4,        # 16
        "skill_level": "High",    # 20
        "learning_velocity": "Medium", # 10
        "role_readiness": "Not Ready" # 3
    } # Total 69
    resp = client.post("/evaluate", json=payload_69)
    assert resp.json()["total_score"] == 69
    assert resp.json()["fit_category"] == FitCategory.PotentialFit.value

    # 70 Points (Strong Fit)
    payload_70 = {
        "name": "Boundary 70",
        "email": "b70@example.com",
        "years_of_experience": 5, # 25
        "num_projects": 3,        # 12
        "skill_level": "High",    # 20
        "learning_velocity": "Medium", # 10
        "role_readiness": "Not Ready" # 3
    } # Total 70
    resp = client.post("/evaluate", json=payload_70)
    assert resp.json()["total_score"] == 70
    assert resp.json()["fit_category"] == FitCategory.StrongFit.value

    # ---------------------------------------------------------
    # EDGE CASE 2: Minimum Possible Score
    # ---------------------------------------------------------
    print("Running Edge Case 2: Minimum Score")
    payload_min = {
        "name": "Min Scorer",
        "email": "min@example.com",
        "years_of_experience": 0, # 0
        "num_projects": 0,        # 0
        "skill_level": "Low",     # 5
        "learning_velocity": "Low", # 3
        "role_readiness": "Not Ready" # 3
    } # Total 11
    resp = client.post("/evaluate", json=payload_min)
    assert resp.json()["total_score"] == 11
    assert resp.json()["fit_category"] == FitCategory.NotReady.value

    # ---------------------------------------------------------
    # EDGE CASE 3: Duplicate Candidate (Idempotency)
    # ---------------------------------------------------------
    print("Running Edge Case 3: Duplicate Candidate")
    # Using 'jane@example.com' from Test 1.
    # Should accept and create new profile/evaluation but link to same candidate ID.
    payload_dup = payload1.copy()
    payload_dup["name"] = "Jane Doe Updated" # Name might be ignored if email found, based on logic
    resp = client.post("/evaluate", json=payload_dup)
    assert resp.status_code == 200
    assert resp.json()["candidate_name"] == "Jane Doe" # Should preserve original name as per logic

    # ---------------------------------------------------------
    # EDGE CASE 4: Invalid Inputs (Validation)
    # ---------------------------------------------------------
    print("Running Edge Case 4: Invalid Inputs")
    payload_invalid = {
        "name": "Invalid",
        "email": "invalid-email", # Invalid email format
        "years_of_experience": -5, # Negative
        "num_projects": 0,
        "skill_level": "Super High", # Invalid Enum
        "learning_velocity": "Low",
        "role_readiness": "Not Ready"
    }
    resp = client.post("/evaluate", json=payload_invalid)
    assert resp.status_code == 422 # Unprocessable Entity
    
    print("All edge case tests passed!")

    # ---------------------------------------------------------
    # Test GET /candidate/{id}
    # ---------------------------------------------------------
    print("Running Test: Get Candidate")
    resp = client.get("/candidate/1")
    if resp.status_code == 200:
        data = resp.json()
        assert "name" in data
        assert "email" in data
        print(f"Candidate Fetched: {data}")
    else:
        print("Candidate 1 not found (might be first run or cleared DB).")

if __name__ == "__main__":
    test_evaluation()
