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

ORCID_STATISTICS = ['liveIds', 'idsWithWorks', 'idsWithVerifiedEmail', 'uniqueDois', 'works',
                               'worksWithDois', 'funding', 'education', 'employment']

DATACITE_ALLOCATOR_SEARCH_SPACE = [

    {'type': 'allocator',
     'resource': 'ANDS+-+Australian+National+Data+Service',
     'country': 'Australia'},
    {'type': 'allocator', 'resource': 'BL+-+The+British+Library',
     'country': 'United Kingdom'},
    {'type': 'allocator', 'resource': 'CDL+-+California+Digital+Library',
     'country': 'United States'},
    {'type': 'allocator',
     'resource': 'CERN+-+CERN+-+European+Organization+for+Nuclear+Research',
     'country': 'Switzerland'},
    {'type': 'allocator',
     'resource': 'CISTI+-+National+Research+Council+Canada',
     'country': 'Canada'},
    {'type': 'allocator', 'resource': 'CRUI+-+CRUI2011', 'country': 'Italy'},
    {'type': 'allocator', 'resource': 'DELFT+-+TU+Delft+Library',
     'country': 'Holland'},
    {'type': 'allocator',
     'resource': 'DK+-+Technical+Information+Center+of+Denmark',
     'country': 'Denmark'},
    {'type': 'allocator', 'resource': 'ESTDOI+-+Tartu+University',
     'country': 'Estonia'},
    {'type': 'allocator', 'resource': 'ETHZ+-+ETH+Zurich',
     'country': 'Switzerland'},
    {'type': 'allocator',
     'resource': 'GESIS+-+GESIS+-+Leibniz+Institute+for+the+Social+Sciences',
     'country': 'Germany'},
    {'type': 'allocator',
     'resource': 'INIST+-+Institute+for+Scientific+and+Technical+Information',
     'country': 'France'},
    {'type': 'allocator', 'resource': 'MTAKIK+-+MTA+Könyvtára',
     'country': 'Hungary'},
    {'type': 'allocator', 'resource': 'SND+-+Swedish+National+Data+Service',
     'country': 'Sweden'},

    {'type': 'allocator',
     'resource': 'NRCT+-+National+Research+Council+of+Thailand',
     'country': 'Thailand'},

    {'type': 'allocator',
     'resource': 'OSTI+-+Office+of+Scientific+and+Technical+Information+(OSTI)%2C+US+Department+of+Energy',
     'country': 'United States'},

    {'type': 'allocator', 'resource': 'PURDUE+-+Purdue+University+Library',
     'country': 'United States'},
    {'type': 'allocator',
     'resource': 'SUBGOE+-+Niedersächsische+Staats-+und+Universitätsbibliothek+Göttingen',
     'country': 'Germany'},

    {'type': 'allocator',
     'resource': 'TIB+-+German+National+Library+of+Science+and+Technology',
     'country': 'Germany'},

    {'type': 'allocator',
     'resource': 'ZBMED+-+German+National+Library+of+Medicine',
     'country': 'Germany'},
    {'type': 'allocator',
     'resource': 'ZBW+-+Deutsche+Zentralbibliothek+für+Wirtschaftswissenschaften+–+Leibniz-Informationszentrum+Wirtschaft',
     'country': 'Germany'}

]

DATACITE_RESOURCE_TYPES = [
    {'name': 'Collection', 'facet': '&fq=resourceType_facet:"Collection"'},
    {'name': 'Dataset', 'facet': '&fq=resourceType_facet:"Dataset"'},
    {'name': 'Text', 'facet': '&fq=resourceType_facet:"Text"'},
    {'name': 'Software', 'facet': '&fq=resourceType_facet:"Software"'},
    {'name': 'other', 'facet': '&fq=resourceType_facet:"Other"'},
    {'name': 'Unclassified', 'facet': "&fq=-resourceType_facet%3A[*+TO+*]"}
    ]

DATACITE_RESTRICTIONS = [{'name': 'with_orcids', 'query': 'nameIdentifier:ORCID%5C:*'},
                {'name': 'without_orcids', 'query': '*'}]
