# coding=utf-8
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

import json
import os
from datetime import datetime

from iso8601 import ParseError

from .config import (DATACITE_ALLOCATOR_SEARCH_SPACE, DATACITE_RESOURCE_TYPES,
                     DATACITE_RESTRICTIONS, ORCID_STATISTICS)
from .utils import create_file_path

__author__ = 'eamonnmaguire'


class Harvester(object):

    def get_url(self, url):
        import requests
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers=headers)
        contents = response.text
        return json.loads(contents)

    def harvest(self, output_file):
        pass

    def write_as_json(self, dict, file_path):
        create_file_path(file_path)
        with open(file_path, 'w+') as file:
            file.write(json.dumps(dict))

    def get_statistic(self, base_url, *args):
        url = base_url.format(*args)
        print url
        response_contents = self.get_url(url)
        print response_contents
        docs = response_contents

        return docs

    @staticmethod
    def process_date(date, normalise_month=False):

        """
        :param date: date string to be parsed, e.g. 2000-01-07T00:00:00Z
        :param normalise_month: if True, normalise to the month, standardising the day, e.g. 2000-01-01
        :return: if truncated, then 2000-01-01, else 2000-01-07
        """
        import iso8601

        try:
            time = iso8601.parse_date(date)
        except ParseError:
            try:
                time = datetime.fromtimestamp(int(date)/1000.0)
            except Exception:
                return False, None, None


        if normalise_month:
            parsed_date = datetime.strftime(time, '%Y-%m-01')
        else:
            parsed_date = datetime.strftime(time, '%Y-%m-%d')

        return True, parsed_date, datetime.strptime(parsed_date, '%Y-%m-%d')



class ORCIDHarvester(Harvester):
    _base_url = 'https://pub.orcid.org/v2.0_rc1/statistics/{}'

    def harvest(self, output_file='cache/orcids.json'):
        # need to merge the stats into a coherent structure suitable for the front end.
        date_stats = {}
        for statistic in self.get_available_statistics():
            query_result = self.get_statistic(self._base_url, statistic)
            for date in query_result['timeline']:
                _success, processed_date_str, processed_date_datetime = self.process_date(date, normalise_month=True)

                if _success and processed_date_datetime not in date_stats:
                    date_stats[processed_date_datetime] = self.populate_default_dict(processed_date_str)

                if query_result['timeline'][date] > date_stats[processed_date_datetime][statistic]:
                    date_stats[processed_date_datetime][statistic] = query_result['timeline'][date]

        results = self.process_results(date_stats)
        self.write_as_json(results, output_file)
        return results

    def process_results(self, stats):
        import operator
        sorted_dates = sorted(stats.items(), key=operator.itemgetter(0))

        processed_values = []
        last_values = {}
        for statistic in self.get_available_statistics():
            last_values[statistic] = 0
        for index, date in enumerate(sorted_dates):

            value = date.__getitem__(1)
            for statistic in self.get_available_statistics():
                value[statistic + "_month"] = max(0, value[statistic] - last_values[statistic])
                last_values[statistic] = value[statistic]

            processed_values.append(value)

        return processed_values

    def populate_default_dict(self, date):
        __dict = {'date': date}

        for statistic in self.get_available_statistics():
            __dict[statistic] = 0
        return __dict

    def get_available_statistics(self):
        return ORCID_STATISTICS


class DATACiteHarvester(Harvester):
    # {0} - facet type, e.g. allocator
    # {1} - facet value, e.g. ANDS
    # {2} - date to facet on
    # {3} - start date, e.g. 2000-01-01T00:00:00Z
    # {4} - end data, e.g. 2015-12-01T00:00:00Z
    # {5} - additional facets, e.g. dataset type &fq=resourceTypeGeneral:"dataset"
    _base_url = 'http://search.datacite.org/api?q={0}&fq={1}_facet:"{2}"&fq=is_active:true' \
                '&fq=has_metadata:true&wt=json&rows=0&facet=true&facet.date={3}' \
                '&facet.date.start={4}&facet.date.end={5}&facet.date.gap=%2B1MONTH{6}'

    _start_date = '2000-01-01T00:00:00Z'
    _end_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    _date_field = 'minted'

    def harvest(self, output_file='cache/dois.json'):
        results = []
        for resource in DATACITE_ALLOCATOR_SEARCH_SPACE:
            for resource_type in DATACITE_RESOURCE_TYPES:
                for restriction in DATACITE_RESTRICTIONS:
                    results += self.process_statistics(resource, resource_type['name'], restriction,
                                                       self.get_statistic(self._base_url, restriction['query'],
                                                                          resource['type'], resource['resource'],
                                                                          self._date_field,
                                                                          self._start_date, self._end_date,
                                                                          resource_type['facet']))

        self.write_as_json(results, output_file)
        return results

    def process_statistics(self, resource, resource_type, restriction, statistics):

        result = []
        for x in statistics['facet_counts']['facet_dates']['minted']:
            _success, processed_date_str, processed_date_datetime = self.process_date(x)
            if _success and statistics['facet_counts']['facet_dates']['minted'][x] is not 0:
                result.append({'country': resource['country'], 'institution': resource['resource'],
                               'data_key': resource_type, 'date': processed_date_str,
                               'data_value': statistics['facet_counts']['facet_dates']['minted'][x],
                               'restriction': restriction['name']})

        return result
