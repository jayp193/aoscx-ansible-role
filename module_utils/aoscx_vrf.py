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


class VRF:

    def create_vrf(self, aruba_ansible_module, vrf_name):

        if "vrfs" not in aruba_ansible_module.running_config['System'].keys():
            aruba_ansible_module.running_config['System']['vrfs'] = {}

        if vrf_name not in aruba_ansible_module.running_config['System']['vrfs'].keys():  # NOQA
            aruba_ansible_module.running_config['System']['vrfs'][vrf_name] = {
                "name": vrf_name,
                "type": "user",
            }
            if vrf_name == 'default':
                aruba_ansible_module.running_config['System']['vrfs'][vrf_name].pop("type")  # NOQA
        else:
            aruba_ansible_module.warnings.append("VRF {vrf} already exist"
                                                 "".format(vrf=vrf_name))

        return aruba_ansible_module

    def delete_vrf(self, aruba_ansible_module, vrf_name):
        error = ("VRF {name} is attached to {int}. Interface must be deleted "
                 "and "
                 "created under new VRF before VRF can "
                 "be deleted.")
        if not self.check_vrf_exists(aruba_ansible_module, vrf_name):
            aruba_ansible_module.warnings.append("VRF {vrf} is not configured"
                                                 "".format(vrf=vrf_name))
            return aruba_ansible_module

        # Throw error if VRF is attached to an interface
        if 'Port' in aruba_ansible_module.running_config.keys():
            port_dict = aruba_ansible_module.running_config['Port']
            for encoded_port_name in port_dict.keys():
                temp_port_dict = port_dict[encoded_port_name]
                if 'vrf' in temp_port_dict.keys():
                    if temp_port_dict['vrf'] == vrf_name:
                        aruba_ansible_module.module.fail_json(msg=error.format(vrf=vrf_name,  # NOQA
                                                              int=encoded_port_name.replace('%2F', '/')))  # NOQA

        aruba_ansible_module.running_config['System']['vrfs'].pop(vrf_name)
        return aruba_ansible_module

    def check_vrf_exists(self, aruba_ansible_module, vrf_name):

        if "vrfs" not in aruba_ansible_module.running_config['System'].keys():
            return False

        if vrf_name not in aruba_ansible_module.running_config['System']['vrfs'].keys():  # NOQA
            return False

        return True

    def update_vrf_dns_domain_name(self, aruba_ansible_module, vrf_name,
                                   dns_domain_name, update_type="insert"):

        if not self.check_vrf_exists(aruba_ansible_module, vrf_name) and (update_type == 'insert'):  # NOQA
            aruba_ansible_module.module.fail_json(
                "VRF {vrf} is not configured".format(vrf=vrf_name))
            return aruba_ansible_module

        elif not self.check_vrf_exists(aruba_ansible_module, vrf_name) and (update_type == 'delete'):  # NOQA
            aruba_ansible_module.warnings.append("VRF {vrf} is not configured"
                                                 "".format(vrf=vrf_name))
            return aruba_ansible_module

        if (update_type == 'insert') or (update_type == 'update'):
            aruba_ansible_module.running_config['System']['vrfs'][vrf_name]['dns_domain_name'] = dns_domain_name  # NOQA
        elif update_type == 'delete':
            aruba_ansible_module.running_config['System']['vrfs'][vrf_name].pop('dns_domain_name')  # NOQA

        return aruba_ansible_module

    def update_vrf_dns_domain_list(self, aruba_ansible_module, vrf_name,
                                   dns_domain_list, update_type="insert"):

<<<<<<< HEAD
<<<<<<< HEAD
        if not self.check_vrf_exists(aruba_ansible_module, vrf_name) and (update_type == 'insert'):
            aruba_ansible_module.module.fail_json(
                "VRF {} is not configured".format(vrf_name))
=======
=======
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4
        if not self.check_vrf_exists(aruba_ansible_module, vrf_name) and (update_type == 'insert'):  # NOQA
            aruba_ansible_module.module.fail_json(msg="VRF {vrf} is not "
                                                      "configured"
                                                      "".format(vrf=vrf_name))
<<<<<<< HEAD
>>>>>>> b72fff9... Adds 10.4 support to modules
=======
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4
            return aruba_ansible_module

        elif not self.check_vrf_exists(aruba_ansible_module, vrf_name) and (update_type == 'delete'):  # NOQA
            aruba_ansible_module.warnings.append("VRF {vrf} is not "
                                                 "configured"
                                                 "".format(vrf=vrf_name))
            return aruba_ansible_module

        if (update_type == 'insert') or (update_type == 'update'):
            aruba_ansible_module.running_config['System']['vrfs'][vrf_name]['dns_domain_list'] = dns_domain_list  # NOQA
        elif update_type == 'delete':
            aruba_ansible_module.running_config['System']['vrfs'][vrf_name].pop('dns_domain_list')  # NOQA

        return aruba_ansible_module

    def update_vrf_dns_name_servers(self, aruba_ansible_module, vrf_name,
                                    dns_name_servers, update_type="insert"):

<<<<<<< HEAD
<<<<<<< HEAD
        if not self.check_vrf_exists(aruba_ansible_module, vrf_name) and (update_type == 'insert'):
            aruba_ansible_module.module.fail_json(
                "VRF {} is not configured".format(vrf_name))
=======
=======
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4
        if not self.check_vrf_exists(aruba_ansible_module, vrf_name) and (update_type == 'insert'):  # NOQA
            aruba_ansible_module.module.fail_json(msg="VRF {vrf} is not "
                                                      "configured"
                                                      "".format(vrf=vrf_name))
<<<<<<< HEAD
>>>>>>> b72fff9... Adds 10.4 support to modules
=======
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4
            return aruba_ansible_module
        elif not self.check_vrf_exists(aruba_ansible_module, vrf_name) and (update_type == 'delete'):  # NOQA
            aruba_ansible_module.warnings.append("VRF {vrf} is not "
                                                 "configured"
                                                 "".format(vrf=vrf_name))
            return aruba_ansible_module

        if (update_type == 'insert') or (update_type == 'update'):
            aruba_ansible_module.running_config['System']['vrfs'][vrf_name]['dns_name_servers'] = dns_name_servers  # NOQA
        elif update_type == 'delete':
            aruba_ansible_module.running_config['System']['vrfs'][vrf_name].pop('dns_name_servers')  # NOQA

        return aruba_ansible_module

    def update_vrf_dns_host_v4_address_mapping(self, aruba_ansible_module,
                                               vrf_name,
                                               dns_host_v4_address_mapping,
                                               update_type="insert"):

<<<<<<< HEAD
<<<<<<< HEAD
    def update_vrf_dns_host_v4_address_mapping(self, aruba_ansible_module, vrf_name, dns_host_v4_address_mapping, update_type="insert"):

        if not self.check_vrf_exists(aruba_ansible_module, vrf_name) and (update_type == 'insert'):
            aruba_ansible_module.module.fail_json(
                "VRF {} is not configured".format(vrf_name))
            return aruba_ansible_module

        elif not self.check_vrf_exists(aruba_ansible_module, vrf_name) and (update_type == 'delete'):
            aruba_ansible_module.warnings.append(
                "VRF {} is not configured".format(vrf_name))
=======
        if not self.check_vrf_exists(aruba_ansible_module, vrf_name) and (update_type == 'insert'):  # NOQA
            aruba_ansible_module.module.fail_json(msg="VRF {vrf} is not "
                                                      "configured"
                                                      "".format(vrf=vrf_name))
            return aruba_ansible_module

=======
        if not self.check_vrf_exists(aruba_ansible_module, vrf_name) and (update_type == 'insert'):  # NOQA
            aruba_ansible_module.module.fail_json(msg="VRF {vrf} is not "
                                                      "configured"
                                                      "".format(vrf=vrf_name))
            return aruba_ansible_module

>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4
        elif not self.check_vrf_exists(aruba_ansible_module, vrf_name) and (update_type == 'delete'):  # NOQA
            aruba_ansible_module.warnings.append(msg="VRF {vrf} is not "
                                                     "configured"
                                                     "".format(vrf=vrf_name))
<<<<<<< HEAD
>>>>>>> b72fff9... Adds 10.4 support to modules
=======
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4
            return aruba_ansible_module

        if (update_type == 'insert') or (update_type == 'update'):
            aruba_ansible_module.running_config['System']['vrfs'][vrf_name]['dns_host_v4_address_mapping'] = dns_host_v4_address_mapping  # NOQA
        elif update_type == 'delete':
            aruba_ansible_module.running_config['System']['vrfs'][vrf_name].pop('dns_host_v4_address_mapping')  # NOQA

        return aruba_ansible_module

    def update_vrf_dns_host_v6_address_mapping(self, aruba_ansible_module,
                                               vrf_name,
                                               dns_host_v6_address_mapping,
                                               update_type="insert"):

<<<<<<< HEAD
<<<<<<< HEAD
    def update_vrf_dns_host_v6_address_mapping(self, aruba_ansible_module, vrf_name, dns_host_v6_address_mapping, update_type="insert"):

        if not self.check_vrf_exists(aruba_ansible_module, vrf_name) and (update_type == 'insert'):
            aruba_ansible_module.module.fail_json(
                "VRF {} is not configured".format(vrf_name))
=======
=======
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4
        if not self.check_vrf_exists(aruba_ansible_module, vrf_name) and (update_type == 'insert'):  # NOQA
            aruba_ansible_module.module.fail_json(msg="VRF {vrf} is not "
                                                      "configured"
                                                      "".format(vrf=vrf_name))
<<<<<<< HEAD
>>>>>>> b72fff9... Adds 10.4 support to modules
=======
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4
            return aruba_ansible_module

        elif not self.check_vrf_exists(aruba_ansible_module, vrf_name) and (update_type == 'delete'):  # NOQA
            aruba_ansible_module.warnings.append("VRF {vrf} is not "
                                                 "configured"
                                                 "".format(vrf=vrf_name))
            return aruba_ansible_module

        if (update_type == 'insert') or (update_type == 'update'):
            aruba_ansible_module.running_config['System']['vrfs'][vrf_name]['dns_host_v4_address_mapping'] = dns_host_v6_address_mapping  # NOQA
        elif update_type == 'delete':
            aruba_ansible_module.running_config['System']['vrfs'][vrf_name].pop('dns_host_v6_address_mapping')  # NOQA

        return aruba_ansible_module

    def enable_disable_vrf_ssh_server(self, aruba_ansible_module, vrf_name,
                                      enable_ssh_server=False):

        if not self.check_vrf_exists(aruba_ansible_module, vrf_name):
<<<<<<< HEAD
<<<<<<< HEAD
            aruba_ansible_module.module.fail_json(
                "VRF {} is not configured".format(vrf_name))
=======
            aruba_ansible_module.module.fail_json(msg="VRF {vrf} is not "
                                                      "configured"
                                                      "".format(vrf=vrf_name))
>>>>>>> b72fff9... Adds 10.4 support to modules
=======
            aruba_ansible_module.module.fail_json(msg="VRF {vrf} is not "
                                                      "configured"
                                                      "".format(vrf=vrf_name))
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4
            return aruba_ansible_module

        aruba_ansible_module.running_config['System']['vrfs'][vrf_name]['ssh_enable'] = enable_ssh_server  # NOQA

        return aruba_ansible_module

    def check_vrf_snmp_enable(self, aruba_ansible_module, vrf_name):

        if not self.check_vrf_exists(aruba_ansible_module, vrf_name):
<<<<<<< HEAD
<<<<<<< HEAD
            aruba_ansible_module.module.fail_json(
                "VRF {} is not configured".format(vrf_name))
=======
            aruba_ansible_module.module.fail_json(msg="VRF {vrf} is not "
                                                      "configured"
                                                      "".format(vrf=vrf_name))
>>>>>>> b72fff9... Adds 10.4 support to modules
=======
            aruba_ansible_module.module.fail_json(msg="VRF {vrf} is not "
                                                      "configured"
                                                      "".format(vrf=vrf_name))
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4
            return aruba_ansible_module

        if aruba_ansible_module.running_config['System']['vrfs'][vrf_name]['enable_snmp']:  # NOQA
            return True

        return False

    def enable_disable_vrf_snmp(self, aruba_ansible_module, vrf_name,
                                enable_snmp=False):

        if not self.check_vrf_exists(aruba_ansible_module, vrf_name):
<<<<<<< HEAD
<<<<<<< HEAD
            aruba_ansible_module.module.fail_json(
                "VRF {} is not configured".format(vrf_name))
=======
            aruba_ansible_module.module.fail_json(msg="VRF {vrf} is not "
                                                      "configured"
                                                      "".format(vrf=vrf_name))
>>>>>>> b72fff9... Adds 10.4 support to modules
=======
            aruba_ansible_module.module.fail_json(msg="VRF {vrf} is not "
                                                      "configured"
                                                      "".format(vrf=vrf_name))
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4
            return aruba_ansible_module

        for vrf in aruba_ansible_module.running_config['System']['vrfs'].keys():  # NOQA
            if self.check_vrf_snmp_enable(aruba_ansible_module, vrf):
<<<<<<< HEAD
<<<<<<< HEAD
                aruba_ansible_module.module.fail_json("SNMP is enabled in VRF {}. Only one VRF can have SNMP enabled.")
=======
=======
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4
                aruba_ansible_module.module.fail_json(msg="SNMP is enabled in"
                                                          " VRF {vrf}. Only "
                                                          "one VRF can have "
                                                          "SNMP enabled."
                                                          "".format(vrf=vrf))
<<<<<<< HEAD
>>>>>>> b72fff9... Adds 10.4 support to modules
=======
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4

        aruba_ansible_module.running_config['System']['vrfs'][vrf_name]['enable_snmp'] = enable_snmp  # NOQA

        return aruba_ansible_module

    def enable_disable_vrf_https_server(self, aruba_ansible_module, vrf_name,
                                        enable_https_server=False):

        if not self.check_vrf_exists(aruba_ansible_module, vrf_name):
<<<<<<< HEAD
<<<<<<< HEAD
            aruba_ansible_module.module.fail_json(
                "VRF {} is not configured".format(vrf_name))
=======
            aruba_ansible_module.module.fail_json(msg="VRF {vrf} is not "
                                                      "configured"
                                                      "".format(vrf=vrf_name))
>>>>>>> b72fff9... Adds 10.4 support to modules
=======
            aruba_ansible_module.module.fail_json(msg="VRF {vrf} is not "
                                                      "configured"
                                                      "".format(vrf=vrf_name))
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4
            return aruba_ansible_module

        aruba_ansible_module.running_config['System']['vrfs'][vrf_name]['https_server'] = {"enable": enable_https_server}  # NOQA

        return aruba_ansible_module

    def update_vrf_address_family(self, aruba_ansible_module, vrf_name,
                                  family_type, route_target_type,
                                  route_target, update_type='insert'):

        if not self.check_vrf_exists(aruba_ansible_module, vrf_name):
<<<<<<< HEAD
<<<<<<< HEAD
            aruba_ansible_module.module.fail_json(
                "VRF {} is not configured".format(vrf_name))
=======
            aruba_ansible_module.module.fail_json(msg="VRF {vrf} is not "
                                                      "configured"
                                                      "".format(vrf=vrf_name))
>>>>>>> b72fff9... Adds 10.4 support to modules
=======
            aruba_ansible_module.module.fail_json(msg="VRF {vrf} is not "
                                                      "configured"
                                                      "".format(vrf=vrf_name))
>>>>>>> a6a7d002c67b68d39183ff87414400ace9e49fc4
            return aruba_ansible_module

        # if (update_type == "insert") or (update_type == "update"):
        #     aruba_ansible_module.running_config['System']['vrfs'][vrf_name][family_type]

        # if update_type == 'delete':
