#
# (C) Do Le Quoc, 2014
#

from flask import Flask

app = Flask(__name__)

from cpuinfo import view

print "CPU info service starting up... "

