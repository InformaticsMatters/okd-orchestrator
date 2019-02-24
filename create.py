#!/usr/bin/env python

"""create.py - create the world.
"""

from __future__ import print_function

import argparse
from builtins import input
import codecs
from munch import DefaultMunch
import os
import sys

import yaml

from utils import io, templater

# Environment variable used to hold the OKD admin and developer passwords.
OKD_ADMIN_PASSWORD_ENV = 'TF_VAR_okd_admin_password'
OKD_DEVELOPER_PASSWORD_ENV = 'TF_VAR_okd_developer_password'
OKD_KEYPAIR_NAME_ENV = 'TF_VAR_keypair_name'
OKD_CERTBOT_EMAIL_ENV = 'TF_VAR_master_certbot_email'
OKD_DEPLOYMENTS_DIRECTORY = io.get_deployments_directory()

# The list of supported deployment configuration file versions.
# The config file contains a version number, we only handle
# those that are in this list.
#
# As soon as backwards support is lost (an unsupported)
# the version must be removed form the list ans replaced by a new one.
SUPPORTED_DEPLOYMENT_VERSIONS = [1]


def _main(cli_args, chosen_deployment_name):
    """Deployment entry point.

    :param cli_args: The command-line arguments
    :type cli_args: ``list``
    :param chosen_deployment_name: The deployment file
    :type chosen_deployment_name: ``str``
    :returns: True on success
    :rtype: ``bool``
    """

    config_file = os.path.join(OKD_DEPLOYMENTS_DIRECTORY,
                               chosen_deployment_name,
                               io.get_deployment_config_filename(
                                   chosen_deployment_name))
    if not os.path.isfile(config_file):
        print('Config file does not exist ({})'.
              format(chosen_deployment_name))
        return False
    with codecs.open(config_file, 'r', 'utf8') as stream:
        deployment = DefaultMunch.fromDict(yaml.load(stream))

    # First check:
    # is the version present
    # and do we support it?
    if 'version' not in deployment:
        print('The deployment configuration has no version.')
        return False
    if deployment.version not in SUPPORTED_DEPLOYMENT_VERSIONS:
        supported_versions = str(SUPPORTED_DEPLOYMENT_VERSIONS[0])
        for version in SUPPORTED_DEPLOYMENT_VERSIONS[1:]:
            supported_versions += ', {}'.format(version)
        print('The deployment configuration file version ({})'
              ' is not supported.'.format(deployment.version))
        print('Supported versions are: {}'.format(supported_versions))
        return False

    # There must be an okd/inventories directory
    inventory_dir = deployment.okd.inventory_dir
    if not os.path.isdir('okd/inventories/{}'.format(inventory_dir)):
        print('Missing "okd/inventories" directory')
        print('Expected to find the inventory directory "{}"'
              ' but it was not there.'.format(inventory_dir))
        print('Every deployment must have an "inventories" directory')
        return False

    # -----
    # Hello
    # -----
    io.banner(deployment.name, full_heading=True, quiet=False)
    if not cli_args.auto_acknowledge and not cli_args.just_plan:

        # Display the orchestration description
        # (f there is one)
        if deployment.description:
            io.description(deployment.description)

        confirmation_word = io.get_confirmation_word()
        target = 'CREATE the Cluster' \
            if cli_args.cluster else 'INSTALL OpenShift/OKD'
        confirmation = input('Enter "{}" to {}: '.
                             format(confirmation_word, target))
        if confirmation != confirmation_word:
            print('Phew! That was close!')
            return True

    # Some key information...
    okd_admin_password = os.environ.get(OKD_ADMIN_PASSWORD_ENV)
    if not okd_admin_password:
        io.error('You must define {}'.format(OKD_ADMIN_PASSWORD_ENV))

    okd_api_hostname = deployment.cluster.public_hostname
    okd_api_port = deployment.cluster.api_port

    # -------
    # Ansible (A specific version)
    # -------
    # Install the ansible version name in the deployment file

    cmd = 'pip install --upgrade pip --user'
    rv, _ = io.run(cmd, '.', cli_args.quiet)
    if not rv:
        return False

    cmd = 'pip install ansible=={} --user'. \
        format(deployment.okd.ansible_version)
    rv, _ = io.run(cmd, '.', cli_args.quiet)
    if not rv:
        return False

    t_dir = deployment.cluster.terraform_dir
    if cli_args.cluster:

        # ------
        # Render (jinja2 files)
        # ------
        # Translate content of Jinja2 template files
        # using the deployment configuration's YAML file content.

        if not cli_args.skip_rendering:

            cmd = './render.py {}'.format(chosen_deployment_name)
            cwd = '.'
            rv, _ = io.run(cmd, cwd, cli_args.quiet)
            if not rv:
                return False

        # If the deployment file has a 'my_machines' section
        # then we assume the user's provided their own cluster
        # and the Terraform step is not needed.
        if 'my_machines' in deployment:

            # -----------------
            # Manual Templating
            # -----------------
            # The user has provided their own cluster
            # and defined it in the my_machines section
            # of their deployment configuration.
            #
            # Here we process the rendered inventory files
            # just as Terraform would do.
            io.banner('Templating ...')
            print('inventory')
            if not templater.render(deployment):
                return False

            print('bastion/inventory')
            file_name = 'ansible/bastion/inventory.yaml.tpl'
            if not templater.\
                    render(deployment,
                           template_file_name=file_name):
                return False

            print('post-okd/inventory')
            file_name = 'ansible/post-okd/inventory.yaml.tpl'
            if not templater. \
                    render(deployment,
                           template_file_name=file_name,
                           admin_password=okd_admin_password):
                return False

        else:

            # ---------
            # Terraform
            # ---------
            # Create compute instances for the cluster.

            cmd = 'terraform init'
            cwd = 'terraform/{}'.format(t_dir)
            rv, _ = io.run(cmd, cwd, cli_args.quiet)
            if not rv:
                return False

            # Plan or Apply?
            action = 'plan' if cli_args.just_plan else 'apply -auto-approve'
            cmd = 'terraform {}' \
                  ' -state=.terraform.{}'.format(action,
                                                 chosen_deployment_name)
            cwd = 'terraform/{}'.format(t_dir)
            rv, _ = io.run(cmd, cwd, cli_args.quiet)
            if not rv:
                return False

        if cli_args.just_plan:
            # Just plan means just that...
            return True

        # -------
        # Ansible
        # -------
        # Run the bastion site file.

        if not cli_args.skip_pre_okd:

            extra_env = ''
            if deployment.okd.certificates:
                if deployment.okd.certificates.generate_api_cert:

                    certbot_email = os.environ.get(OKD_CERTBOT_EMAIL_ENV)
                    if not certbot_email:
                        io.error('You must define {}'.
                                 format(OKD_CERTBOT_EMAIL_ENV))
                        return False

                    extra_env += ' -e master_cert_email="{}"'.\
                        format(certbot_email)
                    extra_env += ' -e public_hostname="{}"'. \
                        format(deployment.cluster.public_hostname)
                else:

                    # User-supplied certificates -
                    # expect a vault password file
                    # in the deployment directory
                    extra_env += ' --vault-password-file' \
                                 ' {}/{}/vault-pass.txt'.\
                        format(OKD_DEPLOYMENTS_DIRECTORY,
                               chosen_deployment_name)

            if OKD_DEPLOYMENTS_DIRECTORY != 'deployments':
                extra_env += ' -e deployments_directory="{}"'.\
                    format(OKD_DEPLOYMENTS_DIRECTORY)
            else:
                extra_env += ' -e deployments_directory="../../deployments"'

            keypair_name = os.environ.get(OKD_KEYPAIR_NAME_ENV)
            if not keypair_name:
                io.error('You must define {}'.format(OKD_KEYPAIR_NAME_ENV))
                return False

            cmd = 'ansible-playbook site.yaml' \
                  ' {}' \
                  ' -e keypair_name={}' \
                  ' -e inventory_dir={}' \
                  ' -e deployment_name={}'.format(extra_env,
                                                  keypair_name,
                                                  deployment.okd.inventory_dir,
                                                  chosen_deployment_name)
            cwd = 'ansible/bastion'
            rv, _ = io.run(cmd, cwd, cli_args.quiet)
            if not rv:
                return False

        # Now expose the Bastion's IP...

        if 'my_machines' in deployment:

            # Simulate the final step in Terraform,
            # i.e. exposing the bastion.
            # Doing this simplifies things for the user
            # i.e. "it looks and feels the same"

            io.banner('terraform output ...')
            print('bastion_ip = {}'.format(deployment.my_machines.bastion))

        else:

            cmd = 'terraform output' \
                  ' -state=.terraform.{}'.format(chosen_deployment_name)
            cwd = 'terraform/{}'.format(t_dir)
            rv, _ = io.run(cmd, cwd, cli_args.quiet)
            if not rv:
                return False

        # Leave.
        return True

    # If we get here we're installing OpenShift/OKD
    # (on a cluster that is assumed to exist)...

    # -----
    # Clone (OpenShift Ansible Repo)
    # -----
    # ...and checkout the revision defined by the deployment tag.

    if not cli_args.skip_okd:

        # If the expected clone directory does not exist
        # then clone OpenShift Ansible.
        if not os.path.exists('openshift-ansible'):

            cmd = 'git clone' \
                  ' https://github.com/openshift/openshift-ansible.git' \
                  ' --no-checkout'
            cwd = '.'
            rv, _ = io.run(cmd, cwd, cli_args.quiet)
            if not rv:
                return False

        # Checkout the required OpenShift Ansible TAG
        cmd = 'git checkout tags/{}'. \
            format(deployment.okd.ansible_tag)
        cwd = 'openshift-ansible'
        rv, _ = io.run(cmd, cwd, cli_args.quiet)
        if not rv:
            return False

    # -------
    # Ansible (Pre-OKD)
    # -------

    if not cli_args.skip_pre_okd:

        extra_env = ''
        if deployment.okd.certificates and\
                deployment.okd.certificates.generate_api_cert:
            extra_env += ' -e public_hostname={}'. \
                format(deployment.cluster.public_hostname)
        cmd = 'ansible-playbook site.yaml' \
              ' {}' \
              ' -i ../../okd/inventories/{}/inventory.yaml'.\
            format(extra_env, inventory_dir)
        cwd = 'ansible/pre-okd'
        rv, _ = io.run(cmd, cwd, cli_args.quiet)
        if not rv:
            return False

    # -------
    # Ansible (OKD)
    # -------
    # Deploy using the playbooks named in the deployment
    # (from the checked-out version).

    if not cli_args.skip_okd:

        for play in deployment.okd.play:
            cmd = 'ansible-playbook ../openshift-ansible/playbooks/{}.yml' \
                  ' -i inventories/{}/inventory.yaml'.\
                format(play, inventory_dir)
            cwd = 'okd'
            rv, _ = io.run(cmd, cwd, cli_args.quiet)
            if not rv:
                return False

    # -------
    # Ansible (Post-OKD)
    # -------

    if not cli_args.skip_post_okd:

        # Always run the 'site' playbook.
        # This adds the OKD admin and (optional) developer user accounts
        # and other common things like template deployment.
        #
        # The following variables are made available to all the playbooks: -
        #
        # - okd_api_hostname
        # - okd_admin
        # - okd_admin_password

        extra_env = ''
        dev_password = os.environ.get(OKD_DEVELOPER_PASSWORD_ENV)
        if dev_password:
            extra_env += ' -e okd_developer_password={}'.format(dev_password)
        # The template namespace
        # (optionally defined in the configuration)
        if deployment.okd.template and deployment.okd.template.namespace:
            template_namespace = deployment.okd.template.namespace
            extra_env += ' -e template_namespace={}'.format(template_namespace)
        cmd = 'ansible-playbook site.yaml' \
              '{}' \
              ' -e okd_api_hostname=https://{}:{}' \
              ' -e okd_admin=admin' \
              ' -e okd_admin_password={}' \
              ' -e okd_deployment={}'. \
            format(extra_env,
                   okd_api_hostname, okd_api_port,
                   okd_admin_password, chosen_deployment_name)
        cwd = 'ansible/post-okd'
        rv, _ = io.run(cmd, cwd, cli_args.quiet)
        if not rv:
            return False

        # Now iterate through the plays listed in the cluster's
        # 'post_okd' list...

        if deployment.okd.post_okd:
            for play in deployment.okd.post_okd:
                # Any user-defined 'extra' variables?
                play_vars = ''
                if play.vars:
                    for var in play.vars:
                        play_vars += '-e {} '.format(var)
                    play_vars = play_vars[:-1]
                # Run the user playbook...
                cmd = 'ansible-playbook playbooks/{}/deploy.yaml' \
                    ' -e okd_api_hostname=https://{}:{}' \
                    ' -e okd_admin=admin' \
                    ' -e okd_admin_password={}' \
                    ' -e okd_deployment={}' \
                    ' {}'.\
                    format(play.play,
                           okd_api_hostname, okd_api_port,
                           okd_admin_password, chosen_deployment_name,
                           play_vars)
                cwd = 'ansible/post-okd'
                rv, _ = io.run(cmd, cwd, cli_args.quiet)
                if not rv:
                    return False

    # -------
    # Success
    # -------

    # OK if we get here.
    # Cluster created and OKD installed.
    return True


if __name__ == '__main__':

    # Parse the command-line then run the main method.
    PARSER = argparse. \
        ArgumentParser(description='The Informatics Matters Orchestrator.'
                                   ' Creates the OpenShift/OKD cloud-based'
                                   ' execution platform using Terraform and'
                                   ' Ansible.')

    PARSER.add_argument('-q', '--quiet',
                        help='Decrease output verbosity',
                        action='store_true')

    PARSER.add_argument('-c', '--cluster',
                        help='Create the cluster,'
                             ' do not install OpenShift/OKD',
                        action='store_true')

    PARSER.add_argument('-j', '--just-plan',
                        help='Just plan the terraform orchestration,'
                             ' not not apply it. This field only makes'
                             ' sense if using --cluster',
                        action='store_true')

    PARSER.add_argument('-o', '--okd',
                        help='Create the OpenShift/OKD installation'
                             ' (on an existing cluster)',
                        action='store_true')

    PARSER.add_argument('-d', '--display-deployments',
                        help='Display known deployments',
                        action='store_true')

    PARSER.add_argument('-sr', '--skip-rendering',
                        help='Skip the Jinja2 rendering stage',
                        action='store_true')

    PARSER.add_argument('-spr', '--skip-pre-okd',
                        help='Skip the Pre-OpenShift/OKD deployment stage',
                        action='store_true')

    PARSER.add_argument('-so', '--skip-okd',
                        help='Skip the OpenShift/OKD deployment stage',
                        action='store_true')

    PARSER.add_argument('-spo', '--skip-post-okd',
                        help='Skip the Post-OpenShift/OKD deployment stage',
                        action='store_true')

    PARSER.add_argument('--auto-acknowledge',
                        help='Skip the create confirmation question',
                        action='store_true')

    PARSER.add_argument('deployment', metavar='DEPLOYMENT',
                        type=str, nargs='?',
                        help='The name of the deployment')

    ARGS = PARSER.parse_args()

    # Go...
    deployment_name = io.get_deployment_config_name(ARGS.deployment,
                                                    ARGS.display_deployments)

    # User must have specified 'cluster' or 'open-shift'
    if not ARGS.cluster and not ARGS.okd:
        # If 'destroy' exists then we need to know whether
        # we're creating a cluster or an OKD deployment
        # (on an existing cluster)
        if os.path.isfile('destroy.py'):
            io.error('Must specify --cluster or --okd')
            sys.exit(1)
        # Otherwise we assume --okd
        ARGS.okd = True
    if ARGS.just_plan and not ARGS.cluster:
        io.error('Must specify --cluster if using --skip-plan')
        sys.exit(1)

    # The OKD admin password must be set.
    if not os.environ.get(OKD_ADMIN_PASSWORD_ENV):
        io.error('You must define the "{}" environment variable'.
                 format(OKD_ADMIN_PASSWORD_ENV))
        sys.exit(1)

    success = _main(ARGS, deployment_name)

    # Done
    # ...or failed and exhausted retry attempts!
    if not success:
        io.error('Failed to create')
        # Return non-zero exit value to the shell...
        sys.exit(1)
