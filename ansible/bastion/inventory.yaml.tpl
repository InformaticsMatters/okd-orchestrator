---

all:
  children:

    bastion:
      hosts:
        ${bastion}:
          ansible_connection: ssh
          ansible_user: ${ssh_user}

    cli-node:
      hosts:
        ${cli_node}:
          ansible_connection: ssh
          ansible_user: ${ssh_user}
