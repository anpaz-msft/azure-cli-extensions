# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=redefined-builtin

import logging

from knack.util import CLIError

from .._client_factory import cf_jobs, _get_data_credentials, base_url
from .workspace import WorkspaceInfo
from .target import TargetInfo

logger = logging.getLogger(__name__)


def to_notebook(job):
    return {
        "name": job.name,
        "endpoint": job.notebook_endpoint
    }

def list(cmd, resource_group_name=None, workspace_name=None):
    """
    Get the list of notebooks in a Quantum Workspace.
    """
    info = WorkspaceInfo(cmd, resource_group_name, workspace_name)
    client = cf_jobs(cmd.cli_ctx)

    def is_notebook(job):
        return job.status == "Running"

    all_jobs = client.list_by_account(resource_group_name=info.resource_group, account_name=info.name)
    return [to_notebook(job) for job in all_jobs if is_notebook(job)]



def launch(cmd, job_id, resource_group_name=None, workspace_name=None):
    """
    Get the job's status and details.
    """
    import webbrowser 
    
    info = WorkspaceInfo(cmd, resource_group_name, workspace_name)
    client = cf_jobs(cmd.cli_ctx)
    job = client.get(info.resource_group, info.name, job_id)

    webbrowser.open(job.notebook_endpoint) 


def create(cmd, job_id, resource_group_name=None, workspace_name=None):
    """
    Submit a new Job to run a Jupyter notebook 
    """
    from ..vendored_sdks.aisc.models import JobResourceDescription, PlacementPolicy, FrameworkImageBase, InstanceTypeSettings, ScalePolicy, PyTorchFrameworkImage, StorageLocation, StorageMount, StorageSourceAzureBlob, StorageSourceKind

    info = WorkspaceInfo(cmd, resource_group_name, workspace_name)
    client = cf_jobs(cmd.cli_ctx)

    instanceType = InstanceTypeSettings( 
        instance_type= "AISupercomputer.D1",  
        scale_policy = ScalePolicy( current_instance_type_count=1 )
    )

    placementPolicy = PlacementPolicy(
        instance_types= [ instanceType ],
        location="westus2"
    )

    return client.begin_create_or_update(
        resource_group_name=info.resource_group,
        account_name=info.name,
        job_name= job_id,
        placement_policies= [ placementPolicy ], 
        framework_image = PyTorchFrameworkImage()
    )

