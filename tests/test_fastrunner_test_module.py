"""Test for fastrunner.test module"""
import pytest
from django.test import TestCase
from django.utils.crypto import get_random_string

from fastuser import models


@pytest.mark.django_db
class TestFastrunnerTestModule(TestCase):
    """Test the test module in fastrunner package"""
    
    def test_model_test_functionality(self):
        """Test that ModelTest class works correctly"""
        # Import the test class
        from fastrunner.test import ModelTest
        
        # Create an instance and run setup
        test_instance = ModelTest()
        test_instance.setUp()
        
        # Verify the user was created
        user = models.UserInfo.objects.get(username="rikasai")
        self.assertEqual(user.email, "lihuacai168@gmail.com")
        
        # Run the test method
        test_instance.test_user_register()