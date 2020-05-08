# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from .._client_factory import cf_workspaces
from azure.cli.core.commands.client_factory import get_subscription_id

def list(cmd, resource_group_name=None, tag=None, location=None):
    from azure.cli.command_modules.resource.custom import list_resources
    return list_resources(cmd, resource_group_name=resource_group_name, resource_type="Microsoft.Quantum/Workspaces", tag=tag, location=location)

def show(cmd):
    subscription = get_subscription_id(cmd.cli_ctx)
    _resource_client_factory
    print(subscription)
    