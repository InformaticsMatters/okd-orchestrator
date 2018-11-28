############
Architecture
############

.. highlight:: none

The orchestrator is a utility that is designed to simplify the creation
(and removal) of an OpenShift cluster. It introduces a number of
*concepts* and accomplishes it through the use of a number of *components*.

The utility is in an early stage of development and is evolving rapidly.
The goal is to provide a simple and rapid and automated means of instantiating
an OpenShift Origin-based compute cluster with minimal effort.

The Concept
===========

The Components
===============

The orchestrator consists of: -

*   **Deployment configuration** files
*   **Packer** templates
*   **Terraform** templates
*   A **Jinja2** rendering process
*   Ansible **playbooks**
*   A **create** utility
*   A **destroy** utility

deployments
-----------

In ``deployments/``.

A **Deployment** *describes* your cluster; providing a high-level description
of the cluster hardware and software requirements that includes the number and
types of the compute instances used for your OpenShift nodes.

The **deployment** is defined in a `YAML`_ file.

You can have more than one deployment file, each describing a separate
OpenShift cluster.

Deployment files are located in the ``deployments`` directory.

.. _YAML: http://yaml.org

Packer templates
----------------

In ``packer/``.

Terraform Templates
-------------------

In ``terraform/``.

Jinja2 Rendering Process
------------------------

Ansible Playbooks
-----------------

In ``ansible/`` and ``openshift-ansible//``.

The Create Utility
------------------

The Destroy Utility
-------------------
