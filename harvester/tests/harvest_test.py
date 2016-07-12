#
# This file is part of the THOR Dashboard Project.
# Copyright (C) 2016 CERN.
#
# The THOR dashboard is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# HEPData is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with the THOR dashboard; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

import unittest

from harvester.harvester import ORCIDHarvester, DATACiteHarvester

__author__ = 'eamonnmaguire'


class ORCIDHarvestTest(unittest.TestCase):
    def setUp(self):
        self.harvester = ORCIDHarvester()

    def test_harvest_stats(self):
        results = self.harvester.harvest()
        self.assertTrue(len(results) > 0,
                        msg="Number of results returned is zero.")

        statistics = self.harvester.get_available_statistics()
        for statistic in statistics:
            for item in results:
                self.assertTrue(statistic in item,
                                msg='{0} not present for date {1}'.format(
                                    statistic, item['date']))


class DataCiteHarvestTest(unittest.TestCase):
    def setUp(self):
        self.harvester = DATACiteHarvester()

    def test_harvest_works(self):
        results = self.harvester.get_works()
        for result in results:
            print result
        self.assertTrue(len(results) > 0)
