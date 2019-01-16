###############################
Deploying Application Templates
###############################

A template describes a set of objects that can be parameterised and processed
to produce a list of objects for creation by OpenShift Container Platform.
A template can be processed to create anything you have permission to create
within a project.

You can create template objects form the CLI or upload templates to a project
or the global template library. Here we discuss the latter.

This is not a description of templates, it is a description of how the
orchestrator allows you to to defined a set of templates for deployment
to your cluster.

`Templates for OKD 3.11`_ are well described on the RedHat site.

Orchestrator template file location
===================================

The orchestrator looks for template files in the ``templates``
sub-directory of your deployment so you need to place all the
templates you wish to deploy in that directory.

Orchestrator template configuration
===================================

To successfully deploy templates you will need to *enable* the
template service broker by adding it to the ``okd.enable`` list::

    okd:
      [...]
      enable:
      - tsb

You then need to declare the template destination project using the
``template`` configuration block::

    okd:
      [...]
      template:
        namespace: openshift

The namespace must be a namespace (project) that exists in your OKD
deployment. ``openshift`` is a global/default project often used to house
application templates.

Templates are deployed by the Ansible playbook
``ansible/post-okd/templates.yaml``. It inspects the selected directory,
expecting every file in it to be an OpenShift template for your cluster.

.. _Templates for OKD 3.11: https://docs.openshift.com/container-platform/3.11/dev_guide/templates.html
