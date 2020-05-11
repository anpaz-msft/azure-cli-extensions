# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from .._client_factory import cf_workspaces

class TargetInfo(object):
    def __init__(self, cmd, target_id=None):

        def select_value(key, value):
            if not value is None:
                return value
            value = cmd.cli_ctx.config.get('quantum', key, None)
            if not value is None:
                return value
            value = cmd.cli_ctx.config.get(cmd.cli_ctx.config.defaults_section_name, key, None)
            if not value is None:
                return value

        self.target_id = select_value('target_id', target_id)

    def clear(self):
        self.target_id = ''

    def save(self, cmd):
        from azure.cli.core.util import ConfiguredDefaultSetter

        with ConfiguredDefaultSetter(cmd.cli_ctx.config, False):
            cmd.cli_ctx.config.set_value('quantum', 'target_id', self.target_id)


def show(cmd, target_id=None):
    info = TargetInfo(cmd, target_id)
    return info

def set(cmd, target_id=None):
    #TODO: Validate target.
    info = TargetInfo(cmd, target_id)
    if info:
        info.save(cmd)

def clear(cmd):
    info = TargetInfo(cmd)
    info.clear()
    info.save(cmd)
    return
