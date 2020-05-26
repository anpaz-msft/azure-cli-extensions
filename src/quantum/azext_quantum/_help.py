# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.help_files import helps  # pylint: disable=unused-import


helps['quantum'] = """
    type: group
    short-summary: Manage Quantum Workspaces and submit jobs to Azure Quantum Providers.
"""

helps['quantum jobs list'] = """
    type: command
    short-summary: List the jobs of the current workspace.
"""

# helps['quantum delete'] = """
#     type: command
#     short-summary: Delete a Quantum.
# """

# helps['quantum show'] = """
#     type: command
#     short-summary: Show details of a Quantum.
# """

# helps['quantum update'] = """
#     type: command
#     short-summary: Update a Quantum.
# """
