#!/usr/bin/env python

"""destroy.py - destroy the world.
"""

from __future__ import print_function

import argparse
import glob
import os
import sys

import yaml

from utils import io


def _main(cli_args, deployment_name):
    """Destruction entry point.

    :param cli_args: The command-line arguments
    :type cli_args: ``list``
    :param deployment_name: The deployment file (excluding the extension)
    :type deployment_name: ``str``
    :return: True on success
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
        print('Expected to find the directory "{}" but it was nto there.'.
              format(deployment_name))
        print('Every deployment must have a matching "inventories" directory')
        return False

    # -----
    # Hello
    # -----
    io.banner(deployment['name'], full_heading=True, quiet=False)

    # Caution if bastion
    if cli_args.bastion:
        print()
        print('CAUTION You are about to destroy the bastion.')
        print('------- Have you destroyed all the clusters created from it?')
        print('        If not you risk leaving a large number of cloud')
        print('        objects orphaned that might otherwise be difficult to')
        print('        delete.')
        print('        Are you sure you want to destroy the bastion?')
        print()

    confirmation_word = io.get_confirmation_word()
    confirmation = raw_input('Enter "{}" to DESTROY this deployment: '.
                             format(confirmation_word))
    if confirmation != confirmation_word:
        print('Phew! That was close!')
        return True

    # -------
    # Ansible
    # -------
    if ('play' in deployment['ansible'] and
            'pre_os_destroy' in deployment['ansible']['play']):
        # Undo local (bastion) /etc/hosts?
        pre_os_destroy = deployment['ansible']['play']['pre_os_destroy']
        if pre_os_destroy:
            cmd = 'ansible-playbook {}.yaml'.format(pre_os_destroy)
            cwd = 'ansible/pre-os'
            rv = io.run(cmd, cwd, cli_args.quiet)
            if not rv:
                return False

    # ---------
    # Terraform
    # ---------
    # Destroy the cluster.

    # The 'action' sub-directory.
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

    t_dir = deployment['terraform']['dir']
    cmd = '~/bin/terraform destroy -force -state=.terraform.{}'.\
        format(deployment_name)
    cwd = 'terraform/{}/{}'.format(t_dir, tf_sub_dir)
    rv = io.run(cmd, cwd, cli_args.quiet)

    return rv


if __name__ == '__main__':

    # Parse the command-line then run the main method.
    PARSER = argparse.\
        ArgumentParser(description='The Informatics Matters Orchestrator.'
                                   ' Destroys the cloud-based execution'
                                   ' platform.')

    PARSER.add_argument('-q', '--quiet', help="Decrease output verbosity",
                        action='store_true')

    PARSER.add_argument('-b', '--bastion',
                        help='Destroy the bastion node.'
                             ' If not set the compute cluster is destroyed.',
                        action='store_true')

    PARSER.add_argument('-d', '--display-deployments',
                        help='Display known deployments',
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

    # We must have a deployment defined if we get here...
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
        io.error('Failed to destroy the cluster.')
        # Return non-zero exit value to the shell...
        sys.exit(1)
