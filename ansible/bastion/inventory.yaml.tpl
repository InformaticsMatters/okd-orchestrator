---

all:
  children:

    bastion:
      hosts:
        ${bastion}:
          ansible_connection: ssh
          ansible_user: centos

    cli-node:
      hosts:
        ${cli_node}:
          ansible_connection: ssh
          ansible_user: centos
