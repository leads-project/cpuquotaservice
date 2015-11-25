
_VIRT_ENV_NAME="cpuquotaservice"
TARGET_DEPLOYMENT=
TARGET_DIR="cpuquotaservice"

dev_prepare_virtualenv:
	. $$(which virtualenvwrapper.sh) ; \
	mkvirtualenv $(_VIRT_ENV_NAME) ; \
	pip install -U -r requirements.txt ; \
	echo "Virtualenv ready, to use it, run:  workon $(_VIRT_ENV_NAME)"
	
deploy_installer:
	ssh $(TARGET_DEPLOYMENT) "mkdir -p ~/$(TARGET_DIR)"; \
	scp install.sh requirements.txt runCPUService.py $(TARGET_DEPLOYMENT):~/$(TARGET_DIR); \
	scp -r cpuinfo $(TARGET_DEPLOYMENT):~/$(TARGET_DIR);

run_install:
	ssh $(TARGET_DEPLOYMENT) "cd ~/cpuquotaservice/ && bash +x install.sh"

generate_ssh_key:
	ssh $(TARGET_DEPLOYMENT) "ssh-keygen -t rsa -b 4096 -q -N '' -f ~/.ssh/id_rsa"

distribute_ssh_key:
	# KEY=$(< ~/.ssh/id_rsa.pub)  egrep -o 'r00011[0-9]m[0-9]+[ ]' /etc/hosts | tr -d ' '  |  uniq | xargs -I {} ssh {}  "echo '${KEY}' >> .ssh/authorized_keys && echo 'Key copied'"
	echo "TO BE IMPLEMENTED!"


