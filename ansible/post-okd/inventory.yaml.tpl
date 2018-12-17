---

all:
  children:

    cli-node:
      hosts:
        ${cli-node-ip}:
          ansible_user: ${ansible-user}
          admin_password: ${admin-password}
