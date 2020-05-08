# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long

from knack.arguments import CLIArgumentType


def load_arguments(self, _):

    from azure.cli.core.commands.parameters import tags_type
    from azure.cli.core.commands.validators import get_default_location_from_resource_group

    workspace_name_type = CLIArgumentType(options_list=['--workspace-name', '-w'], help='Name of the Quantum Workspace. You can configure the default workspace using `az quantum workspace set`.', id_part=None, required=False)

    with self.argument_context('quantum workspace') as c:
        c.argument('name', workspace_name_type)

    with self.argument_context('quantum job') as c:
        c.argument('workspace_name', workspace_name_type)
