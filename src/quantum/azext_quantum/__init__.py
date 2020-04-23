# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core import AzCommandsLoader
from azure.cli.core.profiles import register_resource_type

from azext_quantum._help import helps  # pylint: disable=unused-import

from .profiles import QUANTUM_DATA, QUANTUM_MGMT

class QuantumCommandsLoader(AzCommandsLoader):

    def __init__(self, cli_ctx=None):
        from azure.cli.core.commands import CliCommandType
        from azext_quantum._client_factory import cf_quantum_mgmt
        quantum_custom = CliCommandType(
            operations_tmpl='azext_quantum.custom#{}',
            client_factory=cf_quantum_mgmt)
        super(QuantumCommandsLoader, self).__init__(cli_ctx=cli_ctx,
                                                  custom_command_type=quantum_custom)

    def load_command_table(self, args):
        from azext_quantum.commands import load_command_table
        load_command_table(self, args)
        return self.command_table

    def load_arguments(self, command):
        from azext_quantum._params import load_arguments
        load_arguments(self, command)


COMMAND_LOADER_CLS = QuantumCommandsLoader
