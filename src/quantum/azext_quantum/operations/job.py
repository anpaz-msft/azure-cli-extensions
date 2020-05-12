# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from .._client_factory import cf_jobs, _get_data_credentials, base_url
from .workspace import WorkspaceInfo
from .target import TargetInfo

def list(cmd, resource_group_name=None, workspace_name=None):
    info = WorkspaceInfo(cmd, resource_group_name, workspace_name)
    client = cf_jobs(cmd.cli_ctx, info.subscription, info.resource_group, info.name)
    return client.list()


def show(cmd, job_id, resource_group_name=None, workspace_name=None):
    info = WorkspaceInfo(cmd, resource_group_name, workspace_name)
    client = cf_jobs(cmd.cli_ctx, info.subscription, info.resource_group, info.name)
    return client.get(job_id)


def submit(cmd, program_args, resource_group_name=None, workspace_name=None, target_id=None, build=False):
    import os

    ws = WorkspaceInfo(cmd, resource_group_name, workspace_name)
    target = TargetInfo(cmd, target_id)
    token = _get_data_credentials(cmd.cli_ctx, ws.subscription).get_token().token

    args = ["dotnet", "run"]
    if not build:
        args.append("--no-build")

    args.append("--")
    args.append("submit")

    args.append("--subscription")
    args.append(ws.subscription)

    args.append("--resource-group")
    args.append(ws.resource_group)

    args.append("--workspace")
    args.append(ws.name)

    args.append("--target")
    args.append(target.target_id)

    args.append("--output")
    args.append("Id")

    if not ('AZURE_QUANTUM_STORAGE' in os.environ):
        raise ValueError(f"Please set the AZURE_QUANTUM_STORAGE environment variable with an Azure Storage's connection string")

    args.append("--storage")
    args.append(os.environ['AZURE_QUANTUM_STORAGE'])

    args.append("--aad-token")
    args.append(token)

    args.append("--base-uri")
    args.append(base_url())

    args.extend(program_args)

    import subprocess
    result = subprocess.run(args, stdout=subprocess.PIPE, check=False)

    if (result.returncode == 0):
        job_id = result.stdout    
        return { 'job_id': job_id }

    raise ValueError("Failed to submit job.")

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


