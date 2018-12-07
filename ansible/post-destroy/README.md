# ansible/post-destroy
Various playbooks for cluster post-destruction actions.
Actions that take place here are dependent on the cloud provider.
For example, AWS may require the removal of dynamic volumes,
left behind after the cluster's been destroyed.

The `destroy.py` module runs the `site.yaml` file in the directory
matching the terraform directory that was used for the cluster.

These scripts run in the local host as the cluster
(and all its cloud objects) no longer exists.
