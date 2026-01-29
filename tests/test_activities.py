"""Test cases for FastAPI activities management application."""
import pytest


class TestGetActivities:
    """Tests for retrieving activities."""
    
    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns a 200 status code."""
        response = client.get("/activities")
        assert response.status_code == 200
    
    def test_get_activities_returns_dict(self, client):
        """Test that GET /activities returns a dictionary."""
        response = client.get("/activities")
        assert isinstance(response.json(), dict)
    
    def test_get_activities_contains_expected_activities(self, client):
        """Test that response contains expected activity names."""
        response = client.get("/activities")
        activities = response.json()
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
            "Soccer Club", "Art Club", "Drama Club", "Debate Team", "Science Club"
        ]
        for activity in expected_activities:
            assert activity in activities
    
    def test_activity_has_required_fields(self, client):
        """Test that each activity has all required fields."""
        response = client.get("/activities")
        activities = response.json()
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        for activity_name, activity_data in activities.items():
            for field in required_fields:
                assert field in activity_data, f"{activity_name} missing {field}"
    
    def test_participants_is_list(self, client):
        """Test that participants field is a list."""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list), \
                f"{activity_name} participants should be a list"
    
    def test_max_participants_is_integer(self, client):
        """Test that max_participants field is an integer."""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["max_participants"], int), \
                f"{activity_name} max_participants should be an integer"


class TestSignupForActivity:
    """Tests for signing up for activities."""
    
    def test_signup_new_student_returns_200(self, client, reset_activities):
        """Test that signing up a new student returns 200."""
        response = client.post(
            "/activities/Basketball%20Team/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
    
    def test_signup_new_student_returns_success_message(self, client, reset_activities):
        """Test that signup returns appropriate success message."""
        response = client.post(
            "/activities/Basketball%20Team/signup?email=newstudent@mergington.edu"
        )
        data = response.json()
        assert "message" in data
        assert "Signed up" in data["message"]
        assert "newstudent@mergington.edu" in data["message"]
    
    def test_signup_adds_participant(self, client, reset_activities):
        """Test that signup adds participant to activity."""
        email = "newstudent@mergington.edu"
        client.post(f"/activities/Basketball%20Team/signup?email={email}")
        
        response = client.get("/activities")
        activities = response.json()
        assert email in activities["Basketball Team"]["participants"]
    
    def test_signup_nonexistent_activity_returns_404(self, client):
        """Test that signup for non-existent activity returns 404."""
        response = client.post(
            "/activities/NonExistent%20Activity/signup?email=student@mergington.edu"
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_signup_duplicate_email_returns_400(self, client, reset_activities):
        """Test that signing up duplicate email returns 400."""
        email = "michael@mergington.edu"  # Already in Chess Club
        response = client.post(
            f"/activities/Chess%20Club/signup?email={email}"
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_same_student_different_activities(self, client, reset_activities):
        """Test that a student can sign up for multiple different activities."""
        email = "newstudent@mergington.edu"
        
        # Sign up for two different activities
        response1 = client.post(
            f"/activities/Basketball%20Team/signup?email={email}"
        )
        response2 = client.post(
            f"/activities/Soccer%20Club/signup?email={email}"
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify in both activities
        activities = client.get("/activities").json()
        assert email in activities["Basketball Team"]["participants"]
        assert email in activities["Soccer Club"]["participants"]


class TestUnregisterFromActivity:
    """Tests for unregistering from activities."""
    
    def test_unregister_existing_participant_returns_200(self, client, reset_activities):
        """Test that unregistering an existing participant returns 200."""
        email = "michael@mergington.edu"  # Already in Chess Club
        response = client.delete(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        assert response.status_code == 200
    
    def test_unregister_returns_success_message(self, client, reset_activities):
        """Test that unregister returns appropriate success message."""
        email = "michael@mergington.edu"
        response = client.delete(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        data = response.json()
        assert "message" in data
        assert "Unregistered" in data["message"]
        assert email in data["message"]
    
    def test_unregister_removes_participant(self, client, reset_activities):
        """Test that unregister removes participant from activity."""
        email = "michael@mergington.edu"
        client.delete(f"/activities/Chess%20Club/unregister?email={email}")
        
        response = client.get("/activities")
        activities = response.json()
        assert email not in activities["Chess Club"]["participants"]
    
    def test_unregister_nonexistent_activity_returns_404(self, client):
        """Test that unregister from non-existent activity returns 404."""
        response = client.delete(
            "/activities/NonExistent%20Activity/unregister?email=student@mergington.edu"
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_unregister_non_participant_returns_400(self, client, reset_activities):
        """Test that unregistering non-participant returns 400."""
        email = "notregistered@mergington.edu"
        response = client.delete(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]
    
    def test_unregister_multiple_times_fails_second_time(self, client, reset_activities):
        """Test that unregistering the same participant twice fails on second attempt."""
        email = "michael@mergington.edu"
        
        # First unregister should succeed
        response1 = client.delete(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        assert response1.status_code == 200
        
        # Second unregister should fail
        response2 = client.delete(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        assert response2.status_code == 400
        assert "not registered" in response2.json()["detail"]


class TestSignupAndUnregisterInteraction:
    """Tests for interactions between signup and unregister."""
    
    def test_signup_then_unregister(self, client, reset_activities):
        """Test signing up and then unregistering."""
        email = "newstudent@mergington.edu"
        
        # Sign up
        response1 = client.post(
            f"/activities/Basketball%20Team/signup?email={email}"
        )
        assert response1.status_code == 200
        
        # Verify signup worked
        activities = client.get("/activities").json()
        assert email in activities["Basketball Team"]["participants"]
        
        # Unregister
        response2 = client.delete(
            f"/activities/Basketball%20Team/unregister?email={email}"
        )
        assert response2.status_code == 200
        
        # Verify unregister worked
        activities = client.get("/activities").json()
        assert email not in activities["Basketball Team"]["participants"]
    
    def test_unregister_then_signup_again(self, client, reset_activities):
        """Test unregistering and then signing up again."""
        email = "michael@mergington.edu"
        
        # Unregister
        response1 = client.delete(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        assert response1.status_code == 200
        
        # Verify unregister worked
        activities = client.get("/activities").json()
        assert email not in activities["Chess Club"]["participants"]
        
        # Sign up again
        response2 = client.post(
            f"/activities/Chess%20Club/signup?email={email}"
        )
        assert response2.status_code == 200
        
        # Verify signup worked
        activities = client.get("/activities").json()
        assert email in activities["Chess Club"]["participants"]
