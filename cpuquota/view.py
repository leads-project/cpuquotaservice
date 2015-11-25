#
# (C) Do Le Quoc, 2014
#

#!/usr/bin/python

import subprocess

from flask import Flask, render_template, g, redirect, jsonify, url_for, abort, request, make_response
from ujson import loads

from cpuinfo import app
import json
import os
from cloudandheat import get_host_for_vm, get_vcpu_quota, set_vcpu_quota


class CloudAndHeatCreds:
    username = os.environ['OS_USERNAME']
    password = os.environ['OS_PASSWORD']
    auth_url = os.environ['OS_AUTH_URL']
    tenant = os.environ['OS_TENANT_NAME']
    bare_metal_user = os.environ['BM_USER']


creds=CloudAndHeatCreds()


def getCPUQuota(vm_host, vm_kvm_name):
    vcpu_quota, vcpu_period = get_vcpu_quota(vm_host, vm_kvm_name, creds)
    return vcpu_quota, vcpu_period


def setCPUQuota(vm_host, vm_kvm_name, vcpu_value):
    output = set_vcpu_quota(vm_host, vm_kvm_name, vcpu_value, creds)
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
    vm_host, vm_kvm_name = get_host_for_vm(vmID, creds)

    if len(vmID) == 0:
        abort(404)
    else:
        result ={}  
        vcpu_quota, vcpu_period = getCPUQuota(vm_host, vm_kvm_name)
        result["vcpu_quota"] = vcpu_quota
        result["vcpu_period"] = vcpu_period

    return json.dumps(result) 


@app.route("/setcpuquota/<vm_id>/<quota_value>", methods = ['GET'])
def setcpuquota(vm_id, quota_value):
    vmID = str(vm_id)
    vm_host, vm_kvm_name = get_host_for_vm(vmID, creds)

    if len(vm_id) == 0 or _is_number(quota_value) is not True:
        abort(404)
    else:
        result = setCPUQuota(vm_host, vm_kvm_name, int(quota_value))
    return json.dumps(result)


def _is_number(value):
    return value.isdigit() or _is_negative_number(value)


def _is_negative_number(value):
    return value.startswith('-') and value[1:].isdigit()
