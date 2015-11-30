import unittest

from harvester.harvester import ORCIDHarvester, DATACiteHarvester

__author__ = 'eamonnmaguire'


class ORCIDHarvestTest(unittest.TestCase):
    def setUp(self):
        self.harvester = ORCIDHarvester()


    def test_harvest_stats(self):
        results = self.harvester.harvest()

        self.assertTrue(len(results)>0, msg="Number of results returned is zero.")

        statistics = self.harvester.get_available_statistics()
        for statistic in statistics:
            for item in results:
                self.assertTrue(statistic in item, msg='{0} not present for date {1}'.format(statistic, item['date']))


class DataCiteHarvestTest(unittest.TestCase):
    def setUp(self):
        self.harvester = DATACiteHarvester()

    def test_harvest_works(self):

        results = self.harvester.get_works()
        for result in results:
            print result
        self.assertTrue(len(results) > 0)