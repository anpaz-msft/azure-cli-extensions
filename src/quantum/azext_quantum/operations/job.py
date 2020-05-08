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
    args = ["dotnet", "run"] if build else ["dotnet", "run", "--no-build"]
    subprocess.run(args)
    return

def output(cmd, job_id, resource_group_name=None, workspace_name=None):
    import io
    import tempfile
    import json
    from azure.cli.command_modules.storage._client_factory import blob_data_service_factory

    def parse_url(url):
        from urllib.parse import urlparse
        o = urlparse(url)

        account_name = o.netloc.split('.')[0]
        container = o.path.split('/')[-2]
        blob = o.path.split('/')[-1]
        sas_token = o.query

        return {
            "account_name": account_name,
            "container": container,
            "blob": blob,
            "sas_token": sas_token
        }

    info = WorkspaceInfo(cmd, resource_group_name, workspace_name)
    client = cf_jobs(cmd.cli_ctx, info.subscription, info.resource_group, info.name)
    job = client.get(job_id)

    if job.status != "Succeeded":
        return f"Job status: {job.status}. Output only available if Succeeded."

    args = parse_url(job.output_data_uri)
    blob_service = blob_data_service_factory(cmd.cli_ctx, args)

    path = tempfile.mktemp()
    blob_service.get_blob_to_path(args['container'], args['blob'], path)

    with open(path) as json_file:
        data = json.load(json_file)
        return data


