#
# (C) Do Le Quoc TUD
#

from cpuquota import app

hostName='127.0.0.1'
portNumber = 8080

app.run(host=hostName, port=portNumber, debug = True)

