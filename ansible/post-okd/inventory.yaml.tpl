---

all:
  children:

    cli-node:
      hosts:
        ${cli-node}:
          ansible_user: ${ansible-user}
          admin_password: ${admin-password}
