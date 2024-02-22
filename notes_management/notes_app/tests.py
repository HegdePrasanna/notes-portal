from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Notes
class TestSetup(APITestCase):
    def setUp(self):
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()
# Create your tests here.
