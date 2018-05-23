import unittest
from function import *


class RandomTest(unittest.TestCase):

    def setUp(self):
        self.list_emplacement = ['paris', 'bar à chat', 'openclassrooms', 'université villetaneuse', 'piscine molitor']
        self.list_sentance = ['jacque chirac', 'musée du louvre', 'Cathédrale Notre-Dame de Paris', 'dragon', 'Phénix']
        self.list_emplacement_sentance = ['paris', 'musée du louvre', 'nike', 'google', 'openclassrooms']
        self.wrong_search = 'oefnuiçzebgfizehbguiozebgizebgihzebg'

    def test_emplacement(self):
        for emplacement in self.list_emplacement:
            test_emplacement = get_emplacement_maps(emplacement)
            self.assertIsNot(test_emplacement, False)

    def test_description(self):
        for sentance in self.list_sentance:
            test_sentance = get_description_wiki(sentance)
            self.assertIsNot(test_sentance, False)

    def test_emplacement_sentance(self):
        for element in self.list_emplacement_sentance:
            test_emplacement = get_emplacement_maps(element)
            test_sentance = get_description_wiki(element)
            self.assertIsNot(test_emplacement, False)
            self.assertIsNot(test_sentance, False)

    def test_wrong_description(self):
        test_sentance = get_description_wiki(self.wrong_search)
        self.assertIs(test_sentance, False)

    def test_wrong_emplacement(self):
        test_sentance = get_emplacement_maps(self.wrong_search)
        self.assertIs(test_sentance, False)

    def test_wrong_emplacement_sentance(self):
        test_emplacement = get_emplacement_maps(self.wrong_search)
        test_sentance = get_description_wiki(self.wrong_search)
        self.assertIs(test_emplacement, False)
        self.assertIs(test_sentance, False)