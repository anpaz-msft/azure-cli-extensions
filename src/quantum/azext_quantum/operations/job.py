# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from .._client_factory import cf_jobs
from .workspace import WorkspaceInfo

def list(cmd, resource_group_name=None, workspace_name=None):
    info = WorkspaceInfo(cmd, resource_group_name, workspace_name)
    client = cf_jobs(cmd.cli_ctx, info.subscription, info.resource_group, info.name)
    return client.list()

    
def show(cmd, job_id, resource_group_name=None, workspace_name=None):
    info = WorkspaceInfo(cmd, resource_group_name, workspace_name)
    client = cf_jobs(cmd.cli_ctx, info.subscription, info.resource_group, info.name)
    return client.get(job_id)

    
def submit(cmd, resource_group_name=None, workspace_name=None, build=False):
    WorkspaceInfo(cmd, resource_group_name, workspace_name)
    import subprocess
    args = ["dotnet", "run", "" if build else "--no-build"]
    print("args:", args)
    subprocess.run(args)
    return