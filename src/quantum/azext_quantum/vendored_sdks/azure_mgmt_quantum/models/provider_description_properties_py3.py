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

from .provider_properties_py3 import ProviderProperties


class ProviderDescriptionProperties(ProviderProperties):
    """A list of Provider-specific properties.

    :param description: Description about this Provider.
    :type description: str
    :param provider_type: Provider type.
    :type provider_type: str
    :param company: Company name.
    :type company: str
    :param default_endpoint: Provider's default endpoint.
    :type default_endpoint: str
    :param aad: Azure Active Directory info.
    :type aad: ~quantum.models.ProviderPropertiesAad
    :param managed_application: Provider's Managed-Application info
    :type managed_application:
     ~quantum.models.ProviderPropertiesManagedApplication
    :param targets: The list of targets available from this provider
    :type targets: list[~quantum.models.TargetDescription]
    :param skus: The list of skus selected for this provider
    :type skus: list[~quantum.models.SkuDescription]
    """

    _attribute_map = {
        'description': {'key': 'description', 'type': 'str'},
        'provider_type': {'key': 'providerType', 'type': 'str'},
        'company': {'key': 'company', 'type': 'str'},
        'default_endpoint': {'key': 'defaultEndpoint', 'type': 'str'},
        'aad': {'key': 'aad', 'type': 'ProviderPropertiesAad'},
        'managed_application': {'key': 'managedApplication', 'type': 'ProviderPropertiesManagedApplication'},
        'targets': {'key': 'targets', 'type': '[TargetDescription]'},
        'skus': {'key': 'skus', 'type': '[SkuDescription]'},
    }

    def __init__(self, *, description: str=None, provider_type: str=None, company: str=None, default_endpoint: str=None, aad=None, managed_application=None, targets=None, skus=None, **kwargs) -> None:
        super(ProviderDescriptionProperties, self).__init__(description=description, provider_type=provider_type, company=company, default_endpoint=default_endpoint, aad=aad, managed_application=managed_application, targets=targets, skus=skus, **kwargs)
