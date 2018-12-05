###############
Getting Started
###############

The orchestrator is designed to simplify the construction of an OpenShift
cluster on various cloud providers. At the moment we have working solutions
for Amazon *EC2*, *OpenStack* and *Scaleway* and a working example for
*EC2* that we use as a tutorial.

The tools required by the orchestrator are packaged into a convenient
Docker image that you can run on your laptop or desktop. The essential
tools you *will* need are: -

-  **Git** (and a fork of the OKD Orchestrator repository)
-  **Docker**

Git
---

In order to use the orchestrator, an open source software project, you will
need the `Git`_ version control system installed. Using Git you should start
with a clone of a **fork** of the orchestrator project. A fork is preferred
because you may need to make changes to the configuration files or
create your own configurations.

#. Install Git
#. Visit the `orchestrator repository`_. Fork it and clone it to your
   development host.

You will be working from the clone of this project so start by navigating to
the root of your working copy.

.. _Git: https://git-scm.com
.. _Orchestrator Repository: https://github.com/InformaticsMatters/okd-orchestrator

Docker
------

We use `Docker`_ because it is a tool designed to make it easier to create,
deploy, and run applications by using containers. Containers allow a developer
to package up an application with all of the parts it needs, such as libraries
and other dependencies, and ship it all out as one package.

#. Install Docker. You can refer to Docker's installation guide,
   which includes guides for various platforms.

We have been using Docker **18.09.0** but any recent version should be
suitable.

.. _docker: https://www.docker.com
.. _installation guide: https://docs.docker.com/install/
