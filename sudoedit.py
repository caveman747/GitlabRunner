import os, subprocess
import sys
from sys import argv

def etc_update(host_name, *args):
    path = "/etc/hosts"
    host_name = host_name[0]
    fw = open(path,'w')
    fw.write("ALL=(ALL) NOPASSWD: /usr/bin/apt, /usr/bin/snap")

etc_update(sys.argv[1:])