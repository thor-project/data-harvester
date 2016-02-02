import json
import os
from datetime import datetime
from iso8601 import ParseError

__author__ = 'eamonnmaguire'


class Harvester(object):
    cachedir = 'cache'

    def get_url(self, url):
        import requests
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers=headers)
        contents = response.text
        return json.loads(contents)

    def harvest(self):
        pass

    def write_as_json(self, dict, file_path):
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

            if normalise_month:
                parsed_date = datetime.strftime(time, '%Y-%m-01')
            else:
                parsed_date = datetime.strftime(time, '%Y-%m-%d')

            return True, parsed_date, datetime.strptime(parsed_date, '%Y-%m-%d')
        except ParseError:
            return False, None, None


class ORCIDHarvester(Harvester):
    _base_url = 'https://pub.orcid.org/v2.0_rc1/statistics/{}'
    _statistics_to_retrieve = ['liveIds', 'idsWithWorks', 'idsWithVerifiedEmail', 'uniqueDois', 'works',
                               'worksWithDois', 'funding', 'education', 'employment']

    def harvest(self):
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
        self.write_as_json(results, os.path.join(self.cachedir, 'orcids.json'))
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
        return self._statistics_to_retrieve


class DATACiteHarvester(Harvester):
    # {0} - facet type, e.g. allocator
    # {1} - facet value, e.g. ANDS
    # {2} - date to facet on
    # {3} - start date, e.g. 2000-01-01T00:00:00Z
    # {4} - end data, e.g. 2015-12-01T00:00:00Z
    # {5} - additional facets, e.g. dataset type &fq=resourceTypeGeneral:"dataset"
    _base_url = 'http://search.datacite.org/api?q={0}&fq={1}_facet:"{2}"&fq=is_active:true&fq=has_metadata:true&wt=json&rows=0&facet=true&facet.date={3}&facet.date.start={4}&facet.date.end={5}&facet.date.gap=%2B1MONTH{6}'

    _start_date = "2000-01-01T00:00:00Z"
    _end_date = "2016-02-01T00:00:00Z"
    _date_field = "minted"

    search_space = [

        {'type': 'datacentre', 'resource': 'CDL.DRYAD+-+Dryad', 'country': 'United States'},
        {'type': 'datacentre', 'resource': 'CDL.DIGSCI+-+Digital+Science', 'country': 'United Kingdom'},
        {'type': 'datacentre', 'resource': 'BL.IMPERIAL+-+Imperial+College+London', 'country': 'United Kingdom'},
        {'type': 'datacentre', 'resource': 'BL.CCDC+-+The+Cambridge+Crystallographic+Data+Centre',
         'country': 'United Kingdom'},
        {'type': 'datacentre', 'resource': 'BL.F1000R+-+Faculty+of+1000+Research+Ltd', 'country': 'United Kingdom'},
        {'type': 'datacentre', 'resource': 'BL.UKDA+-+UK+Data+Archive', 'country': 'United Kingdom'},
        {'type': 'datacentre',
         'resource': 'TIB.PANGAEA+-+PANGAEA+-+Publishing+Network+for+Geoscientific+and+Environmental+Data',
         'country': 'Germany'},
        {'type': 'datacentre', 'resource': 'TIB.R-GATE+-+ResearchGate', 'country': 'Germany'},
        {'type': 'allocator', 'resource': 'ANDS+-+Australian+National+Data+Service', 'country': 'Australia'},
        {'type': 'datacentre', 'resource': 'CERN.ZENODO+-+ZENODO+-+Research.+Shared.', 'country': 'Switzerland'},
        {'type': 'datacentre', 'resource': 'CERN.YELLOW+-+CERN+Yellow+Reports', 'country': 'Switzerland'}
    ]

    resource_types = [{'name': 'Collection', 'facet': '&fq=resourceType_facet:"Collection"'},
                      {'name': 'Dataset', 'facet': '&fq=resourceType_facet:"Dataset"'},
                      {'name': 'Text', 'facet': '&fq=resourceType_facet:"Text"'},
                      {'name': 'Software', 'facet': '&fq=resourceType_facet:"Software"'},
                      {'name': 'other', 'facet': '&fq=resourceType_facet:"Other"'},
                      {'name': 'Unknown', 'facet': "&fq=-resourceType_facet%3A[*+TO+*]"}
                      ]

    restrictions = [{'name': 'with_orcids', 'query': 'nameIdentifier:ORCID%5C:*'},
                    {'name': 'without_orcids', 'query': '*'}]

    def harvest(self):
        os.makedirs(self._cachedir)

    def get_works(self):
        results = []
        for resource in self.search_space:
            for resource_type in self.resource_types:
                for restriction in self.restrictions:
                    results += self.process_statistics(resource, resource_type['name'], restriction,
                                                       self.get_statistic(self._base_url, restriction['query'],
                                                                          resource['type'], resource['resource'],
                                                                          self._date_field,
                                                                          self._start_date, self._end_date,
                                                                          resource_type['facet']))

        self.write_as_json(results, os.path.join(self.cachedir, 'dois.json'))
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
