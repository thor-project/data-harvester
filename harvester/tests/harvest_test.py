import unittest

from harvester.harvester import ORCIDHarvester, DATACiteHarvester

__author__ = 'eamonnmaguire'


class ORCIDHarvestTest(unittest.TestCase):
    def setUp(self):
        self.harvester = ORCIDHarvester()


    def test_harvest_stats(self):
        _dict = self.harvester.harvest()

        for statistic in self.harvester.get_available_statistics():
            self.assertTrue(len(_dict['stats'][statistic]) > 0, msg="{} should have returned results".format(statistic))
        print _dict['stats']


class DataCiteHarvestTest(unittest.TestCase):
    def setUp(self):
        self.harvester = DATACiteHarvester()

    def test_harvest_works(self):

        results = self.harvester.get_works()
        for result in results:
            print result
        self.assertTrue(len(results) > 0)