# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class TargetStatus(Model):
    """Target status.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar id: Target id.
    :vartype id: str
    :ivar current_availability: Target availability. Possible values include:
     'Available', 'Degraded', 'Unavailable'
    :vartype current_availability: str or ~quantum.models.TargetAvailability
    :ivar average_queue_time: Average queue time in seconds.
    :vartype average_queue_time: long
    :ivar status_page: A page with detailed status of the provider.
    :vartype status_page: str
    """

    _validation = {
        'id': {'readonly': True},
        'current_availability': {'readonly': True},
        'average_queue_time': {'readonly': True},
        'status_page': {'readonly': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'current_availability': {'key': 'currentAvailability', 'type': 'str'},
        'average_queue_time': {'key': 'averageQueueTime', 'type': 'long'},
        'status_page': {'key': 'statusPage', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(TargetStatus, self).__init__(**kwargs)
        self.id = None
        self.current_availability = None
        self.average_queue_time = None
        self.status_page = None
