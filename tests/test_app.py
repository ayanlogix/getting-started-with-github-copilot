"""
Unit tests for Mergington High School Activities API
Generated with GitHub Copilot assistance
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from app import app, activities

client = TestClient(app)


def test_get_activities():
    """Test that activities endpoint returns all activities"""
    response = client.get('/activities')
    assert response.status_code == 200
    data = response.json()
    assert 'Chess Club' in data
    assert 'Programming Class' in data
    assert 'Gym Class' in data
    assert 'Art Club' in data
    assert 'Drama Club' in data


def test_activity_has_description():
    """Test that each activity has a description field"""
    response = client.get('/activities')
    data = response.json()
    for name, details in data.items():
        assert 'description' in details, f'{name} is missing description'


def test_signup_for_activity():
    """Test signing up a new participant"""
    response = client.post('/activities/Art Club/signup?email=test@mergington.edu')
    assert response.status_code == 200
    assert 'Signed up' in response.json()['message']
    # Cleanup
    activities['Art Club']['participants'].remove('test@mergington.edu')


def test_signup_activity_not_found():
    """Test signing up for non-existent activity returns 404"""
    response = client.post('/activities/Nonexistent Club/signup?email=test@mergington.edu')
    assert response.status_code == 404


def test_signup_already_registered():
    """Test that duplicate signup returns 400"""
    response = client.post('/activities/Chess Club/signup?email=michael@mergington.edu')
    assert response.status_code == 400
