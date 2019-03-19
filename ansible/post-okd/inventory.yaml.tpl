---

all:
  children:

    cli-node:
      hosts:
        ${cli_node}:
          ansible_user: ${ssh_user}
          admin_password: ${admin_password}
