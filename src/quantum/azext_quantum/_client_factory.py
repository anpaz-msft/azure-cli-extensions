# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from .profiles import QUANTUM_DATA

def cf_quantum(cli_ctx, subscription_id=None, resource_group_name=None, workspace_name=None):
    from .vendored_sdks.azure_quantum import QuantumClient
    from azure.cli.core._profile import Profile
    profile = Profile(cli_ctx=cli_ctx)
    cred, subscription_id, _ = profile.get_login_credentials(subscription_id=subscription_id, resource="https://quantum.microsoft.com")
    return QuantumClient(cred, subscription_id, resource_group_name, workspace_name, base_url="https://app-jobs-canarysouthcentralus.azurewebsites.net/")

def cf_quantum_mgmt(cli_ctx, *_):
    from azure.cli.core.commands.client_factory import get_mgmt_service_client
    from .vendored_sdks.azure_mgmt_quantum import QuantumManagementClient
    return get_mgmt_service_client(cli_ctx, QuantumManagementClient)

def cf_workspaces(cli_ctx, *_):
    return cf_quantum_mgmt(cli_ctx).workspaces

def cf_offerings(cli_ctx, *_):
    return cf_quantum_mgmt(cli_ctx).offerings

def cf_jobs(cli_ctx, subscription_id=None, resource_group_name=None, workspace_name=None):
    return cf_quantum(cli_ctx, subscription_id, resource_group_name, workspace_name).jobs
