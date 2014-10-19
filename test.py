#!/usr/bin/python

#Copyright (c) 2014 Xavier Claude
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of
#this software and associated documentation files (the "Software"), to deal in
#the Software without restriction, including without limitation the rights to
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
#the Software, and to permit persons to whom the Software is furnished to do so,
#subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
#FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
#IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
#CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import getopt
import os
import string
import sys
from subprocess import Popen, PIPE
from netaddr import IPNetwork

debug = False;

DNULL = open(os.devnull, 'w')


#TODO add ftp
port_list = [25,110,143,443,587,993,995]
starttls_port = [25,587,143,110]
smtp_port = [25,587]
imap_port = [143,993]
pop_port = [110,995]

proto_list = ["ssl3"]

def generate_cmd(proto, host, port):
    cmd = []
    cmd.append("openssl")
    cmd.append("s_client")
    cmd.append("-" + proto)
    cmd.append("-connect")
    cmd.append(host + ":" + str(port))

    if port in starttls_port:
        cmd.append("-starttls")
        if port in smtp_port:
            cmd.append("smtp")
        elif port in imap_port:
            cmd.append("imap")
        elif port in pop_port:
            cmd.append("pop")
        else:
            print "Unsupported port: " + str(port)
            sys.exit(2)

    return cmd

def print_usage(not_enough=False, too_much=False):
    if not_enough:
        print "You should specify an host or a network"
    if too_much:
        print "You can't specifiy an host and a network"

    print """Usage:
    {0} [-d|--debug] (-n|--network) <net>
    {0} [-d|--debug] <host>
    {0} (-h|--help)

    <host> the host to analyse
    -d, --debug: print debug informations
    -n, --network: analyse all the hosts in the given network
    -h, --help: print this help information
    """.format(sys.argv[0])

def analyse_host(host):
    print "Analysing " + host + ": " 

    for proto in proto_list:
        for port in port_list:
            cmd = generate_cmd(proto,host,port)

            openssl = Popen(cmd, stdin=PIPE, stdout=DNULL, stderr=PIPE)
            err = openssl.communicate()[1]

            if openssl.returncode != 0:
                if string.find(err, "alert handshake failure") != -1:
                    if debug:
                        print str(port) + ": ok, no " + proto
                else:
                    if debug:
                        print str(port) + ": connection error"
            else:
                print str(port) + ": " + proto + " enable"

def analyse_net(net):
    ip_list = IPNetwork(net)

    for ip in ip_list:
        analyse_host(str(ip))

try:
    options, remainder = getopt.getopt(sys.argv[1:], "dhn:", ["debug", "help",
"net="])
except getopt.GetoptError as err:
    print str(err)
    print_usage()
    sys.exit(2)

for opt, arg in options:
    if opt in ("-d", "--debug"):
        debug=True;
    elif opt in ("-h", "--help"):
        print_usage()
    elif opt in ("-n", "--network"):
        net = arg

if net and remainder:
    print_usage(too_much=True)
    sys.exit(2)
elif remainder:
    analyse_host(remainder)
elif net:
    analyse_net(net)
else:
    print_usage(not_enough=True)
    sys.exit(2)



