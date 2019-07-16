#########
Using NFS
#########

If you need to use NFS as a storage option in your cluster you can follow
this simple recipe. One advantage of NFS is that it is simple and provides you
with volumes that can be mounted **ReadWriteMany**.

You will need to provide a suitably formatted volume (attached to a designated
server instance), define your exports, open some ports and create suitable
**Persistent Volumes**.

We've documented a summary here but, for reference, you can refer to some
handy documentation: -

*   On `AWS`_ relating to making volumes available for use on Linux
*   The official OpenShift `NFS`_ documentation

.. _aws: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-using-volumes.html
.. _nfs: https://docs.openshift.com/container-platform/3.11/install_config/persistent_storage/persistent_storage_nfs.html#nfs-export-settings

Start the NFS server
====================
You should find that the ``nfs-server`` package is installed and running on
your designated NFS server (i.e. an infrastructure node in your cluster).
If not install it using your favorite package manager and start it::

    $ sudo yum install -y nfs-server
    $ sudo systemctl start nfs-server

Open NFS ports
==============
Depending on your NFS version you'll need to open suitable ports, OpenShift
does nto do this for you automatically. For **NFS v4.x** you need to open
``2049`` and ``111``::

    $ sudo iptables -I INPUT 1 -p tcp --dport 2049 -j ACCEPT
    $ sudo iptables -I INPUT 1 -p tcp --dport 111 -j ACCEPT

Create a storage volume
=======================
Create and attach a storage volume to your designated server. The volume
needs to be formatted (i.e. as ``ext4``) and mounted.

Check volumes with ``lsblk`` and use ``file`` to make sure it needs formatting
(as it'll report as *data*)::

    $ lsblk
    NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
    vda    253:0    0  160G  0 disk
    └─vda1 253:1    0  160G  0 part /
    vdb    253:16   0  150G  0 disk
    vdi    253:128  0  100G  0 disk /nfs-gp

    $ sudo file -s /dev/vdb
    /dev/vdb: data

For a volume available where the device (i.e. ``vdb``) is ``DEVICE`` to be
mounted at ``/nfs-gp`` on your server you'd typically run::

    $ sudo mkfs -t ext4 /dev/${DEVICE}
    $ sudo mkdir /nfs-gp
    $ sudo mount /dev/${DEVICE} /nfs-gp

Add your drive to ``fstab`` to ensure they're re-attached and available after
a server reboot by referring to the
**Automatically Mount an Attached Volume After Reboot** section of the
handy `AWS`_ documentation.

Define your exports
===================
Create directories on your NFS mount for each **PersistentVolume** you
plan to create and set permissions and ownership. A good pattern is to
clearly name the directories so they're obvious that they belong to
a **PersistentVolume** by prefixing each with ``pv-``::

    $ sudo cd /nfs-gp
    $ sudo mkdir pv-data-dir
    $ sudo chmod -R 777 pv-*
    $ sudo chown -R nfsnobody.nfsnobody pv-*

Create an export file (i.e. ``my.exports``), typically in ``/etc/exports.d``,
containing an export line for each directory you've created::

    /nfs-gp/pv-data-dir *(rw,root_squash)

Then, bounce the NFS server and check the exports::

    $ sudo systemctl restart nfs-server
    $ showmount -e localhost

Testing
=======
Go to another server in your cluster and test that you can mount the
exported volume to a locally-created directory. So, on another server,
where ``SERVER`` is the server hosting the NFS volume, if the following is
successful you're ready to use NFS::

    $ sudo mkdir /blob
    $ sudo mount -t nfs ${SERVER}:/nfs-gp/pv-data-dir /blob

Then un-mount and remove the test directory::

    $ sudo umount /blob
    $ sudo rmdir /blob

Create PersistentVolumes and Claims
===================================
OpenShift applications will need a **PersistentVolume** for each NFS directory.
Application developers will also need to provide a suitable matching
**PersistentVolumeClaim**.

Typically, from the master instance (or any server with compatible OpenShift
OC command-line tools), define and create a **PersistentVolume**
for each volume you've exported in a YAML file.

For the above example a **PV** YAML file that permits storage of 10Gi on the
server ``prod-infra`` for use by *any* application might look something like
this::

    kind: PersistentVolume
    apiVersion: v1
    metadata:
      name: pv-data-dir
    spec:
      capacity:
        storage: 10Gi
      accessModes:
      - ReadWriteMany
      persistentVolumeReclaimPolicy: Recycle
      nfs:
        server: prod-infra
        path: /nfs-gp/pv-squonk-work-dir
    claimRef:
      name: squonk-work-dir-pvc
      namespace: ${APP_NAMESPACE}


And installed and made available to OpenShift applications with the command::

    $ oc create -f my-pv.yaml

The corresponding application's **PersistentVolumeClaim** might look
something like this::

    kind: PersistentVolumeClaim
    apiVersion: v1
    metadata:
      name: django-data-dir-pvc
      namespace: django-app
    spec:
      volumeName: pv-data-dir
      accessModes:
      - ReadWriteMany
      resources:
        requests:
          storage: 10Gi

For more details about **PersistentVolumes** and **Claims**
you should refer to the OpenShift documentation on `binding`_
persistent volumes by labels.

.. _binding: https://docs.okd.io/3.11/install_config/storage_examples/binding_pv_by_label.html#binding-pv-by-label-pv-with-labels
