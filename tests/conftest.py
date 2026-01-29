"""Pytest configuration and fixtures for FastAPI tests."""
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from fastapi.testclient import TestClient
from app import app, activities


@pytest.fixture
def client():
    """Provide a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before and after each test."""
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Join the team for practice and games",
            "schedule": "Tuesdays and Thursdays, 4:30 PM - 6:00 PM",
            "max_participants": 15,
            "participants": []
        },
        "Soccer Club": {
            "description": "Practice soccer skills and compete in matches",
            "schedule": "Mondays and Wednesdays, 3:00 PM - 5:00 PM",
            "max_participants": 20,
            "participants": []
        },
        "Art Club": {
            "description": "Explore various art techniques and create projects",
            "schedule": "Fridays, 3:00 PM - 5:00 PM",
            "max_participants": 15,
            "participants": []
        },
        "Drama Club": {
            "description": "Participate in theater productions and improv",
            "schedule": "Tuesdays, 3:30 PM - 5:30 PM",
            "max_participants": 20,
            "participants": []
        },
        "Debate Team": {
            "description": "Engage in debates and improve public speaking skills",
            "schedule": "Wednesdays, 4:00 PM - 6:00 PM",
            "max_participants": 12,
            "participants": []
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Thursdays, 3:00 PM - 5:00 PM",
            "max_participants": 15,
            "participants": []
        }
    }
    
    # Store original state
    original_state = {k: {"participants": v["participants"].copy()} for k, v in activities.items()}
    
    yield
    
    # Restore original state
    for activity_name, original_data in original_state.items():
        activities[activity_name]["participants"] = original_data["participants"].copy()
