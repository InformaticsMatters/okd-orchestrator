###########
Orientation
###########

The OKD Orchestrator can do two things: -

-   **Instantiate** a cluster of compute instances (currently AWS)
-   **Install** RedHat's OKD platform on the cluster

It achieves this through the use of Packer, Terraform and Ansible,
managed by Python modules and a high-level configuration file
providing you with simple **create** and **destroy** mechanisms.

You execute the orchestrator using a clone (or fork) of the OKD
orchestrator repository.

The orchestrator environment (Packer, terraform, Ansible etc.) is conveniently
provided by a container image or, if you are comfortable working with your own
copies of the tools and Python virtual environments, you can use the **create**
and **destroy** modules from the command-line. [#1]_

.. _packer: https://www.packer.io
.. _terraform: https://www.terraform.io
.. _ansible: https://www.ansible.com
.. _pyhton: https://www.python.org

.. [#1] The documentation assumes that you will be using the containerised OKD

Instantiating a cluster
=======================

Illustrated in the simplified process diagram below, from your development
machine, using Docker or a Python environment and tools, the step typically
involves: -

-   Compiling machine images with `Yacker`_ to form a suitable base
    operating system on which to deploy OKD
-   Defining your deployment in a **configuration file**
-   Creating the cluster of compute instances, networking and firewalls
    for the cluster using the **create** module

..  image:: ../images/okd-orchestrator.001.png

You don't need to understand Yacker (Packer) or Terraform to use the OKD
orchestrator.

.. _yacker: https://yacker.readthedocs.io/en/latest/

Installing the OKD platform
===========================

With the cluster created (or the presence of your own compute instances) this
step typically involves: -

-   Installing the OKD platform from the Bastion (or Master) using the
    **create** module (which manages OKD installation via Ansible)

..  image:: ../images/okd-orchestrator.002.png
