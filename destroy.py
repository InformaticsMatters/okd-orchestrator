#!/usr/bin/env python

"""destroy.py - destroy the world.
"""

from __future__ import print_function

import argparse
from builtins import input
import codecs
from munch import Munch
import os
import sys

import yaml

from utils import io

# The deployments directory.
OKD_DEPLOYMENTS_DIRECTORY = io.get_deployments_directory()

OKD_DEFAULT_CLUSTER_SSH_USER = 'centos'


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

    config_file = os.path.join(OKD_DEPLOYMENTS_DIRECTORY,
                               chosen_deployment_name,
                               io.get_deployment_config_filename(
                                   chosen_deployment_name))
    if not os.path.isfile(config_file):
        io.error('Configuration file does not exist in the deployment ({})'.
                 format(chosen_deployment_name))
        return False
    with codecs.open(config_file, 'r', 'utf8') as stream:
        deployment = Munch.fromDict(yaml.load(stream))

    # There must be an okd/inventories directory
    inventory_dir = deployment.okd.inventory_dir
    if not os.path.isdir('okd/inventories/{}'.format(inventory_dir)):
        io.error('Missing "okd/inventories" directory')
        print('Expected to find the directory "{}" but it was not there.'.
              format(chosen_deployment_name))
        print('Every deployment must have a matching "inventories" directory')
        return False

    # If the cluster SSH user is not defined,
    # insert it.
    if 'ssh_user' not in deployment.cluster:
        print('Setting default SSH user "{}"'.format(OKD_DEFAULT_CLUSTER_SSH_USER))
        deployment.cluster.ssh_user = OKD_DEFAULT_CLUSTER_SSH_USER

    # -----
    # Hello
    # -----
    io.banner(deployment.name, full_heading=True, quiet=False)

    if not cli_args.now:

        # Display the orchestration description
        # (f there is one)
        if deployment.description:
            io.description(deployment.description)

        # User said "now" so don't ask for confirmation
        print('CAUTION You are about to destroy the cluster.')
        print('======= Are you sure you want to do this?')
        print()

        confirmation_word = io.get_confirmation_word()
        confirmation = input('Enter "{}" to DESTROY this deployment: '.
                             format(confirmation_word))
        if confirmation != confirmation_word:
            print('Phew! That was close!')
            return True

    # ------
    # Render
    # ------
    if not cli_args.skip_rendering:

        cmd = './render.py {} --ssh-user {}'.\
            format(chosen_deployment_name,
                   deployment.cluster.ssh_user)
        cwd = '.'
        rv, _ = io.run(cmd, cwd, cli_args.quiet)
        if not rv:
            return False

    # ---------
    # Terraform
    # ---------
    # Destroy the cluster.

    t_dir = deployment.cluster.terraform_dir
    cmd = 'terraform init'
    cwd = 'terraform/{}'.format(t_dir)
    rv = io.run(cmd, cwd, cli_args.quiet)
    if not rv:
        return False

    t_dir = deployment.cluster.terraform_dir
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

    PARSER.add_argument('-sr', '--skip-rendering',
                        help='Skip the Jinja2 rendering stage',
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
