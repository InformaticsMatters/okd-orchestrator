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

The orchestrator is designed to allow the deployment of **Clusters** and their
**Bastion** control servers with minimal effort from the comfort of a
development laptop.

Creation and destruction is handled by logic managed from within
two Python command-line modules; ``create.py`` and ``destroy.py``. The modules
call upon a number of underlying processes (essentially carried out by
**Terraform** and **Ansible**) in order to create and destroy your hardware.

With a few utilities installed on your development host you should be able to
create and manage clusters across a wide-variety of cloud providers using
just these two modules.

The Components
==============

The orchestrator consists of: -

*   **Deployment configuration** files
*   **Provider Variables**
*   **Yacker** templates
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

Provider Variables
------------------

In ``provider-env``.

Yacker templates
----------------

In ``yacker/``.

**Yacker** is used to create base images for the compute instances.
It is a YAML wrapper around **Packer**. It is driven by YAML files that
describe installation instructions that are executed on a base Operating System
like CentOS in order to form an OS and utilities suitable for OKD.

The YAML *template* files are organised in directories relating to OKD
version and cloud provider. For example there is an AWS *bastion image*
template for OKD 3.9 in ``yacker/3.9/aws``.

**Yacker** is employed once per OKD release and cloud provider combination.
The images produced are suitable for any cluster for the given OKD release on
that cloud provider.

Terraform Templates
-------------------

In ``terraform/``.

**Terraform** is used to create and destroy the OKD cluster hardware.
It is a form of IaC tool that automates the construction of cloud infrastructure
including additional volumes, networks, subnets and security groups.

It's language is declarative, meaning that you simply need to describe what is
connected to what and it manages the creation of objects and their connections.

Once you've described your cluster you have access to Terraform commands like
**apply** to build the cluster and **destroy** to delete it.

Jinja2 Rendering Process
------------------------

Ansible Playbooks
-----------------

In ``ansible/``.

The Create Utility
------------------

The Destroy Utility
-------------------
