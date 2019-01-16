##############################
Deployment Configurations (v1)
##############################

.. highlight:: none

The OKD Orchestrator is trying to strike a balance between requiring you to
edit the complex Ansible inventory file expected by the OKD installation
and a simpler approach, exposing sufficient variables that allow
the ability to create rich, useful OKD clusters.

The orchestrator compiles the inventory file for you based on a set of
what it considers to be a useful and sufficiently rich set of parameters. [#f1]_

**Deployment configurations**, written in `YAML`_, are a simplified but
comprehensive text files that form a very-high-level description of an
OpenShift/OKD cluster. Creating an OpenShift cluster requires the compilation
of base operating-system images on which the OKD software runs, the creation of
physical machines on which to run the software and the installation and
configuration of the software itself and each of these steps can be a
challenging task and each often utilities a different definition language. So,
to install OpenShift you often find yourself having to understand
`Ansible`_, `JSON`_, `Jinja`_, `HCL`_, and `YAML`_ file formats and languages.

The *OKD Orchestrator* is design to simplify the creation of a cluster
by consolidating the definition of your cluster into one simple-to-read
file format and then automating the vast majority of tasks, relying on 3rd
party tools like Packer, Terraform and Ansible to build the necessary
cluster and install and configure the software. The orchestrator's *deployment
configuration* file is designed for the non-expert, less technical user
who simply wants to get a richly-defined OpenShift OKD cluster up and running.

.. _ansible: https://www.ansible.com
.. _json: https://www.json.org
.. _jinja: http://jinja.pocoo.org
.. _hcl: https://www.terraform.io/docs/configuration/syntax.html
.. _yaml: https://yaml.org

The Configuration Format and Location
=====================================

Configuration files are written in `YAML`_ and are located in the
``deployments`` directory of the OKD Orchestrator project [#f2]_
where a directory exists for each deployment.

Deployments are referred to using the base name of the configuration directory
which should therefore be compact but descriptive. The example configuration
(*compact-aws-frankfurt-3-11*) can be found in
``deployments/compact-aws-frankfurt-3-11/configuration.yaml`` [#f3]_.

The Configuration File Content
==============================

The configuration file consists of the a *preamble* that defines the
file version, name and description of the configuration followed by
sections (maps) that define the actual deployment:

#.  A ``cluster`` section that defines the machines and topology of the cluster
    on which OKD will be installed.
#.  An ``okd`` section that defines the OpenShift/OKD version to be installed
    and lists the Ansible playbooks that are to be executed to create the
    OKD cluster

Configurations are typically grouped into **Compact** or **Complex** topologies
where _Compact_ deployments generally have single Master instances and
_Complex_ deployments relay on resilient multi-master instances combined with
a production-grade load-balancer.

A Compact Topology Example
--------------------------

The ``deployments/compact-aws-frankfurt-3-11`` configuration is a
reference implementation of a **compact** style of deployment (a non-HA
deployment).

It can be easily configured with separate Bastion, Master and
Infrastructure instances or as a cost-effective *all-in-one* deployment
where the Bastion, Master and Infrastructure resources all reside on a single
machine. It also serves as a good *template* for your own compact deployment.

Refer to the ``compact-aws-frankfurt-3-11`` configuration file for a
detailed description of the properties it exposes to allow the formation of a
**compact** topology deployment.

A Complex Topology Example
--------------------------

*TBD*

.. rubric:: Footnotes

.. [#f1] Its capabilities will eventually evolve to create a large range of
         cluster topologies.
.. [#f2] You can place deployment configurations in any directory,
         placing the path to the deployment into the
         ``TF_VAR_deployments_directory`` environment variable.
.. [#f3] At the moment configuration files muse have the extension
         ``.yaml``