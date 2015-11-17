import json
import os
import urllib
import urllib2

__author__ = 'eamonnmaguire'


class Harvester(object):
    def __init__(self):
        pass

    def get_url(self, url):
        import requests
        response = requests.get(url)
        contents = response.text
        return json.loads(contents)

    def harvest(self):
        pass

    def write_as_json(self, dict, file_path):
        with open(file_path, 'w') as file:
            file.write(json.dumps(dict))

    def get_statistic(self, base_url, *args):
        url = base_url.format(*args)
        print url
        response_contents = self.get_url(url)
        print response_contents
        docs = response_contents

        return docs


class ORCIDHarvester(Harvester):
    _base_url = 'https://pub.orcid.org/v2.0_rc1/statistics/{}'
    _statistics_to_retrieve = ['liveIds', 'idsWithWorks', 'idsWithVerifiedEmail', 'uniqueDois', 'works']

    def harvest(self):
        # need to merge the stats into a coherent structure suitable for the front end.
        result = {"stats": {}}

        for statistic in self.get_available_statistics():
            result['stats'][statistic] = self.get_statistic(self._base_url, statistic)

        return result

    def get_available_statistics(self):
        return self._statistics_to_retrieve


class DATACiteHarvester(Harvester):
    # {0} - facet type, e.g. allocator
    # {1} - facet value, e.g. ANDS
    # {2} - date to facet on
    # {3} - start date, e.g. 2000-01-01T00:00:00Z
    # {4} - end data, e.g. 2015-12-01T00:00:00Z
    # {5} - additional facets, e.g. dataset type &fq=resourceTypeGeneral:"dataset"
    _base_url = 'http://search.datacite.org/api?q=*&fq={0}_facet:"{1}"&fq=is_active:true&fq=has_metadata:true&wt=json&rows=0&facet=true&facet.date={2}&facet.date.start={3}&facet.date.end={4}&facet.date.gap=%2B1MONTH{5}'
    _cachedir = 'cache'

    start_date = "2000-01-01T00:00:00Z"
    end_date = "2015-01-01T00:00:00Z"
    date_field = "minted"
    search_space = [
        {'type': 'datacentre', 'resource': 'CDL.DRYAD+-+Dryad', 'country': 'USA'},
        # {'type': 'datacentre', 'resource': 'CDL.DIGSCI+-+Digital+Science', 'country': 'United Kingdom'},
        # {'type': 'allocator', 'resource': 'BL+-+The+British+Library', 'country': 'United Kingdom'},
        # {'type': 'datacentre', 'resource': 'TIB+-+German+National+Library+of+Science+and+Technology', 'country': 'Germany'},
        {'type': 'allocator', 'resource': 'ANDS+-+Australian+National+Data+Service', 'country': 'Australia'},
        {'type': 'allocator', 'resource': 'CERN+-+CERN+-+European+Organization+for+Nuclear+Research',
         'country': 'Switzerland'},

    ]

    resource_types = [{'name': 'Collection', 'facet': '&fq=resourceType_facet:"Collection"'},
                      {'name': 'Dataset', 'facet': '&fq=resourceType_facet:"Dataset"'},
                      {'name': 'Text', 'facet': '&fq=resourceType_facet:"Text"'},
                      {'name': 'Software', 'facet': '&fq=resourceType_facet:"Software"'},
                      {'name': 'other', 'facet': '&fq=resourceType_facet:"Other"'},
                      {'name': 'Unknown', 'facet': "&fq=-resourceType_facet%3A[*+TO+*]"}
                      ]

    def harvest(self):
        os.makedirs(self._cachedir)

    def get_works(self):
        results = []
        for resource in self.search_space:
            for resource_type in self.resource_types:
                results += self.process_statistics(resource, resource_type['name'],
                                                   self.get_statistic(self._base_url, resource['type'],
                                                                      resource['resource'],
                                                                      self.date_field, self.start_date,
                                                                      self.end_date,
                                                                      resource_type['facet']))

            json.dump(results, open(os.path.join(self._cachedir, 'dois.json'), 'w'))
            return results


    def process_statistics(self, resource, resource_type, statistics):

        result = [{'country': resource['country'], 'institution': resource['resource'],
                   'data_key': resource_type, 'date': x, 'data_value': statistics['facet_counts']['facet_dates']['minted'][x]} for x in statistics['facet_counts']['facet_dates']['minted']]
        return result
