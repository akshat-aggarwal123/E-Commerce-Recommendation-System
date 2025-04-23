import unittest
from fastapi.testclient import TestClient
from ...app.main import app
from ...app.services.recommendation_service import RecommendationService
import pandas as pd

class TestRecommendationEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment before running tests.
        """
        cls.client = TestClient(app)
        cls.service = RecommendationService()

    def test_generate_recommendations(self):
        """
        Test the recommendation generation logic.
        """
        customer_id = "C3805"  # Example customer ID from the dataset
        top_n = 5
        
        try:
            recommendations = self.service.generate_recommendations(customer_id, top_n)
            self.assertIsInstance(recommendations, list)
            self.assertTrue(len(recommendations) <= top_n)
            self.assertIn("Product_ID", recommendations[0])
            self.assertIn("Recommendation_Score", recommendations[0])
        except Exception as e:
            self.fail(f"generate_recommendations failed with exception: {e}")

    def test_recommendation_api(self):
        """
        Test the /recommend/{customer_id} API endpoint.
        """
        customer_id = "C3805"  # Example customer ID from the dataset
        top_n = 5
        
        response = self.client.get(f"/recommend/{customer_id}", params={"top_n": top_n})
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("recommendations", data)
        recommendations = data["recommendations"]
        
        self.assertIsInstance(recommendations, list)
        self.assertTrue(len(recommendations) <= top_n)
        self.assertIn("Product_ID", recommendations[0])
        self.assertIn("Recommendation_Score", recommendations[0])

    def test_invalid_customer_id(self):
        """
        Test the behavior when an invalid customer ID is provided.
        """
        invalid_customer_id = "INVALID_CUSTOMER"
        response = self.client.get(f"/recommend/{invalid_customer_id}", params={"top_n": 5})
        self.assertEqual(response.status_code, 500)
        self.assertIn("detail", response.json())

if __name__ == "__main__":
    unittest.main()