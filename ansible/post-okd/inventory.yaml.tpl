---

all:
  children:

    cli-node:
      hosts:
        ${cli_node}:
          ansible_user: centos
          admin_password: ${admin_password}
