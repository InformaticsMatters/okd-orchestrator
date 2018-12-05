########################
Compiling Machine Images
########################

.. highlight:: none

The OKD cluster (and its Bastion) are formed from hardware
provided by your cloud provider. As the base image for each of our
physical machines needs some pre-installed software it's often
easier to compile a dedicated base image that all our compute instances
will use.

Once an image has been compiled for a cloud provider region it can be used
for any number of clusters for that provider's region.

To compile imageswe use `yacker`_ a YAML wrapper for `packer`_,
a HashiCorp tool dedicated to the the automated construction of machine images.

.. epigraph::

   **Yacker** configurations are defined *template* files written in YAML.
   Without going into great detail the files consist of ``variables``,
   ``builders`` and ``provisioners`` sections.

   The ``provisioners`` section contains the list of instructions that are
   executed on top of a base images. The cloud-specific details are held
   in the ``builders`` section and the ``variables`` provide some dynamic control.

The image templates are located in the ``yacker`` project directory
where you'll find templates organised according to OKD release and
cloud provider. For example, the OpenShift 3.9 AWS EC2 templates for the
Bastion and OpenShift cluster nodes can be found in the ``yacker/3.9/aws``
directory.

.. _yacker: https://pypi.org/project/matildapeak-yacker/
.. _packer: https://www.packer.io

The following guides provide instructions for the cloud providers
we support: -

-   :doc:`compiling-machine-images-for-aws`
