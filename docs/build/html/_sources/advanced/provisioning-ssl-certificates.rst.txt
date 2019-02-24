#############################
Provisioning SSL Certificates
#############################

Automated (certbot) certificates
================================

If you have a `certbot`_ (Let's Encrypt) account the OKD Orchestrator can
automatically generate SSL certificates for your site. You just need
to do the following before creating your cluster: -

#.  Provide your account's registered email in the
    ``TF_VAR_master_certbot_email`` variable in your ``setenv.sh`` file
#.  Set the configuration file property ``okd.certificates.generate_api_cert``
    to ``yes``.

This is convenient and quick. Certbot certificates are nice, and self-signed
but they often expire after a few months, needing to be renewed.

.. _certbot: https://certbot.eff.org

User (pre-defined) certificates
===============================

As an alternative you can provide your own certificates, and you may well
have some that are pre-built for the domain you'll be deploying OKD to.
If you have your own certificates you can automatically deploy these
with a few simple steps.

In order to deploy your own certificates You should should have: -

-   Three **certificate files**. ``cert.crt``, ``ca-bandle.crt`` and
    ``private.key``
-   The **domain name** for the master API/console

As best practice, and to protect them, your certificate files must be encrypted
using `ansible vault`_ [#1]_.

To deploy your certificates, do the following before deploying your cluster: -

#.  Place your encrypted certificate files into a directory called
    ``certificates`` in your deployment configuration directory. For example
    if your deployment configuration is ``aws_demo`` the files would
    go into ``deployments/aws_demo/certificates``
#.  Set the configuration file property ``okd.certificates.generate_api_cert``
    to the SSL domain name for the master
#.  Create a ``vault-pass.txt`` file containing the vault password you
    used to encrypt your certificates and place this in your deployment
    directory (e.g. in ``deployments/aws_demo``) [#2]_

.. _ansible vault: https://docs.ansible.com/ansible/latest/user_guide/vault.html

.. [#1] Ansible vault is available in the OKD Orchestrator's container image.
        The files will be automatically decrypted as they are sent to the
        Bastion/Master for the OKD installation process.
.. [#2] You can commit your certificates to revision control as they are
        encrypted but the ``vault-pass.txt`` file is the one thing you
        do not commit. This remains a local file.
