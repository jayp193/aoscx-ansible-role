#!/usr/bin/python
# -*- coding: utf-8 -*-

# (C) Copyright 2020 Hewlett Packard Enterprise Development LP.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.aoscx import get


class VrfsFacts(object):
    '''
    VRFs facts class
    '''
    def __init__(self, module, subspec='config', options='options'):
        '''
        init function
        '''
        self._module = module

    def populate_facts(self, connection, ansible_facts, data=None):
        '''
        Obtain and return VRFs Facts
        '''
        vrfs_url = '/rest/v10.04/system/vrfs?depth=2'
        data = get(self._module, vrfs_url)
        facts = {
            'vrfs': data
        }
        ansible_facts['ansible_network_resources'].update(facts)
        return ansible_facts
