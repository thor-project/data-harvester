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

DATACITE_RESOURCE_TYPES = [
    {'name': 'Collection', 'facet': '&fq=resourceType_facet:"Collection"'},
    {'name': 'Image', 'facet': '&fq=resourceType_facet:"Image"'},
    {'name': 'Audiovisual', 'facet': '&fq=resourceType_facet:"Audiovisual"'},
    {'name': 'Even', 'facet': '&fq=resourceType_facet:"Event"'},
    {'name': 'Film', 'facet': '&fq=resourceType_facet:"Film"'},
    {'name': 'Sound', 'facet': '&fq=resourceType_facet:"Sound"'},
    {'name': 'Model', 'facet': '&fq=resourceType_facet:"Model"'},
    {'name': 'Interactive resource', 'facet': '&fq=resourceType_facet:"InteractiveResource"'},
    {'name': 'Dataset', 'facet': '&fq=resourceType_facet:"Dataset"'},
    {'name': 'Workflow', 'facet': '&fq=resourceType_facet:"Workflow"'},
    {'name': 'Service', 'facet': '&fq=resourceType_facet:"Service"'},
    {'name': 'Text', 'facet': '&fq=resourceType_facet:"Text"'},
    {'name': 'Physical object', 'facet': '&fq=resourceType_facet:"PhysicalObject"'},
    {'name': 'Software', 'facet': '&fq=resourceType_facet:"Software"'},
    {'name': 'other', 'facet': '&fq=resourceType_facet:"Other"'},
    {'name': 'Unclassified', 'facet': "&fq=-resourceType_facet%3A[*+TO+*]"}
]

DATACITE_RESTRICTIONS = [{'name': 'with_orcids', 'query': 'nameIdentifier:ORCID%5C:*'},
                         {'name': 'without_orcids', 'query': '*'}]
