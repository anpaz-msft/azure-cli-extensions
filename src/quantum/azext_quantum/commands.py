# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long
from azure.cli.core.commands import CliCommandType
from azext_quantum._client_factory import cf_workspaces, cf_jobs

def load_command_table(self, _):

    workspace_sdk = CliCommandType(
        operations_tmpl='azext_quantum.vendored_sdks.azure_mgmt_quantum.operations.workspaces_operations'
                        '#WorkspacesOperations.{}',
        client_factory=cf_workspaces
    )

    jobs_sdk = CliCommandType(
        operations_tmpl='azext_quantum.vendored_sdks.azure_mgmt_quantum.operations.workspaces_operations'
                        '#WorkspacesOperations.{}',
        client_factory=cf_jobs
    )

    with self.command_group('quantum workspace', workspace_sdk) as w:
        #g.custom_command('create', 'create_quantum')
        # g.command('delete', 'delete')
        #g.custom_command('list', 'list_quantum')
        w.show_command('show', 'get')
        # g.generic_update_command('update', setter_name='update', custom_func_name='update_quantum')

        
    with self.command_group('quantum jobs', jobs_sdk) as j:
        #g.custom_command('create', 'create_quantum')
        # g.command('delete', 'delete')
        #g.custom_command('list', 'list_quantum')
        j.show_command('show', 'get')
        # g.generic_update_command('update', setter_name='update', custom_func_name='update_quantum')


    with self.command_group('quantum', is_preview=True):
        pass
