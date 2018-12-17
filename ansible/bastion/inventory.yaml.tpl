---

all:
  children:

    bastion:
      hosts:
        ${bastion}:
          ansible_connection: ssh
          ansible_user: centos

    master1:
      hosts:
        ${master1}:
          ansible_connection: ssh
          ansible_user: centos
