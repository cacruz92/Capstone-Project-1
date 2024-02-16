import unittest
from flask import Flask
from flask_testing import TestCase
from models import db, User
from app import app

class TestApp(TestCase):
    """Test cases for the app."""

    def create_app(self):
        """Create the app instance for testing."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///diet_tracker_test'
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        """Set up the test database."""
        db.create_all()

    def tearDown(self):
        """Tear down the test database."""
        db.session.remove()
        db.drop_all()

    def test_valid_signup(self):
        """Test user signup with valid data."""
        response = self.client.post('/register', data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'password',
            'daily_calorie_goal': 2000,
            'goal_weight': 180
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<p><b>Name:</b> John Doe</p>", response.data)

    def test_invalid_signup(self):
        """Test user signup with invalid data."""
        response = self.client.post('/register', data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalid_email',
            'password': 'password',
            'daily_calorie_goal': 2000,
            'goal_weight': 180
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"<p><b>Name:</b> John Doe</p>", response.data)
        self.assertIn(b"Invalid email address.", response.data)

    def test_valid_login(self):
        """Test user login with valid credentials."""
        user = User(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="password",
            daily_calorie_goal=2000,
            goal_weight=180
        )
        db.session.add(user)
        db.session.commit()
        response = self.client.post('/login', data={
            'email': 'john@example.com',
            'password': 'password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Logged in successfully!", response.data)

    def test_invalid_login(self):
        """Test user login with invalid credentials."""
        response = self.client.post('/login', data={
            'email': 'john@example.com',
            'password': 'wrong_password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Logged in successfully!", response.data)
        self.assertIn(b"Invalid credentials.", response.data)

if __name__ == '__main__':
    unittest.main()
