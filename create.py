#!/usr/bin/env python

"""create.py - create the world.
"""

from __future__ import print_function

import argparse
import glob
import os
import sys
import time

import yaml

from utils import io

# Time (in seconds) to pause after creating cluster instances
# before invoking any ansible playbook. Added to give cluster
# time to fully initialise prior to installing OpenShift.
# (Not sure it's actually needed)
#
# But I do find the occasional inability to ssh.
# and when I re-run the affected part of the playbook all is fine.
# So maybe the machines are still initialising?
_PRE_ANSIBLE_PAUSE_S = 60.0


def _main(cli_args, deployment_name):
    """Deployment entry point.

    :param cli_args: The command-line arguments
    :type cli_args: ``list``
    :param deployment_name: The deployment file (excluding the extension)
    :type deployment_name: ``str``
    :returns: True on success
    :rtype: ``bool``
    """

    deployment_file = 'deployments/{}.yaml'.format(deployment_name)
    if not os.path.exists(deployment_file):
        io.error(('No config file ({}) for an "{}" deployment'.
                 format(deployment_file, deployment_name)))
        return False
    with open(deployment_file, 'r') as stream:
        deployment = yaml.load(stream)

    # There must be an openshift/inventories/<deployment> directory
    if not os.path.isdir('openshift/inventories/{}'.format(deployment_name)):
        io.error('Missing "openshift/inventories" directory')
        print('Expected to find the directory "{}" but it was not there.'.format(deployment_name))
        print('Every deployment must have a matching "inventories" directory')
        return False

    # -----
    # Hello
    # -----
    io.banner(deployment['name'], quiet=False)
    if not cli_args.auto_approve:
        confirmation_word =io.get_confirmation_word()
        confirmation = raw_input('Enter "{}" to CREATE this cluster: '.
                                 format(confirmation_word))
        if confirmation != confirmation_word:
            print('Phew! That was close!')
            return True

    # ------
    # Render (jinja2 files)
    # ------
    # Translate content of jinja2 template files.

    if not cli_args.skip_rendering:

        cmd = './render.py {}'.format(deployment_name)
        cwd = '.'
        rv = io.run(cmd, cwd, cli_args.quiet)
        if not rv:
            return False

    # ---------
    # Terraform
    # ---------
    # Create compute instances for the cluster.

    if not cli_args.skip_terraform:

        # The 'terraform' sub-directory.
        # The sub-directory where execution material is located.
        # For terraform the files either relate to the bastion or cluster
        # and are in subdirectories 'bastion' and 'cluster'.
        # The same applies to the ansible playbook - one will be
        # in 'bastion' and one will be in 'cluster'
        tf_sub_dir = 'bastion' if cli_args.bastion else 'cluster'

        t_dir = deployment['terraform']['dir']
        cmd = '~/bin/terraform init'
        cwd = 'terraform/{}/{}'.format(t_dir, tf_sub_dir)
        rv = io.run(cmd, cwd, cli_args.quiet)
        if not rv:
            return False

        cmd = '~/bin/terraform apply' \
              ' -auto-approve' \
              ' -state=.terraform.{}'.format(deployment_name)
        cwd = 'terraform/{}/{}'.format(t_dir, tf_sub_dir)
        rv = io.run(cmd, cwd, cli_args.quiet)
        if not rv:
            return False

    if cli_args.bastion:

        if not cli_args.skip_terraform:
            io.banner('time.sleep({})'.format(_PRE_ANSIBLE_PAUSE_S),
                      cli_args.quiet)
            time.sleep(_PRE_ANSIBLE_PAUSE_S)

        cmd = 'ansible-playbook' \
              ' ../ansible/bastion/site.yaml' \
              ' -e keypair_name={}' \
              ' -e deployment={}'.format(deployment['cluster']['keypair_name'],
                                         deployment_name)
        cwd = 'openshift'
        rv = io.run(cmd, cwd, cli_args.quiet)
        if not rv:
            return False

        # Done
        return True

    # -------
    # Ansible (A specific version)
    # -------
    # Install the ansible version name in the deployment file

    if not cli_args.skip_initialisation:

        cmd = 'pip install --upgrade pip --user'
        rv = io.run(cmd, '.', cli_args.quiet)
        if not rv:
            return False

        cmd = 'pip install ansible=={} --user'. \
            format(deployment['ansible']['version'])
        rv = io.run(cmd, '.', cli_args.quiet)
        if not rv:
            return False

    # --------
    # Checkout (OpenShift Ansible)
    # --------
    # Updates our OpenShift-Ansible sub-module
    # and checks out the revision defined by the deployment tag.

    if not cli_args.skip_initialisation:

        # Git sub-module initialisation
        cmd = 'git submodule update --init --remote'
        cwd = '.'
        rv = io.run(cmd, cwd, cli_args.quiet)
        if not rv:
            return False

        # OpenShift Ansible
        cmd = 'git checkout tags/{}'. \
            format(deployment['openshift']['ansible_tag'])
        cwd = 'openshift-ansible'
        rv = io.run(cmd, cwd, cli_args.quiet)
        if not rv:
            return False

    # -----------------
    # Pre-Ansible Pause
    # -----------------
    # Pre-OpenShift playbook.

    if not cli_args.skip_terraform and not cli_args.skip_openshift:

        io.banner('time.sleep({})'.format(_PRE_ANSIBLE_PAUSE_S),
                  cli_args.quiet)
        time.sleep(_PRE_ANSIBLE_PAUSE_S)

    # -------
    # Ansible (Pre-OpenShift)
    # -------

    if ('play' in deployment['ansible'] and
            'pre_os_create' in deployment['ansible']['play']):
        pre_os_create = deployment['ansible']['play']['pre_os_create']
        if not cli_args.skip_pre_openshift and pre_os_create:

            cmd = 'ansible-playbook {}.yaml'.format(pre_os_create)
            cwd = 'ansible/pre-os'
            rv = io.run(cmd, cwd, cli_args.quiet)
            if not rv:
                return False

    # -------
    # Ansible (OpenShift)
    # -------
    # Deploy OpenShift using the playbooks named in the deployment
    # from the checked-out version.

    if not cli_args.skip_openshift:

        for play in deployment['openshift']['play']:
            cmd = 'ansible-playbook ../openshift-ansible/playbooks/{}'.\
                format(play)
            cwd = 'openshift'
            rv = io.run(cmd, cwd, cli_args.quiet)
            if not rv:
                return False

    # -------
    # Ansible (Post-OpenShift)
    # -------

    if not cli_args.skip_post_openshift:

        cmd = 'ansible-playbook site.yaml'
        cwd = 'ansible/post-os'
        rv = io.run(cmd, cwd, cli_args.quiet)
        if not rv:
            return False

    # -------
    # Success
    # -------

    # OK if we get here...
    return True


if __name__ == '__main__':

    # Parse the command-line then run the main method.
    PARSER = argparse. \
        ArgumentParser(description='The Informatics Matters Orchestrator.'
                                   ' Creates the cloud-based execution'
                                   ' platform using tools like Terraform and'
                                   ' Ansible.')

    PARSER.add_argument('-q', '--quiet',
                        help='Decrease output verbosity',
                        action='store_true')

    PARSER.add_argument('-b', '--bastion',
                        help='Only create the bastion node',
                        action='store_true')

    PARSER.add_argument('-d', '--display-deployments',
                        help='Display known deployments',
                        action='store_true')

    PARSER.add_argument('-si', '--skip-initialisation',
                        help='Skip the initialisation stage',
                        action='store_true')

    PARSER.add_argument('-sr', '--skip-rendering',
                        help='Skip the Jinja2 rendering stage',
                        action='store_true')

    PARSER.add_argument('-st', '--skip-terraform',
                        help='Skip the terraform stage',
                        action='store_true')

    PARSER.add_argument('-spr', '--skip-pre-openshift',
                        help='Skip the Pre-OpenShift deployment stage',
                        action='store_true')

    PARSER.add_argument('-so', '--skip-openshift',
                        help='Skip the OpenShift deployment stage',
                        action='store_true')

    PARSER.add_argument('-spo', '--skip-post-openshift',
                        help='Skip the Post-OpenShift deployment stage',
                        action='store_true')

    PARSER.add_argument('--auto-approve',
                        help='Skip the confirmation question',
                        action='store_true')

    PARSER.add_argument('deployment', metavar='DEPLOYMENT',
                        type=str, nargs='?',
                        help='The name of the deployment')

    ARGS = PARSER.parse_args()

    deployments = glob.glob('deployments/*.yaml')
    # If there are no deployments, we can do nothing!
    if not deployments:
        print('The deployments directory is empty.')
        sys.exit(1)

    # Deal with special cases...
    # 1. 'display deployments'
    if ARGS.display_deployments:
        for deployment in deployments:
            # Display the deployment without the path
            # and removing the '.yaml' suffix.
            print(os.path.basename(deployment)[:-5])
        sys.exit(0)

    # If a deployment wasn't named, and there's more than one,
    # then the user must name one...
    if not ARGS.deployment:
        if len(deployments) > 1:
            print('ERROR: You need to supply the name of a deployment.'
                  ' Use --display-deployments to list them.')
            sys.exit(1)
        deployment_file = os.path.basename(deployments[0])[:-5]
    else:
        deployment_file = ARGS.deployment

    # Load the deployment's configuration file...
    config_file = 'deployments/{}.yaml'.format(deployment_file)
    if not os.path.exists(config_file):
        io.error('No config file ({}) for an "{}" deployment'.
               format(config_file, deployment_file))
        sys.exit(1)

    # Go...
    success = _main(ARGS, deployment_file)

    # Done
    # ...or failed and exhausted retry attempts!
    if not success:
        io.error('Failed to start cluster')
        # Return non-zero exit value to the shell...
        sys.exit(1)
