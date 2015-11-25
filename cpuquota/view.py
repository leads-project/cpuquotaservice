#
# (C) Do Le Quoc TUD
#

#!/usr/bin/python

import subprocess

from flask import Flask, render_template, g, redirect, jsonify, url_for, abort, request, make_response
from ujson import loads

from cpuinfo import app
import json


def getCPUQuota(vmID):
    arg = "schedinfo " + str(vmID) 
    out = subprocess.Popen(['virsh', arg], stdout=subprocess.PIPE)
    out, err= out.communicate()
    vcpu_period=0
    vcpu_quota=0
    for line in out.split("\n"):
        if "vcpu_period" in line:
             vcpu_period = float(line.split(":")[1])
        if "vcpu_quota" in line:
             vcpu_quota =  float(line.split(":")[1])

    return vcpu_quota, vcpu_period


def setCPUQuota(vmID, vcpu_quota):
    arg = "schedinfo " + str(vmID) + " --set vcpu_quota=" + str(vcpu_quota)
    cmdcall = subprocess.Popen(['virsh', arg], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = cmdcall.stdout.read()
    if "error" not in str(output):
        return "ok"
    else:
        return output



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found'} ), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify( { 'error': 'bad request' } ), 400)



@app.route('/')
@app.route('/index')
def index():
    return "CPU Quota Service"

@app.route("/getcpuquota/<vm_id>", methods = ['GET'])
def getcpuquota(vm_id):
    vmID = str(vm_id)

    if len(vmID) == 0:
        abort(404)
    else:
        result ={}  
        vcpu_quota, vcpu_period = getCPUQuota(vmID)
        result["vcpu_quota"] = vcpu_quota
        result["vcpu_period"] = vcpu_period

    return json.dumps(result) 



@app.route("/setcpuquota/<vm_id>/<int:quota_value>", methods = ['GET'])
def setcpuquota(vm_id, quota_value):
    if len(vm_id) == 0 or str(quota_value).isdigit() is not True:
        abort(404)
    else:
        result = setCPUQuota(str(vm_id), int(quota_value))

    return json.dumps(result)
