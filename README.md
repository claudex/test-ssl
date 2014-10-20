#Description

Test an host or all the hosts in the specified network if SSLv3 in enabled on
the common port for SSL. Currently it tests SMTP, POP3, IMAP and HTTPS.

#Usage

    ./test.py [-d|--debug] [(-t|--timeout) <timeout>] (-n|--network) <net>
    ./test.py [-d|--debug] [(-t|--timeout) <timeout>] <host>
    ./test.py (-h|--help)

    <host> the host to analyse
    -d, --debug: print debug informations
    -n, --network: analyse all the hosts in the given network
    -t, --timeout: set the timemout in seconds, default 30 seconds
    -h, --help: print this help information

#Dependancies

	Require Python2 and python-netaddr module
