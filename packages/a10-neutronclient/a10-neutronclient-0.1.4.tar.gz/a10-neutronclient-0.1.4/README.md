# A10 Networks Neutron Client Extensions
===========================================

A10 Networks Neutron Client Extensions

Supported releases:

* OpenStack: Icehouse, Juno, Kilo, Liberty, Mitaka
* LBaaS versions: v1, v2
* ACOS versions: ACOS 2/AxAPI 2.1 (ACOS 2.7.2+), ACOS 4/AxAPI 3.0 (ACOS 4.0.1-GA +)

Working but not available for support:

* OpenStack: git/master


## A10 github repos
- [a10-neutronclient](https://github.com/a10networks/a10-neutronclient) - Neutron CLI Client extensions.  Adds "a10-*" commands to the neutron client.
- [a10-neutron-lbaas](https://github.com/a10networks/a10-neutron-lbaas) - Main A10 LBaaS driver repo. Middleware sitting between the
openstack driver and our API client, mapping openstack constructs to A10's AxAPI.
- [acos-client](https://github.com/a10networks/acos-client) - AxAPI client used by A10's OpenStack driver


## Installation steps:

### Step 1:

Make sure you have python-neutronclient installed.  These extensions will need to be installed on any computer where the neutron CLI is used.

### Step 2:

The latest supported version of a10-neutronclient is available via standard pypi repositories and the current development version is available on github.

##### Installation from pypi
```sh
sudo pip install a10-neutronclient
```

##### Installation from cloned git repository.

Download the driver from: <https://github.com/a10networks/a10-neutronclient>


```sh
sudo pip install git+https://github.com/a10networks/a10-neutronclient
```

```sh
git clone https://github.com/a10networks/a10-neutronclient
cd a10-neutronclient
sudo pip install -e .
```

## Configuration

As these extensions provide client functionality, the only configuration necessary is configuring Neutron to load the API extensions.  This process is covered in the respositories for a10-neutron-lbaas and a10-openstack.

To verify successful installation, type the following command.
```sh
neutron --help
```
The Neutron CLI should present you with a list of commands.  If the client extensions are properly installed, you will see methods prefixed with "a10-".

## A10 Community

Feel free to fork, submit pull requests, or join us on freenode IRC, channel #a10-openstack. Serious support escalations and formal feature requests must
still go through standard A10 processes.

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
