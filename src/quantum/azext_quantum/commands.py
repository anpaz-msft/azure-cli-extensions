# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from collections import OrderedDict

# pylint: disable=line-too-long
from azure.cli.core.commands import CliCommandType
from azext_quantum._client_factory import cf_offerings

from .operations.workspace import WorkspaceInfo

def validate_workspace_info(cmd, namespace):
    group = getattr(namespace, 'resource_group_name', None)
    name = getattr(namespace, 'name', None)
    ws = WorkspaceInfo(cmd, group, name)

    if not ws.subscription:
        raise ValueError("Missing subscription argument")
    if not ws.resource_group:
        raise ValueError("Missing resource-group argument")
    if not ws.name:
        raise ValueError("Missing workspace name argument")

def transform_job(result):
    result = OrderedDict([
        ('Id', result['id']),
        ('State', result['status']),
        ('Target', result['target']),
        ('Submission time', result['creationTime']),
        ('Completion time', result['endExecutionTime'])
    ])
    return result

def transform_jobs(results):
    return [transform_job(job) for job in results]

def load_command_table(self, _):

    workspace_ops = CliCommandType(operations_tmpl='azext_quantum.operations.workspace#{}')
    job_ops = CliCommandType(operations_tmpl='azext_quantum.operations.job#{}')
    offerings_ops = CliCommandType(
        operations_tmpl='azext_quantum.vendored_sdks.azure_mgmt_quantum.operations.offerings_operations#OfferingsOperations.{}',
        client_factory=cf_offerings
    )
    # target_ops = CliCommandType(operations_tmpl='azext_quantum.operations.target#{}')

    with self.command_group('quantum workspace', workspace_ops) as w:
        w.command('list', 'list')
        w.command('show', 'show', validator=validate_workspace_info)   ## TODO: argument list/help
        w.command('set', 'set', validator=validate_workspace_info)
        w.command('clear', 'clear')

    with self.command_group('quantum offers', offerings_ops) as w:
        w.command('list', 'list')   ## TODO: argument list/help

    # with self.command_group('quantum target', target_ops) as t:
    #     t.command('list', 'list_quantum')
    #     t.command('set', 'set')
    #     t.command('show', 'get')
    #     t.command('add', 'add')

    with self.command_group('quantum job', job_ops) as j:
        j.command('list', 'list', validator=validate_workspace_info, table_transformer=transform_jobs)
        j.command('show', 'show', validator=validate_workspace_info, table_transformer=transform_job)
    #     #g.custom_command('create', 'create_quantum')
    #     j.command('list', 'list')
    #     #j.show_command('show', 'get')
    #     # g.generic_update_command('update', setter_name='update', custom_func_name='update_quantum')


    with self.command_group('quantum', is_preview=True):
        pass
