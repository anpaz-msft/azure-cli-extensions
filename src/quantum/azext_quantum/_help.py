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

helps['quantum job'] = """
    type: group
    short-summary: Manage jobs for Azure Quantum.
"""

helps['quantum target'] = """
    type: command
    short-summary: Manage execution targets for Azure Quantum workspaces.
"""

helps['quantum job submit'] = """
    type: command
    short-summary: Submits a job for quantum execution on Azure Quantum.
"""

helps['quantum execute'] = """
    type: command
    short-summary: Submits a job for quantum execution on Azure Quantum, and waits for the result.
"""
