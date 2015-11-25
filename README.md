# REST interface for cpu quota service

Openstack does not support runtime vertical scaling(changing virtual CPU power/speed). It only supports to change flavor size. However, this changes will only be affected after booting VMs. Meanwhile, KVM allows us to perform vertical scaling. To trigger the actions on KVM level, cloud users need the admin credentials that is impossible. Therefore I created this REST interface to run it on cloud provider side to perform vertical scaling services. Thanks Cloud&amp;Heat (https://www.cloudandheat.com/de/index.html) for helping us deploy this interface in their system.

### How to deploy ###
* $./install.sh
* Modify IP address and port in the  runCPUQuotaService.py
* $sudo python runCPUService.py

### How to use ###
* Access http://IP:8080/getcpuquota/vmID1 to get cpu quota information of virtual machine vmID1
* Access http://IP:8080/setcpuquota/vmID1/$quota_value to set cpu quota to vmID1

### Contact? ###
* SE Group, TU Dresden, Germany
* Do Le Quoc: lequocdo@gmail.com

