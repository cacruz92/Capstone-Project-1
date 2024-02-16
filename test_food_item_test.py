import unittest
from flask import Flask
from flask_testing import TestCase
from models import db, FoodItem
from app import app

class TestFoodItemModel(TestCase):
    """Test cases for the FoodItem model."""

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

    def test_fooditem_creation(self):
        """Test creation of a FoodItem."""
        food_item = FoodItem(
            name="Apple",
            calories=95,
            protein=0.5,
            carbohydrates=25,
            fat=0.3
        )
        db.session.add(food_item)
        db.session.commit()

        queried_food_item = FoodItem.query.filter_by(name="Apple").first()
        self.assertIsNotNone(queried_food_item)
        self.assertEqual(queried_food_item.calories, 95)
        self.assertEqual(queried_food_item.protein, 0.5)
        self.assertEqual(queried_food_item.carbohydrates, 25)
        self.assertEqual(queried_food_item.fat, 0.3)

    def test_fooditem_deletion(self):
        """Test deletion of a FoodItem."""
        food_item = FoodItem(
            name="Banana",
            calories=105,
            protein=1.3,
            carbohydrates=27,
            fat=0.4
        )
        db.session.add(food_item)
        db.session.commit()

        db.session.delete(food_item)
        db.session.commit()

        queried_food_item = FoodItem.query.filter_by(name="Banana").first()
        self.assertIsNone(queried_food_item)

if __name__ == '__main__':
    unittest.main()
