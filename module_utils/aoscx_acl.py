#!/usr/bin/python
# -*- coding: utf-8 -*-
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

# (C) Copyright 2019-2020 Hewlett Packard Enterprise Development LP.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

>>>>>>> b72fff9... Adds 10.4 support to modules

from ansible.module_utils.aoscx import ArubaAnsibleModule
from random import randint


class ACL:

    def create_acl(self, aruba_ansible_module, acl_name, acl_type):

        if not aruba_ansible_module.running_config.has_key("ACL"):
            aruba_ansible_module.running_config["ACL"] = {}

        acl_index = acl_name + "/" + acl_type

        if not aruba_ansible_module.running_config["ACL"].has_key(acl_index):
            aruba_ansible_module.running_config["ACL"][acl_index] = {
                "name": acl_name,
                "list_type": acl_type,
                "cfg_version": randint(-900719925474099, 900719925474099)
            }

        return aruba_ansible_module

    def check_acl_exist(self, aruba_ansible_module, acl_name, acl_type):

        if not aruba_ansible_module.running_config.has_key("ACL"):
            return False

        acl_index = acl_name + "/" + acl_type

        if not aruba_ansible_module.running_config["ACL"].has_key(acl_index):
            return False

        return True

    def delete_acl(self, aruba_ansible_module, acl_name, acl_type):

        if not self.check_acl_exist(aruba_ansible_module, acl_name, acl_type):
            aruba_ansible_module.warnings.append("ACL {} of type {} not does not exist ".format(acl_name,acl_type))
            return aruba_ansible_module

        acl_index = acl_name + "/" + acl_type

        aruba_ansible_module.running_config["ACL"].pop(acl_index)

        return aruba_ansible_module

    def update_acl_fields(self, aruba_ansible_module, acl_name, acl_type, acl_fields):

        if not self.check_acl_exist(aruba_ansible_module, acl_name, acl_type):
            aruba_ansible_module.warnings.append("ACL {} of type {} not does not exist ".format(acl_name,acl_type))
            return aruba_ansible_module

        acl_index = acl_name + "/" + acl_type

        for key in acl_fields.keys():

            if aruba_ansible_module.running_config["ACL"][acl_index].has_key(key):
                if (aruba_ansible_module.running_config["ACL"][acl_index][key] != acl_fields[key]):
                    aruba_ansible_module.running_config["ACL"][acl_index][key] = acl_fields[key]
                    aruba_ansible_module.running_config["ACL"][acl_index]["cfg_version"] = randint(-900719925474099, 900719925474099)
            else:
                aruba_ansible_module.running_config["ACL"][acl_index][key] = acl_fields[key]
                aruba_ansible_module.running_config["ACL"][acl_index]["cfg_version"] = randint(-900719925474099, 900719925474099)

        return aruba_ansible_module

    def update_acl_entry(self, aruba_ansible_module, acl_name, acl_type, acl_entry_sequence_number, acl_entry_details, update_type="insert"):
        if not self.check_acl_exist(aruba_ansible_module, acl_name, acl_type):
            aruba_ansible_module.warnings.append("ACL {} of type {} not does not exist ".format(acl_name,acl_type))
            return aruba_ansible_module

        acl_index = acl_name + "/" + acl_type

        if (update_type == 'insert') or (update_type == 'update') :

            if not aruba_ansible_module.running_config["ACL"][acl_index].has_key("cfg_aces"):
                aruba_ansible_module.running_config["ACL"][acl_index]["cfg_aces"] = {}

            if aruba_ansible_module.running_config["ACL"][acl_index]["cfg_aces"].has_key(acl_entry_sequence_number):
                if aruba_ansible_module.running_config["ACL"][acl_index]["cfg_aces"][acl_entry_sequence_number] != acl_entry_details:
                    aruba_ansible_module.running_config["ACL"][acl_index]["cfg_aces"][acl_entry_sequence_number] = acl_entry_details
                    aruba_ansible_module.running_config["ACL"][acl_index]["cfg_version"] = randint(-900719925474099, 900719925474099)
            else:
                aruba_ansible_module.running_config["ACL"][acl_index]["cfg_aces"][acl_entry_sequence_number] = acl_entry_details
                aruba_ansible_module.running_config["ACL"][acl_index]["cfg_version"] = randint(-900719925474099, 900719925474099)

            return aruba_ansible_module

        if update_type == 'delete':

            if not aruba_ansible_module.running_config["ACL"][acl_index].has_key("cfg_aces"):
                aruba_ansible_module.running_config["ACL"][acl_index]["cfg_aces"] = {}

                aruba_ansible_module.running_config["ACL"][acl_index]["cfg_aces"].pop(acl_entry_sequence_number)
                return aruba_ansible_module










