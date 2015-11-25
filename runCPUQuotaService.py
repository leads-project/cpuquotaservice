#
# (C) Do Le Quoc, 2014
#

from cpuinfo import app
import os

hostName = os.environ['CPUQUOTA_LISTEN_IP'] 
portNumber = int(os.environ['CPUQUOTA_PORT'])

app.run(host=hostName, port=portNumber, debug = True)

