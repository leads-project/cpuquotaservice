# REST interface for cpu quota service

Openstack does not support runtime vertical scaling(changing virtual CPU power/speed). It only supports to change flavor size. However, this change will only be affected after booting VMs. Meanwhile, KVM allows us to perform vertical scaling. To trigger the actions on KVM level, cloud users need the admin credentials. That is impossible. Therefore, we have created this REST interface to run it on cloud provider side to perform vertical scaling services. Thanks Cloud&amp;Heat (https://www.cloudandheat.com/de/index.html) for helping us deploy this interface in their system.

### How to deploy ###

1. Move the files to the target installation

    $ make deploy_installer TARGET_DEPLOYMENT=hamm6

2. Run install

  Pre-requirement: *python-dev*

    $ ssh $TARGET_DEPLOYMENT
    $ cd ~/cpuquotaservice/
    $ install.sh

  or with Makefile:

    $ make run_install TARGET_DEPLOYMENT=hamm6

3. Generate new ssh_keys for cpuquotaservice to execute *virsh* on the nodes:

    make generate_ssh_key TARGET_DEPLOYMENT=hamm6

4. Add all the nodes to known_hosts

    $ nova service-list | cut -d'|' -f3 | grep -v '-' | grep r0 | tr -d ' ' |  xargs -P 10  -I {} ssh -o "StrictHostKeyChecking no"  {} 'ls'

5. Distribute ssh public key to all the nodes (copy exactly)

    $ KEY=$(< ~/.ssh/id_rsa.pub) egrep -o 'r000[0-9]+m[0-9]+[ ]' /etc/hosts | tr -d ' '  |  uniq | xargs -I {} ssh {}  "echo '${KEY}' >> .ssh/authorized_keys && echo 'Key copied' && echo \$(hostname)"

6. Run service (in **tmux**):

    $ cd ~/cpuquotaservice/

    $ export CPUQUOTA_LISTEN_IP=...
    $ export CPUQUOTA_PORT=8998
    $ export BW_USER=cpuquotauser

    $ source cpuquota_virtualenv/bin/activate
    $ source openrc.sh

    $ python runCPUQuotaService.py


7. Test:

    $ source openrc.sh
    $ export UUID_VM=$(nova list | grep ACTIVE | grep Running | cut -d'|' -f2 | tr -d ' ' | head -n 1)

    $ TARGET_DEPLOYMENT_IP=...

    $ curl http://${TARGET_DEPLOYMENT_IP}:${CPUQUOTA_PORT}/getcpuquota/${UUID_VM}

### How to use ###

API:

 - To get quota information of instance its uuid:

     http://${TARGET_DEPLOYMENT_IP}:${CPUQUOTA_PORT}/getcpuquota/<instance_uuid>

 - To set cpu quota to instance:

     http://${TARGET_DEPLOYMENT_IP}:${CPUQUOTA_PORT}/setcpuquota/<instance_uuid>/quota_value

   where quota_value is an integer (-1, [virsh low, virsh high]).

### Contact? ###
* Do Le Quoc (SE Group, TU Dresden, Germany), email: lequocdo@gmail.com
* Wojciech Barczynski (Cloud&Heat Technologies GmbH), email: wojciech.barczynski@cloudandheat.com 
