#!/usr/bin/env python
# -*- coding: utf-8 -*-
<<<<<<< HEAD
<<<<<<< HEAD
#
# (C) Copyright 2019 Hewlett Packard Enterprise Development LP.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

import copy
import json
=======

# (C) Copyright 2019-2020 Hewlett Packard Enterprise Development LP.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import copy
import json
import requests
import re
from ansible.module_utils._text import to_text
<<<<<<< HEAD
>>>>>>> b72fff9... Adds 10.4 support to modules
=======

# (C) Copyright 2019-2020 Hewlett Packard Enterprise Development LP.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import copy
import json
import requests
from ansible.module_utils._text import to_text
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4
=======
from ansible.module_utils.basic import env_fallback
>>>>>>> da0d435... New modules and bug fixes
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.common.utils import to_list, ComplexList
from ansible.module_utils.connection import exec_command, Connection, ConnectionError

_DEVICE_CONNECTION = None

_DEVICE_CONFIGS = {}

aoscx_provider_spec = {
    'host': dict(),
    'port': dict(type='int'),
    'username': dict(fallback=(env_fallback, ['ANSIBLE_NET_USERNAME'])),
    'password': dict(fallback=(env_fallback, ['ANSIBLE_NET_PASSWORD']), no_log=True),
    'ssh_keyfile': dict(fallback=(env_fallback, ['ANSIBLE_NET_SSH_KEYFILE']), type='path'),
    'authorize': dict(fallback=(env_fallback, ['ANSIBLE_NET_AUTHORIZE']), type='bool'),
    'auth_pass': dict(fallback=(env_fallback, ['ANSIBLE_NET_AUTH_PASS']), no_log=True),
    'timeout': dict(type='int')
}

aoscx_http_provider_spec = {
    'host': dict(),
    'port': dict(type='int'),
    'username': dict(fallback=(env_fallback, ['ANSIBLE_NET_USERNAME'])),
    'password': dict(fallback=(env_fallback, ['ANSIBLE_NET_PASSWORD']), no_log=True)
}

aoscx_argument_spec = {
    'provider': dict(type='dict', options=aoscx_provider_spec, removed_in_version=2.14),
}

aoscx_http_argument_spec = {
    'provider': dict(type='dict', options=aoscx_http_provider_spec, removed_in_version=2.14),
}

def get_provider_argspec():
    '''
    Returns the provider argument specification
    '''
    return aoscx_provider_spec

def check_args(module, warnings):
    '''
    Checks the argument
    '''
    pass

def get_config(module, flags=None):
    '''
    Obtains the switch configuration
    '''
    flags = [] if flags is None else flags

    cmd = 'show running-config '
    cmd += ' '.join(flags)
    cmd = cmd.strip()

    try:
        return _DEVICE_CONFIGS[cmd]
    except KeyError:
        rc, out, err = exec_command(module, cmd)
        if rc != 0:
            module.fail_json(msg='unable to retrieve current config', stderr=to_text(err, errors='surrogate_then_replace'))
        cfg = to_text(out, errors='surrogate_then_replace').strip()
        _DEVICE_CONFIGS[cmd] = cfg
        return cfg

def load_config(module, commands):
    '''
    Loads the configuration onto the switch
    '''
    rc, out, err = exec_command(module, 'configure terminal')
    if rc != 0:
        module.fail_json(msg='unable to enter configuration mode', err=to_text(out, errors='surrogate_then_replace'))

    for command in to_list(commands):
        if command == 'end':
            continue
        rc, out, err = exec_command(module, command)
        if rc != 0:
            module.fail_json(msg=to_text(err, errors='surrogate_then_replace'), command=command, rc=rc)

    exec_command(module, 'end')


def sanitize(resp):
    '''
    Sanitizes the string to remove additiona white spaces
    '''
    # Takes response from device and adjusts leading whitespace to just 1 space
    cleaned = []
    for line in resp.splitlines():
        cleaned.append(re.sub(r"^\s+", " ", line))
    return '\n'.join(cleaned).strip()

class HttpApi:
    '''
    Module utils class for AOS-CX HTTP API connection
    '''
    def __init__(self, module):
        self._module = module
        self._connection_obj = None

    @property
    def _connection(self):
        '''
        Creates HTTP API connection
        '''
        if not self._connection_obj:
            self._connection_obj = Connection(self._module._socket_path)
        return self._connection_obj

<<<<<<< HEAD
<<<<<<< HEAD
    def get_running_config(self):
        return self._connection.get_running_config()
=======
=======
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4
    def get(self, url, data=None):
        '''
        GET REST call
        '''
        res = self._connection.send_request(data=data, method='GET', path=url)
        return res

    def put(self, url, data=None, headers={}):
        '''
        PUT REST call
        '''
        return self._connection.send_request(data=data, method='PUT', path=url,
                                             headers=headers)

    def post(self, url, data=None, headers={}):
        '''
        POST REST call
        '''
        return self._connection.send_request(data=data, method='POST',
                                             path=url,
                                             headers=headers)

    def file_upload(self, url, files, headers={}):
        """
        Workaround with requests library for lack of support in httpapi for
        multipart POST
        See:
        ansible/blob/devel/lib/ansible/plugins/connection/httpapi.py
        ansible/blob/devel/lib/ansible/module_utils/urls.py
        """
        connection_details = self._connection.get_connection_details()
        if 'auth'in connection_details.keys():
            headers.update(connection_details['auth'])

        full_url = connection_details['url'] + url
        with open(files, 'rb') as file:
            file_param = {'fileupload': file}
            # Workaround for setting no_proxy based off acx_no_proxy flag
            if connection_details['no_proxy']:
                proxies = {'http': None, 'https': None}
                res = requests.post(
                    url=full_url, files=file_param, verify=False,
                    proxies=proxies, headers=headers)
            else:
                res = requests.post(
                    url=full_url, files=file_param, verify=False,
                    headers=headers)
        if res.status_code != 200:
            error_text = "Error while uploading firmware"
            raise ConnectionError(error_text, code=res.status_code)
        return res
<<<<<<< HEAD
>>>>>>> b72fff9... Adds 10.4 support to modules
=======
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4

def get_connection(module, is_cli=False):
    '''
    Returns the connection plugin
    '''
    global _DEVICE_CONNECTION
    if not _DEVICE_CONNECTION:
        if is_cli:
            if hasattr(module, '_aoscx_connection'):
                _DEVICE_CONNECTION = module._aoscx_connection
                return module._aoscx_connection
            module._aoscx_connection = Connection(module._socket_path)
            _DEVICE_CONNECTION = module._aoscx_connection
            return module._aoscx_connection
        else:
            conn = HttpApi(module)
        _DEVICE_CONNECTION = conn
    return _DEVICE_CONNECTION


def get(module, url, data=None):
    '''
    Perform GET REST call
    '''
    conn = get_connection(module)
    res = conn.get(url, data)
    return res

<<<<<<< HEAD
<<<<<<< HEAD
def put_running_config(module, updated_config):
    conn = get_connection(module)
    conn.put_running_config(updated_config)
=======

def put(module, url, data=None, headers={}):
    '''
    Perform PUT REST call
    '''
    conn = get_connection(module)
    res = conn.put(url, data, headers)
    return res


def post(module, url, data=None, headers={}):
    '''
    Perform POST REST call
    '''
    conn = get_connection(module)
    res = conn.post(url, data, headers)
    return res


def file_upload(module, url, files, headers={}):
    '''
    Upload File through REST
    '''
    conn = get_connection(module)
    res = conn.file_upload(url, files, headers)
    return res

<<<<<<< HEAD
=======

def put(module, url, data=None, headers={}):
    conn = get_connection(module)
    res = conn.put(url, data, headers)
    return res
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4

class Cli:
    def __init__(self, module):
        self._module = module
        self._connection_obj = None
>>>>>>> b72fff9... Adds 10.4 support to modules

<<<<<<< HEAD

<<<<<<< HEAD
class ArubaAnsibleModule:
=======
    def run_commands(self, commands, check_rc=True):
        """Run list of commands on remote device and return results
        """
        connection = self._connection_obj
        try:
            response = connection.run_commands(commands=commands,
                                               check_rc=check_rc)
        except ConnectionError as exc:
            self._module.fail_json(msg=to_text(exc,
                                               errors='surrogate_then_replace')
                                   )
        return response
>>>>>>> b72fff9... Adds 10.4 support to modules
=======
def post(module, url, data=None, headers={}):
    conn = get_connection(module)
    res = conn.post(url, data, headers)
    return res


def file_upload(module, url, files, headers={}):
    conn = get_connection(module)
    res = conn.file_upload(url, files, headers)
    return res

>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4

class Cli:
    def __init__(self, module):
        self._module = module
        self._connection_obj = None

    @property
    def _connection(self):
        if not self._connection_obj:
            self._connection_obj = Connection(self._module._socket_path)
        return self._connection_obj

    def run_commands(self, commands, check_rc=True):
        """Run list of commands on remote device and return results
        """
        connection = self._connection_obj
        try:
            response = connection.run_commands(commands=commands,
                                               check_rc=check_rc)
        except ConnectionError as exc:
            self._module.fail_json(msg=to_text(exc,
                                               errors='surrogate_then_replace')
                                   )
        return response
=======
def to_command(module, commands):

    '''
    Convert command to ComplexList
    '''
    transform = ComplexList(dict(
        command=dict(key=True),
        prompt=dict(type='list'),
        answer=dict(type='list'),
        newline=dict(type='bool', default=True),
        sendonly=dict(type='bool', default=False),
        check_all=dict(type='bool', default=False),
    ), module)

    return transform(to_list(commands))

def run_commands(module, commands, check_rc=False):
    '''
    Execute command on the switch
    '''
    conn = get_connection(module, True)
    try:
        return conn.run_commands(commands=commands, check_rc=check_rc)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))
>>>>>>> da0d435... New modules and bug fixes


class ArubaAnsibleModule:
    '''
    Aruba ansible mdule wrapper class
    '''

    def __init__(self, module_args, store_config=True):
        '''
        module init function
        '''

        self.module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True
        )

        self.warnings = list()
        self.changed = False
<<<<<<< HEAD
<<<<<<< HEAD
        self.get_switch_config()

    def get_switch_config(self):
=======
        self.original_config = None
        self.running_config = None
        self.switch_current_firmware = None
        self.switch_platform = None
        self.get_switch_platform()
        self.get_switch_firmware_version()
        self.get_switch_config(store_config=store_config)

        if "10.00" in self.switch_current_firmware:
            self.module.fail_json(msg="Minimum supported "
                                      "firmware version is 10.03")

        if "10.01" in self.switch_current_firmware:
            self.module.fail_json(msg="Minimum supported "
                                      "firmware version is 10.03")

        if "10.02" in self.switch_current_firmware:
            self.module.fail_json(msg="Minimum supported "
                                      "firmware version is 10.03")

    def get_switch_platform(self):
        platform_url = '/rest/v1/system?attributes=platform_name'
        platform = get(self.module, platform_url)
        self.switch_platform = platform["platform_name"]

    def get_switch_firmware_version(self):
        firmware_url = '/rest/v1/firmware'
        firmware_versions = get(self.module, firmware_url)
        self.switch_current_firmware = firmware_versions["current_version"]

    def get_firmware_upgrade_status(self):
        fimrware_status_url = '/rest/v1/firmware/status'
        firmware_update_status = get(self.module, fimrware_status_url)
        return firmware_update_status

    def get_switch_config(self, config_name='running-config',
                          store_config=True):
>>>>>>> b72fff9... Adds 10.4 support to modules
=======
        self.original_config = None
        self.running_config = None
        self.switch_current_firmware = None
        self.switch_platform = None
        self.get_switch_platform()
        self.get_switch_firmware_version()
        self.get_switch_config(store_config=store_config)

        if "10.00" in self.switch_current_firmware:
            self.module.fail_json(msg="Minimum supported "
                                      "firmware version is 10.03")

        if "10.01" in self.switch_current_firmware:
            self.module.fail_json(msg="Minimum supported "
                                      "firmware version is 10.03")

        if "10.02" in self.switch_current_firmware:
            self.module.fail_json(msg="Minimum supported "
                                      "firmware version is 10.03")

    def get_switch_platform(self):
        '''
        Returns the switch platform
        '''
        platform_url = '/rest/v1/system?attributes=platform_name'
        platform = get(self.module, platform_url)
        self.switch_platform = platform["platform_name"]

    def get_switch_firmware_version(self):
        '''
        Returns the switch firmware
        '''
        firmware_url = '/rest/v1/firmware'
        firmware_versions = get(self.module, firmware_url)
        self.switch_current_firmware = firmware_versions["current_version"]

    def get_firmware_upgrade_status(self):
        '''
        Returns the firmware upgrade status
        '''
        fimrware_status_url = '/rest/v1/firmware/status'
        firmware_update_status = get(self.module, fimrware_status_url)
        return firmware_update_status

    def get_switch_config(self, config_name='running-config',
                          store_config=True):
<<<<<<< HEAD
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4

=======
        '''
        Returns the switch config
        '''
>>>>>>> da0d435... New modules and bug fixes
        config_url = '/rest/v1/fullconfigs/{cfg}'.format(cfg=config_name)

        running_config = get(self.module, config_url)

        if store_config:
            self.running_config = copy.deepcopy(running_config)
            self.original_config = copy.deepcopy(running_config)

<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4
        return running_config

    def copy_switch_config_to_remote_location(self, config_name, config_type,
                                              destination, vrf):
        '''
        TFTP switch config to TFTP server
        '''
        config_url = ('/rest/v1/fullconfigs/'
                      '{cfg}?to={dest}&type={type}'
                      '&vrf={vrf}'.format(cfg=config_name,
                                          dest=destination,
                                          type=config_type,
                                          vrf=vrf))

        get(self.module, config_url)
        return

    def tftp_switch_config_from_remote_location(self, config_file_location,
                                                config_name, vrf):
        '''
        TFTP switch config from TFTP server
        '''
        config_url = ('/rest/v1/fullconfigs/'
                      '{cfg}?from={dest}&vrf={vrf}'
                      ''.format(cfg=config_name,
                                dest=config_file_location,
                                vrf=vrf))

        put(self.module, config_url)
        return

    def upload_switch_config(self, config, config_name='running-config'):
        '''
        Upload switch config
        '''
        config_url = '/rest/v1/fullconfigs/{cfg}'.format(cfg=config_name)
        config_json = json.dumps(config)
        put(self.module, config_url, config_json)
        return
<<<<<<< HEAD
>>>>>>> b72fff9... Adds 10.4 support to modules
=======
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4

    def update_switch_config(self):
        '''
        Update switch config
        '''
        self.result = dict(changed=self.changed, warnings=self.warnings)

        if self.original_config != self.running_config:
            self.upload_switch_config(self.running_config)
            self.result["changed"] = True
        else:
            self.result["changed"] = False
            self.module.log("============================ No Change ======="
                            "===========================")
            self.module.exit_json(**self.result)

        with open('/tmp/debugging_running_config.json', 'w') as to_file:
            json.dump(self.running_config, to_file, indent=4)
            to_file.write("\n")

        self.module.exit_json(**self.result)
