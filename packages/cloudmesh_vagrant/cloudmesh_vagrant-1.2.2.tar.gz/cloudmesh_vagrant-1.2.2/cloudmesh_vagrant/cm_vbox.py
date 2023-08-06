from __future__ import print_function

from docopt import docopt
import cloudmesh_vagrant as vagrant
from cloudmesh_client.common.dotdict import dotdict
from pprint import pprint
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.common.Shell import Shell
import sys
import os
from cloudmesh_vagrant.version import __version__
# pprint (vagrant.vm.list())
# vagrant.vm.execute("w2", "uname")
# pprint (vagrant.image.list())

def defaults():
    """
    default values
    :return: a number of default values for memory, image, and script
    :rtype: dotdict
    """
    d = dotdict()
    d.memory = 1024
    # d.image = "ubuntu/xenial64"
    d.image = "ubuntu/trusty64"
    d.port = 8080
    d.script = None
    return d



def _convert(lst, id="name"):
    d = {}
    for entry in lst:
        d[entry[id]] = entry
    return d


def _LIST_PRINT(l, output, order=None):
    if output in ["yaml", "dict", "json"]:
        l = _convert(l)

    result = Printer.write(l,
                           order=order,
                           output=output)

    if output in ["table", "yaml", "json", "csv"]:
        print(result)
    else:
        pprint(result)


def do_vbox(argv):
    """
    ::

      Usage:
        vbox version [--format=FORMAT]
        vbox image list [--format=FORMAT]
        vbox image find NAME
        vbox image add NAME
        vbox vm list [--format=FORMAT] [-v]
        vbox vm delete NAME
        vbox vm config NAME
        vbox vm ip NAME [--all]
        vbox create NAME ([--memory=MEMORY]
                          [--image=IMAGE]
                          [--script=SCRIPT] | list)
        vbox vm boot NAME ([--memory=MEMORY]
                           [--image=IMAGE]
                           [--port=PORT]
                           [--script=SCRIPT] | list)
        vbox vm ssh NAME [-e COMMAND]
    """
    arg = dotdict(docopt(do_vbox.__doc__, argv))
    arg.format = arg["--format"] or "table"
    arg.verbose = arg["-v"]
    arg.all = arg["--all"]

    if arg.version:
        versions = {
            "vagrant": {
               "attribute": "Vagrant Version",
                "version": vagrant.version(),
            },
            "cloudmesh-vbox": {
                "attribute":"cloudmesh vbox Version",
                "version": __version__
            }
        }
        _LIST_PRINT(versions, arg.format)

    elif arg.image and arg.list:
        l = vagrant.image.list(verbose=arg.verbose)
        _LIST_PRINT(l, arg.format, order=["name", "provider", "date"])

    elif arg.image and arg.add:
        l = vagrant.image.add(arg.NAME)
        print(l)

    elif arg.image and arg.find:
        l = vagrant.image.find(arg.NAME)
        print(l)

    elif arg.vm and arg.list:
        l = vagrant.vm.list()
        _LIST_PRINT(l,
                   arg.format,
                   order=["name", "state", "id", "provider", "directory"])

    elif arg.create and arg.list:

        result = Shell.cat("{NAME}/Vagrantfile".format(**arg))
        print (result)

    elif arg.create:

        d = defaults()

        arg.memory = arg["--memory"] or d.memory
        arg.image = arg["--image"] or d.image
        arg.script = arg["--script"] or d.script

        vagrant.vm.create(
            name=arg.NAME,
            memory=arg.memory,
            image=arg.image,
            script=arg.script)

    elif arg.config:

        # arg.NAME
        d = vagrant.vm.info(name=arg.NAME)

        result = Printer.attribute(d, output=arg.format)

        print (result)

    elif arg.ip:

        data = []
        result = vagrant.vm.execute(arg.NAME, "ifconfig")
        if result is not None:
            lines = result.splitlines()[:-1]
            for line in lines:
                if "inet addr" in line:
                    line = line.replace("inet addr", "ip")
                    line = ' '.join(line.split())
                    _adresses = line.split(" ")
                    address = {}
                    for element in _adresses:
                        attribute, value = element.split(":")
                        address[attribute] = value
                    data.append(address)
        if arg.all:
            d = {}
            i = 0
            for e in data:
                d[str(i)] = e
                i = i + 1
            result = Printer.attribute(d, output=arg.format)
            print(result)
        else:
            for element in data:
                ip = element['ip']
                if  ip == "127.0.0.1" or ip.startswith("10."):
                    pass
                else:
                    print (element['ip'])


    elif arg.boot:

        d = defaults()

        arg.memory = arg["--memory"] or d.memory
        arg.image = arg["--image"] or d.image
        arg.script = arg["--script"] or d.script
        arg.port = arg["--port"] or d.port

        vagrant.vm.boot(
            name=arg.NAME,
            memory=arg.memory,
            image=arg.image,
            script=arg.script,
            port=arg.port)

    elif arg.delete:

        result = vagrant.vm.delete(name=arg.NAME)
        print(result)

    elif arg.ssh:

        if arg.COMMAND is None:
            os.system("cd {NAME}; vagrant ssh {NAME}".format(**arg))
        else:
            result = vagrant.vm.execute(arg.NAME, arg.COMMAND)
            if result is not None:
                lines = result.splitlines()[:-1]
                for line in lines:
                    print (line)

    else:

        print ("use help")

def main():
    args = sys.argv[1:]
    do_vbox(args)


if __name__ == '__main__':
    main()
