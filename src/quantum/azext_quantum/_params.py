# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long

from knack.arguments import CLIArgumentType

def load_arguments(self, _):
    workspace_name_type = CLIArgumentType(options_list=['--workspace-name', '-w'], help='Name of the Quantum Workspace. You can configure the default workspace using `az quantum workspace set`.', id_part=None, required=False)
    program_args = CLIArgumentType(nargs='*', help='List of arguments expected by the Q# operation specified as --name=value after `--`.')

    with self.argument_context('quantum workspace') as c:
        c.argument('workspace_name', workspace_name_type)

    with self.argument_context('quantum target') as c:
        c.argument('workspace_name', workspace_name_type)
        c.argument('target_id', options_list=['--target-id', '-t'], help='Target id.')

    with self.argument_context('quantum job') as c:
        c.argument('workspace_name', workspace_name_type)
        c.argument('job_id', options_list=['--job-id', '-id'], help='Job id.')
        c.argument('target_id', options_list=['--target-id', '-t'], help='Target id.')
        c.positional('program_args', program_args)

    with self.argument_context('quantum execute') as c:
        c.argument('workspace_name', workspace_name_type)
        c.argument('target_id', options_list=['--target-id', '-t'], help='Target id.')
        c.positional('program_args', program_args)
