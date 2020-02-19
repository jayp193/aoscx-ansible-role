
aoscx
=========

This Ansible Network role provides a set of platform dependent configuration
 management modules specifically designed for the AOS-CX network device.

Requirements
------------

* Python 2.7 or 3.5+
* Ansible 2.8.1 or later  
<<<<<<< HEAD
* Minimum supported AOS-CX firmware version 10.03
=======
* Minimum supported AOS-CX firmware version 10.03.
>>>>>>> b72fff9... Adds 10.4 support to modules
* Enable REST on your AOS-CX device with the following commands:
    ```
    switch(config)# https-server rest access-mode read-write
    switch(config)# https-server vrf mgmt
    ```

Installation
------------

Through Github, use the following command. Use option `-f` to overwrite current role version:

```
ansible-galaxy install git+https://github.com/aruba/aoscx-ansible-role.git
```

Through Galaxy:

```
ansible-galaxy install arubanetworks.aoscx_role
```

Inventory Variables
--------------

The variables that should be defined in your inventory for your AOS-CX host are:

* `ansible_host`: IP address of switch in `A.B.C.D` format. For IPv6 hosts use a string and enclose in square brackets E.G. `'[2001::1]'`.
* `ansible_user`: Username for switch in `plaintext` format  
* `ansible_password`: Password for switch in `plaintext` format  
* `ansible_connection`: Must always be set to `httpapi`  
* `ansible_network_os`: Must always be set to `aoscx`  
* `ansible_httpapi_use_ssl`: Must always be `True` as AOS-CX uses port 443 for REST  
* `ansible_httpapi_validate_certs`: Set `True` or `False` depending on if Ansible should attempt to validate certificates  
* `ansible_acx_no_proxy`: Set `True` or `False` depending if Ansible should bypass environment proxies to connect to AOS-CX  

### Sample Inventory:

#### INI

```INI
aoscx_1 ansible_host=10.0.0.1 ansible_user=admin ansible_password=password ansible_connection=httpapi ansible_network_os=aoscx ansible_httpapi_validate_certs=False ansible_httpapi_use_ssl=True ansible_acx_no_proxy=True
```

#### YAML

```yaml
all:
  hosts:
    aoscx_1:
      ansible_host: 10.0.0.1
      ansible_user: admin
      ansible_password: password
      ansible_connection: httpapi  # Do not change
      ansible_network_os: aoscx
      ansible_httpapi_validate_certs: False
      ansible_httpapi_use_ssl: True
      ansible_acx_no_proxy: True
```

Example Playbook
----------------

If role installed through [Github](https://github.com/aruba/aoscx-ansible-role)
set role to `aoscx-ansible-role`:

```yaml
    ---
    -  hosts: all
       roles:
        - role: aoscx-ansible-role
       tasks:
         - name: Create L3 Interface 1/1/3
           aoscx_l3_interface:
            interface: 1/1/3
            description: Uplink_Interface
            ipv4: ['10.20.1.3/24']
            ipv6: ['2001:db8::1234/64']
```

If role installed through [Galaxy](https://galaxy.ansible.com/arubanetworks/aoscx_role)
set role to `arubanetworks.aoscx_role`:

```yaml
    ---
    -  hosts: all
       roles:
        - role: arubanetworks.aoscx_role
       tasks:
         - name: Create L3 Interface 1/1/3
           aoscx_l3_interface:
            interface: 1/1/3
            description: Uplink_Interface
            ipv4: ['10.20.1.3/24']
            ipv6: ['2001:db8::1234/64']
```

Contribution
-------
At Aruba Networks we're dedicated to ensuring the quality of our products, if you find any
issues at all please open an issue on our [Github](https://github.com/aruba/aoscx-ansible-role) and we'll be sure to respond promptly!


License
-------

Apache 2.0

Author Information
------------------
Madhusudan Pranav Venugopal (madhusudan-pranav-venugopal)  
Yang Liu (yliu-aruba)  
Tiffany Chiapuzio-Wong (tchiapuziowong)  
