######################
Running Without Docker
######################

Although the orchestrator is designed to run from inside a convenient Docker
container you don't have to. The orchestration code is written in Python
and relies on a Unix-like operating system [#f1]_ so you can run the it
directly from the root of a clone (or fork) of this repository. You simply
need to ensure that your environment is similar to the container's. That is: -

#.  **Python 3** (ideally 3.6 or 3.7). Optionally installed via a
    `virtual environment`_ or with `Conda`_.
#.  The **requirements** from ``requirements.txt`` from the root of this
    project
#.  **Packer** (we currently use v1.3.3), and available on your ``PATH``
#.  **Terraform** available on your ``PATH``. Check any ``provider.tf``
    file in the ``terraform`` director as it specifies the
    ``required_version``. The same version is used by all providers.
#.  You will need some *standard* tools such as ``ssh`` and ``ssh-keygen``

Once the tools are installed you should be able to run ``create.py``
and ``destroy.py`` from the root of the project.

.. _conda: https://conda.io/docs/
.. _virtual environment: https://docs.python.org/3/tutorial/venv.html

.. rubric:: Footnotes

.. [#f1] Sadly running without Docker requires a Unix-like operating system
         and so Windows is not currently supported
