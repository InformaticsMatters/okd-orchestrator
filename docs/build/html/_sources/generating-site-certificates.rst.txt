###########################
Generating SSL Certificates
###########################

You can use the orchestrator's ability to use `Let's Encrypt`_ and the
`certbot`_ utility to automatically create SSL certificates for your site.

It would be normal when deploying a certificate to have satisfied the following
before orchestrating your cluster:

*   Pre-allocate public IPs for the Master and Infrastructure (Router) nodes
*   A domain (like *mydomain.com*) routed to the Master's public IP for
    access to the OpenShift/OKD's web console

The above information need to be placed in your deployment configuration prior
to orchestration.

#.  Place the identity of the Master Node's fixed IP into the value for
    ``cluster.master.fixed_ip_id``. This is normally the provider's identity
    of the allocated IP *not* the IP itself. In the case of AWS this
    would be the the Elastic IP identity (the value starting ``eipalloc-``)
#.  Similarly place the identity of the Infrastructure/Router Node's fixed
    IP into the value for ``cluster.infra.fixed_ip_id``
#.  Place the domain name routed to the master (for the OpenShift console)
    into the value for ``cluster.public_hostname``
#.  Place the domain name that is routed to the Infrastructure/Router
    into the value for ``cluster.router_basename``
#.  To instruct the orchestrator to automatically generate
    certificates set the ``cluster.certificates.generate_api_cert`` value
    to ``Yes``

#.  Finally, you need to set the ``TF_VAR_master_certbot_email`` variable in
    your ``setenv.sh`` file to the email address registered with Let's Encrypt.

You should now be ready to follow the :doc:`creating-your-cluster` guide.

.. _let's encrypt: https://letsencrypt.org
.. _certbot: https://certbot.eff.org

Using automatically allocated public IPs
========================================

If you are not generating a certificate then you can optionally let the
orchestrator allocate public IPs for your Master and Infrastructure instances.

In this case you simply need to remove any value for the Master and
Infrastructure ``fixed_ip_id`` properties of your deployment configuration.

When you do not provide values for the Master and Infrastructure
``fixed_ip_id`` values the orchestrator will, where the provider
allows it, create fixed IPs on your behalf. In the case of AWS this will
be two **Elastic IP** allocations in the region the orchestrator is
deploying to.

Automatically generated public IPs will be removed when the cluster is
destroyed.
