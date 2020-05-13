# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=import-outside-toplevel

import logging

from .._client_factory import cf_jobs, _get_data_credentials, base_url
from .workspace import WorkspaceInfo
from .target import TargetInfo
from knack.util import CLIError

logger = logging.getLogger(__name__)

# pylint: disable=redefined-builtin
def list(cmd, resource_group_name=None, workspace_name=None):
    """
    Returns the list of jobs in a Quantum Workspace.
    """
    info = WorkspaceInfo(cmd, resource_group_name, workspace_name)
    client = cf_jobs(cmd.cli_ctx, info.subscription, info.resource_group, info.name)
    return client.list()


def show(cmd, job_id, resource_group_name=None, workspace_name=None):
    """
    Shows the job's status and details.
    """
    info = WorkspaceInfo(cmd, resource_group_name, workspace_name)
    client = cf_jobs(cmd.cli_ctx, info.subscription, info.resource_group, info.name)
    return client.get(job_id)


def submit(cmd, program_args, resource_group_name=None, workspace_name=None, target_id=None, project=None, build=False):
    """
    Submits a Q# program for execution to Azure Quantum.
    """
    import os

    ws = WorkspaceInfo(cmd, resource_group_name, workspace_name)
    target = TargetInfo(cmd, target_id)
    token = _get_data_credentials(cmd.cli_ctx, ws.subscription).get_token().token

    args = ["dotnet", "run"]
    if not build:
        args.append("--no-build")

    if project:
        args.append("--project")
        args.append(project)

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

    args.append("--storage")
    args.append(os.environ['AZURE_QUANTUM_STORAGE'])

    args.append("--aad-token")
    args.append(token)

    args.append("--base-uri")
    args.append(base_url())

    args.extend(program_args)

    logger.debug(args)

    import subprocess
    result = subprocess.run(args, stdout=subprocess.PIPE, check=False)

    if result.returncode == 0:
        job_id = result.stdout.decode('ascii').strip()  
        return { 'job_id': job_id }

    raise CLIError("Failed to submit job.")

def output(cmd, job_id, resource_group_name=None, workspace_name=None):
    import tempfile
    import json
    import os
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

    path = os.path.join(tempfile.gettempdir(), job_id)
    if os.path.exists(path):
        logger.debug(f"Using existing blob from {path}")
    else:
        logger.debug(f"Downloading job results blob into {path}")

        info = WorkspaceInfo(cmd, resource_group_name, workspace_name)
        client = cf_jobs(cmd.cli_ctx, info.subscription, info.resource_group, info.name)
        job = client.get(job_id)

        if job.status != "Succeeded":
            return f"Job status: {job.status}. Output only available if Succeeded."

        args = parse_url(job.output_data_uri)
        blob_service = blob_data_service_factory(cmd.cli_ctx, args)
        blob_service.get_blob_to_path(args['container'], args['blob'], path)

    with open(path) as json_file:
        data = json.load(json_file)
        return data


def wait(cmd, job_id, resource_group_name=None, workspace_name=None, max_poll_wait_secs=5):
    """
    Place the CLI in a waiting state until the job finishes execution.
    """
    import time

    def has_completed(job):
        return (
            job.status == "Succeeded" or
            job.status == "Failed" or
            job.status == "Cancelled"
        )

    info = WorkspaceInfo(cmd, resource_group_name, workspace_name)
    client = cf_jobs(cmd.cli_ctx, info.subscription, info.resource_group, info.name)

    # TODO: LROPoller...
    w = False
    poll_wait = 0.2
    job = client.get(job_id)

    while not has_completed(job):
        print('.', end='', flush=True)
        w = True
        time.sleep(poll_wait)
        job = client.get(job_id)
        poll_wait = max_poll_wait_secs if poll_wait >= max_poll_wait_secs else poll_wait * 1.5

    if w:
        print("")

    return job

def execute(cmd, program_args, resource_group_name=None, workspace_name=None, target_id=None, project=None, build=False):
    """
    Executes a Q# project on Azure Quantum.

    Submits a job, waits for completion and returns back a histogram with the results distribution.
    """
    job = submit(cmd, program_args, resource_group_name, workspace_name, target_id, project, build)
    print("Job id:", job['job_id'])
    logger.debug(job)

    job = wait(cmd, job['job_id'], resource_group_name, workspace_name)
    logger.debug(job)

    if not job.status == "Succeeded":
        return job

    return output(cmd, job.id, resource_group_name, workspace_name)
