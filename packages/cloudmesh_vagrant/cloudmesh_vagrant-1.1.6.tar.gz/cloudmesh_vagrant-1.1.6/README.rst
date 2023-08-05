Cloudmesh Virtualbox/Vagrant Interface
================================================================

Virtualbox provides a vonvenient way to manage virtual machines on a
local computer. Graphical user interfaces, a commandline client, but
also vagrant exist to access them. However we noticed that we often
only need a very small subset to start a vm and to tear it
down. Remembering the interfaces is difficult. Previously we developed
a cloudmesh_client that has an easy to remember interface. We leverage
from this experience and introduce a very easy to remember commandline
client. At the same time we also allow a simpl python API to manage
virtual machines on virtualbox. We use vagrant internally. However
vagrants focus on directories and Vagrantfiles in a bit inconvenient
also fo us, so we provided wrappers and utelize the design of vagrant
to our advantage while only exposing the needed functionality.

Manual Page
------------

::

    Usage:
      cm-vbox version
      cm-vbox image list [--format=FORMAT]
      cm-vbox vm list [--format=FORMAT]
      cm-vbox vm delete NAME
      cm-vbox create NAME ([--memory=MEMORY]
                           [--image=IMAGE]
                           [--script=SCRIPT] | list)
      cm-vbox vm boot NAME ([--memory=MEMORY]
                            [--image=IMAGE]
                            [--script=SCRIPT] | list)


Source Code
-----------

* https://github.com/cloudmesh/vagrant

Install
--------

mkdir cloudmesh
cd cloudmesh
git clone https://github.com/cloudmesh/vagrant
cd vagrant
python setup.py install


Examples
-------

Listing vms
^^^^^^^^^^^

python v.py vbox vm list

+------+---------+---------+------------+----------------------+
| name | state   | id      | provider   | directory            |
+------+---------+---------+------------+----------------------+
| w12  | running | 47347b4 | virtualbox | ~/w12                |
| w1   | running | db913dd | virtualbox | ~/w1                 |
+------+---------+---------+------------+----------------------+

Listing images
^^^^^^^^^^^^^^

python v.py vbox image list
+-----------------+------------+--------------+
| name            | provider   | date         |
+-----------------+------------+--------------+
| ubuntu/trusty64 | virtualbox | 20160406.0.0 |
+-----------------+------------+--------------+

Booting vms
^^^^^^^^^^^

python v.py vbox vm boot w12

which takes an ubuntu image as default

Destroy a vm
^^^^^^^^^^^^^

python v.py vbox vm delete w12

which deletes the specified vm

Create a Vagrantfile
^^^^^^^^^^^^^^^^^^^^

python v.py vbox create w12

creates a Vagrantfile in ./w12/Vagrantfile



