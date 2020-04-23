# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.util import CLIError


def create_quantum(cmd, resource_group_name, quantum_name, location=None, tags=None):
    raise CLIError('TODO: Implement `quantum create`')


def list_quantum(cmd, resource_group_name=None):
    raise CLIError('TODO: Implement `quantum list`')


def update_quantum(cmd, instance, tags=None):
    with cmd.update_context(instance) as c:
        c.set_param('tags', tags)
    return instance