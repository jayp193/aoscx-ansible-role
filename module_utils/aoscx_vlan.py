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
=======
=======
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4

# (C) Copyright 2019-2020 Hewlett Packard Enterprise Development LP.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

<<<<<<< HEAD
>>>>>>> b72fff9... Adds 10.4 support to modules
=======
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4

from ansible.module_utils.aoscx import ArubaAnsibleModule
from ansible.module_utils.aoscx_port import Port
from ansible.module_utils.aoscx_interface import Interface


class VLAN:

    def create_vlan(self, aruba_ansible_module, vlan_id):

        if "VLAN" not in aruba_ansible_module.running_config.keys():
            aruba_ansible_module.running_config["VLAN"] = {}

        vlan_id_str = str(vlan_id)
        if vlan_id_str not in aruba_ansible_module.running_config.keys():
            aruba_ansible_module.running_config["VLAN"][vlan_id_str] = {
                "id": vlan_id
            }

        return aruba_ansible_module

    def check_vlan_exist(self, aruba_ansible_module, vlan_id):

<<<<<<< HEAD
<<<<<<< HEAD
        if not aruba_ansible_module.running_config.has_key("VLAN"):
=======
=======
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4
        if aruba_ansible_module.switch_platform.startswith("6"):
            if vlan_id == 1:
                return True

        if "VLAN" not in aruba_ansible_module.running_config.keys():
<<<<<<< HEAD
>>>>>>> b72fff9... Adds 10.4 support to modules
=======
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4
            return False

        vlan_id_str = str(vlan_id)

        if vlan_id_str == '1':
            return True

        if vlan_id_str not in aruba_ansible_module.running_config["VLAN"].keys():  # NOQA
            return False

        return True

    def delete_vlan(self, aruba_ansible_module, vlan_id):

        port = Port()
        interface = Interface()

        interface_vlan_id = "vlan{id}".format(id=vlan_id)

        if not self.check_vlan_exist(aruba_ansible_module, vlan_id):
            aruba_ansible_module.warnings.append("VLAN ID {id} is not "
                                                 "configured"
                                                 "".format(id=vlan_id))
            return aruba_ansible_module

        if interface.check_interface_exists(aruba_ansible_module,
                                            interface_vlan_id):
            aruba_ansible_module.module.fail_json(msg="VLAN ID {id} is "
                                                      "configured as interface"
                                                      " VLAN"
                                                      "".format(id=vlan_id))
            return aruba_ansible_module

        port_list = port.get_configured_port_list(aruba_ansible_module)

        vlan_port_fields = ["vlan_tag", "vlan_mode", "vlans_per_protocol",
                            "vlan_trunks"]

        vlan_id_str = str(vlan_id)

        for port_name in port_list:

            vlan_field_values = port.get_port_field_values(aruba_ansible_module, port_name, vlan_port_fields)  # NOQA

            if vlan_field_values["vlan_tag"] == vlan_id_str:
                aruba_ansible_module = port.update_port_fields(aruba_ansible_module, port_name, {"vlan_tag": "1"})  # NOQA

            if vlan_id_str in vlan_field_values["vlan_trunks"] and type(vlan_field_values["vlan_trunks"]) is list:  # NOQA
                vlan_field_values["vlan_trunks"].remove(vlan_id_str)
                aruba_ansible_module = port.update_port_fields(aruba_ansible_module, port_name, {"vlan_trunks": vlan_field_values["vlan_trunks"]})  # NOQA

        aruba_ansible_module.running_config["VLAN"].pop(vlan_id_str)

        return aruba_ansible_module

    def update_vlan_fields(self, aruba_ansible_module, vlan_id,
                           vlan_fields_details, update_type='update'):

        if not self.check_vlan_exist(aruba_ansible_module, vlan_id):
            aruba_ansible_module.warnings.append("VLAN ID {id} is not "
                                                 "configured"
                                                 "".format(id=vlan_id))
            return aruba_ansible_module

        vlan_id_str = str(vlan_id)

        for key in vlan_fields_details.keys():
            if (update_type == 'update') or (update_type == 'insert'):
                aruba_ansible_module.running_config["VLAN"][vlan_id_str][key] = vlan_fields_details[key]  # NOQA
            elif update_type == 'delete':
                aruba_ansible_module.running_config["VLAN"][vlan_id_str].pop(key)  # NOQA
        return aruba_ansible_module

    def get_vlan_fields_values(self, aruba_ansible_module, vlan_id,
                               vlan_fields):

        if not self.check_vlan_exist(aruba_ansible_module, vlan_id):
            aruba_ansible_module.warnings.append(
                "VLAN ID {id} is not configured".format(id=vlan_id))
            return aruba_ansible_module

        vlan_id_str = str(vlan_id)

        result = {}
        for field in vlan_fields:

            if field in aruba_ansible_module.running_config["VLAN"][vlan_id_str].keys():  # NOQA
                result[field] = aruba_ansible_module.running_config["VLAN"][vlan_id_str][field]  # NOQA

        return result
