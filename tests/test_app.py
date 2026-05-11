import urllib.parse


def test_get_activities_returns_available_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert activities["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]


def test_signup_for_activity_adds_new_participant(client):
    email = "teststudent@mergington.edu"
    activity = "Chess Club"
    encoded_activity = urllib.parse.quote(activity, safe="")
    response = client.post(f"/activities/{encoded_activity}/signup?email={urllib.parse.quote(email, safe='')}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"

    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity]["participants"]


def test_duplicate_signup_returns_400(client):
    email = "michael@mergington.edu"
    activity = "Chess Club"
    encoded_activity = urllib.parse.quote(activity, safe="")
    response = client.post(f"/activities/{encoded_activity}/signup?email={urllib.parse.quote(email, safe='')}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_unregister_participant_removes_participant(client):
    email = "michael@mergington.edu"
    activity = "Chess Club"
    encoded_activity = urllib.parse.quote(activity, safe="")
    response = client.delete(f"/activities/{encoded_activity}/participants?email={urllib.parse.quote(email, safe='')}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity}"

    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity]["participants"]


def test_unregister_missing_participant_returns_404(client):
    email = "missing@student.edu"
    activity = "Chess Club"
    encoded_activity = urllib.parse.quote(activity, safe="")
    response = client.delete(f"/activities/{encoded_activity}/participants?email={urllib.parse.quote(email, safe='')}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in activity"
