###############
Getting Started
###############

.. highlight:: none

The orchestrator is designed to simplify the construction of an OpenShift
cluster and various cloud providers. At the moment we have working solutions
for Amazon *EC2*, *OpenStack* and *Scaleway* and a working example for
*EC2* that we use as a tutorial.

Before you can use the orchestrator you will need to install a number
of tools on your host machine you'll be using to create your clusters,
e.g. your laptop or desktop. Ideally you will be starting with a linux host as
distributions for the various tools is generally better for macOS and Linux
(and we really only support Linux-like environments).

You will need to install: -

-   **Git** (and clone this repository)
-   **Python** ``v2.7.15``
-   **Packer** (``v1.3.2``) and **Terraform** (``v0.11.10``)
-   A utility that allows you to generate SSH key pairs

Git (and this repository)
-------------------------

In order to use the orchestrator, an open source software project, you will
need the `Git`_ version control system installed. Using Git you can start
with copy of the orchestrator by *cloning* the main repository or, a more
common approach, allowing you to make changes to the deployments to suite
your environment, would be to *fork* it and then clone your forked copy.

-  After installing Git, visit the `orchestrator repository`_, fork it
   and clone it to your development host.

.. _Git: https://git-scm.com
.. _Orchestrator Repository: https://github.com/InformaticsMatters/okd-orchestrator

Python (and Ansible)
--------------------

The orchestrator currently supports Python 2 so you will need to install that
and PIP if it is not part of it.

-   Install `Python 2.7.15`_

    You might want to follow this by creating a Python or Conda
    *virtual environment* so that you can isolate the orchestrator's Python
    dependencies from any others you may be using.

Ansible, a tool used by the orchestrator, is a Python-based utility and it
and other modules used are installed using a conventional ``requirements.txt``
file and ``pip``.

``pip`` may be installed as part of your chosen Python distribution.
Try running ``pip``. If it cannot be found you may need to install it::

    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    sudo python get-pip.py
    rm get-pip.py

You can now install Ansible and the dependent modules by running ``pip``
from the root directory of your clone of this project::

    pip install --upgrade pip
    pip install -r requirements.txt

.. _Python 2.7.15: https://www.python.org/downloads/release/python-2715/

Packer and Terraform
--------------------

You should visit the HashiCorp site where downloads of `Packer`_ and
`Terraform`_ should be available.

    Although the precise version of Packer is not terribly important
    (``v1.3.2`` or later should be fine) the version of Terraform you install
    *is*. The terraform templates we use make explicit references to the version
    of the application and it is vital you install the right version, which
    is ``v0.11.10``.

.. _Terraform: https://www.terraform.io
.. _Packer: https://www.packer.io

Generating SSH Keys
-------------------

Ensure that you're able to create SSH keys, using a utility like
``ssh-keygen``.

Checking the Installation
^^^^^^^^^^^^^^^^^^^^^^^^^

If you've installed everything then you should have cloned this repository
and be able to run the following commands::

    ansible --version
    packer --version
    terraform --version
