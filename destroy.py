#!/usr/bin/env python

"""destroy.py - destroy the world.
"""

from __future__ import print_function

import argparse
from builtins import input
import codecs
import os
import sys

import yaml

from utils import io

# The deployments directory.
OKD_DEPLOYMENTS_DIRECTORY = io.get_deployments_directory()


def _main(cli_args, chosen_deployment_name):
    """Destruction entry point.

    :param cli_args: The command-line arguments
    :type cli_args: ``list``
    :param chosen_deployment_name: The deployment file
                                   (excluding the extension)
    :type chosen_deployment_name: ``str``
    :return: True on success
    :rtype: ``bool``
    """

    file = os.path.join(OKD_DEPLOYMENTS_DIRECTORY,
                        chosen_deployment_name + '.yaml')
    if not os.path.isfile(file):
        io.error(('Config file does not exist ({})'.
                  format(chosen_deployment_name)))
        return False
    with codecs.open(file, 'r', 'utf8') as stream:
        deployment = yaml.load(stream)

    # There must be an okd/inventories directory
    inventory_dir = deployment['okd']['inventory_dir']
    if not os.path.isdir('okd/inventories/{}'.format(inventory_dir)):
        io.error('Missing "okd/inventories" directory')
        print('Expected to find the directory "{}" but it was not there.'.
              format(chosen_deployment_name))
        print('Every deployment must have a matching "inventories" directory')
        return False

    # -----
    # Hello
    # -----
    io.banner(deployment['name'], full_heading=True, quiet=False)

    if not cli_args.now:

        # User said "now" so don't ask for confirmation
        print()
        print('CAUTION You are about to destroy the cluster.')
        print('------- Are you sure you want to do this?')
        print()

        confirmation_word = io.get_confirmation_word()
        confirmation = input('Enter "{}" to DESTROY this deployment: '.
                             format(confirmation_word))
        if confirmation != confirmation_word:
            print('Phew! That was close!')
            return True

    # ---------
    # Terraform
    # ---------
    # Destroy the cluster.

    t_dir = deployment['terraform']['dir']
    cmd = 'terraform init'
    cwd = 'terraform/{}'.format(t_dir)
    rv = io.run(cmd, cwd, cli_args.quiet)
    if not rv:
        return False

    t_dir = deployment['terraform']['dir']
    cmd = 'terraform destroy -force -state=.terraform.{}'.\
        format(chosen_deployment_name)
    cwd = 'terraform/{}'.format(t_dir)
    rv = io.run(cmd, cwd, cli_args.quiet)

    # ----------------------
    # Ansible (Post-Destroy)
    # ----------------------
    # If there's an 'ansible/post-destroy/<t_dir>' directory
    # we run the site.yaml file in it. There is no inventory,
    # the ansible script runs locally.
    if os.path.exists('ansible/post-destroy/{}'.format(t_dir)):

        cmd = 'ansible-playbook site.yaml'
        cwd = 'ansible/post-destroy/{}'.format(t_dir)
        rv, _ = io.run(cmd, cwd, cli_args.quiet)
        if not rv:
            return False

    return rv


if __name__ == '__main__':

    # Parse the command-line then run the main method.
    PARSER = argparse.\
        ArgumentParser(description='The Informatics Matters Orchestrator.'
                                   ' Destroys the OKD cloud-based execution'
                                   ' platform.')

    PARSER.add_argument('-q', '--quiet', help="Decrease output verbosity",
                        action='store_true')

    PARSER.add_argument('-d', '--display-deployments',
                        help='Display known deployments',
                        action='store_true')

    PARSER.add_argument('-n', '--now', help="Destroy without confirmation",
                        action='store_true')

    PARSER.add_argument('deployment', metavar='DEPLOYMENT',
                        type=str, nargs='?',
                        help='The name of the deployment')

    ARGS = PARSER.parse_args()

    # Go...
    deployment_name = io.get_deployment_config_name(ARGS.deployment,
                                                    ARGS.display_deployments)
    success = _main(ARGS, deployment_name)

    # Done
    # ...or failed and exhausted retry attempts!
    if not success:
        io.error('Failed to destroy the cluster.')
        # Return non-zero exit value to the shell...
        sys.exit(1)
