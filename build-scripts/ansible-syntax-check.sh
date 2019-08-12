#!/bin/bash

# Here we run --syntax-check for all the supported playbooks...

ansible-playbook --syntax-check ansible/bastion/site.yaml -i bastion,cli-node

ansible-playbook --syntax-check ansible/post-destroy/gce/site.yaml -i localhost,
ansible-playbook --syntax-check ansible/post-destroy/aws/site.yaml -i localhost,

ansible-playbook --syntax-check ansible/post-okd/site.yaml -i cli-node,
ansible-playbook --syntax-check ansible/post-okd/users.yaml -i cli-node,
ansible-playbook --syntax-check ansible/post-okd/playbooks/acme-controller/deploy.yaml -i cli-node,
ansible-playbook --syntax-check ansible/post-okd/playbooks/kube-ops-view/deploy.yaml -i cli-node,

ansible-playbook --syntax-check ansible/pre-okd/site.yaml -i masters,
