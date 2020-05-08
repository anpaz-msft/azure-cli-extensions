# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

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

def load_command_table(self, _):

    workspace_ops = CliCommandType(operations_tmpl='azext_quantum.operations.workspace#{}')
    offerings_ops = CliCommandType(
        operations_tmpl='azext_quantum.vendored_sdks.azure_mgmt_quantum.operations.offerings_operations#OfferingsOperations.{}',
        client_factory=cf_offerings
        )
    # target_ops = CliCommandType(operations_tmpl='azext_quantum.operations.target#{}')
    # job_ops = CliCommandType(operations_tmpl='azext_quantum.operations.job#{}')

    with self.command_group('quantum workspace', workspace_ops) as w:
        w.command('list', 'list')
        w.command('show', 'show', validator=validate_workspace_info)   ## TODO: argument list/help
        w.command('set', 'set', validator=validate_workspace_info)
        # w.command('get', 'get')
        # w.show_command('show', 'get')
        # w.custom_command('set', 'get')

    with self.command_group('quantum offers', offerings_ops) as w:
        w.command('list', 'list')   ## TODO: argument list/help

    # with self.command_group('quantum target', target_ops) as t:
    #     t.command('list', 'list_quantum')
    #     t.command('set', 'set')
    #     t.command('show', 'get')
    #     t.command('add', 'add')

    # with self.command_group('quantum jobs', job_ops) as j:
    #     #g.custom_command('create', 'create_quantum')
    #     #j.show_command('list', 'list')
    #     j.command('list', 'list')
    #     #j.show_command('show', 'get')
    #     # g.generic_update_command('update', setter_name='update', custom_func_name='update_quantum')


    with self.command_group('quantum', is_preview=True):
        pass
