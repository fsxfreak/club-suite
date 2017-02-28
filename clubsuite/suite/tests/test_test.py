'''
from django.test import TestCase
from suite.models import TestModel
# Create your tests here.
#

class TestModelTestCase(TestCase):
    def setUp(self):
        TestModel.objects.create(title="abc")

    def test_store(self):
        alphabet=TestModel.objects.get(title="abc")
        self.assertEqual(alphabet.title,"abc")
'''
