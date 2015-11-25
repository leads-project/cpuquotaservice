from flask import Flask

app = Flask(__name__)

from cpuinfo import view

print "CPU quota info service starting up... "

