# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from .._client_factory import cf_jobs

def list(cmd, subscription_id=None, resource_group_name=None, workspace_name=None):
    client = cf_jobs(cmd.cli_ctx, subscription_id, resource_group_name, workspace_name)
    return client.list()