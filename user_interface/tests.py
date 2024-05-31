from django.test import TestCase
from .models import ExperienceModel
from .forms import ExperienceForm

# Create your tests here.
class TestExperienceForm(TestCase):
    def test_is_invalid(self):
        form = ExperienceForm(
            data={

            }
            )
        self.assertFalse(form.is_valid())

    def test_is_valid(self):
        # setup
        data = {
             'user': "testUser", 
             'expTitle': "exp", 
             'expYear': "2024-01-01", 
             'location': "Nairobi", 
             'expEndYear': "2024-12-31", 
             'company': "MyCompany", 
             'expDescription': "Description"
         }

        # execute
        form = ExperienceForm(data=data)

        # assert
        self.assertTrue(form.is_valid())

    def test_not_working_here(self):
        # setup
        data = {
             'user': "testUser", 
             'expTitle': "exp", 
             'expYear': "2024-01-01", 
             'location': "Nairobi", 
             'expEndYear': "", 
             'company': "MyCompany", 
             'expDescription': "Description",
             'stillWorkingHere': False
         }

        # execute
        form = ExperienceForm(data=data)

        # assert
        self.assertFalse(form.is_valid())

    def test_still_working_here(self):
        # setup
        data = {
                'user': "testUser", 
                'expTitle': "exp", 
                'expYear': "2024-01-01", 
                'location': "Nairobi", 
                'expEndYear': "", 
                'company': "MyCompany", 
                'expDescription': "Description",
                'stillWorkingHere': True
            }

        # execute
        form = ExperienceForm(data=data)

        # assert
        self.assertTrue(form.is_valid())
