from django.test import TestCase
from election_results.models import Party

class PartyTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInitialPartyData(self):
        initial_party_data = {
            "C": "Conservative Party",
            "L": "Labour Party",
            "UKIP": "UKIP",
            "LD": "Liberal Democrats",
            "G": "Green Party",
            "Ind": "Independent",
            "SNP": "SNP",
        }
        self.assertEqual(Party.as_dict_by_code(), initial_party_data)
