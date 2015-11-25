from novaclient import client as novaclient
import subprocess

def is_token_valid(token, config):
    """
    To verify keystone token before letting user to do what he wants
    """

    
    return True

def get_host_for_vm(vm_uuid, creds):
    """
    find out where the vm is running physically
    """
    c = get_nova_creds(creds)
    nova = novaclient.Client("1.1",  **c)
    server = nova.servers.get(vm_uuid)

    hostname = getattr(server, 'OS-EXT-SRV-ATTR:host')
    instance_name = getattr(server, 'OS-EXT-SRV-ATTR:instance_name')
    return hostname, instance_name


def get_vcpu_quota(vm_host, vm_kvm_name, creds):
    host_command = "sudo virsh schedinfo {0}".format(str(vm_kvm_name))
    cmd = ["ssh",
           "{0}@{1}".format(creds.bare_metal_user, vm_host),
           "{0}".format(host_command)]
    out = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out, err= out.communicate()
    return _extract_vcpu_info(out)

def _extract_vcpu_info(out):
    found_vp = False
    found_vq = False
    for line in out.split("\n"):
        if "vcpu_period" in line:
             vcpu_period = float(line.split(":")[1])
             found_vp = True
        if "vcpu_quota" in line:
             vcpu_quota =  float(line.split(":")[1])
             found_vq = True
    if not (found_vp and found_vq):
        raise Exception("Internal Error: Cannot find vpcu quota")
    return vcpu_quota, vcpu_period


def set_vcpu_quota(vm_host, vm_kvm_name, vcpu_value, creds):
    host_command = "sudo virsh schedinfo {0} --set vcpu_quota={1}".format(vm_kvm_name, vcpu_value)
    cmd = ["ssh",
           "{0}@{1}".format(creds.bare_metal_user, vm_host),
           "{0}".format(host_command)]

    print " ".join(cmd)

    cmd_call = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = cmd_call.stdout.read()
    return output


def get_nova_creds(creds):
    d = {}
    d['auth_url']=creds.auth_url
    d['username']=creds.username
    d['api_key']=creds.password
    d['project_id']=creds.tenant
    return d