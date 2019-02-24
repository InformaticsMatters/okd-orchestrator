#####################################
Anatomy of a Deployment Configuration
#####################################

**Deployment Configurations**, located in ``configuration.yaml`` files
in sub-directories of the project's ``deployments`` directory, provide
a high-level abstraction that, in one file, allows you to describe your
cluster hardware and the properties of your desired OKD software
configuration at a relatively high level. The OKD orchestrator uses this
as a template in order to provision the system for you.

    The trade-off by using *yet another file format* is one of simple verses
    advanced. You will no-doubt be able to fine-tune and configure your
    cluster and OKD software in a richer and more powerful environment if you
    manage the system and its underlying files yourself. But the
    **OKD Orchestrator** philosophy is about *simplicity* rather than
    *advanced* features. It's about rapidly creating (and destroying) simple
    Virtual Environments (VEs) without having to understand your cloud
    provider's provisioning complexities relating to networks, volumes,
    and machines or the myriad of complex parameters that can be setupo to
    form a rich and complex OKD platform.

-   The deployment file is a **text file**, a `YAML`_ file that provides you
    with an environment where you can document your configuration as well as
    define it
-   The file consists of three *sections*: -

    -   A section used to define the VE hardware (the ``cluster`` section)
    -   A section used to define the OKD software (the ``okd`` section)
    -   An optional section used to define pre-allocated hardware when working
        with custom/bare-metal installations (the ``my_machines`` section) [#f1]_

Rather than go into detail here, and risk breaking the *do not repeat yourself*
rule, the documentation relating to the format and content of the deployment
configuration can be found embedded in the built-in ``compact-aws-frankfurt-3-11``
configuration.

For a detailed discussion of the configuration file format and the settable
parameters please refer to
``deployments/compact-aws-frankfurt-3-11/configuration.yaml``.

.. _yaml: https://yaml.org

.. rubric:: Footnotes

.. [#f1] If you are using the OKD Orchestrator to deploy the cloud hardware the
         **my_machines** section is not used
