#!/usr/bin/env python

"""destroy.py - destroy the world.
"""

from __future__ import print_function

import argparse
from builtins import input
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

    # There must be an openshift/inventories directory
    inventory_dir = deployment['openshift']['inventory_dir']
    if not os.path.isdir('openshift/inventories/{}'.format(inventory_dir)):
        io.error('Missing "openshift/inventories" directory')
        print('Expected to find the directory "{}" but it was not there.'.
              format(deployment_name))
        print('Every deployment must have a matching "inventories" directory')
        return False

    # -----
    # Hello
    # -----
    io.banner(deployment['name'], full_heading=True, quiet=False)

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
    cwd = 'terraform/{}/cluster'.format(t_dir)
    rv = io.run(cmd, cwd, cli_args.quiet)
    if not rv:
        return False

    t_dir = deployment['terraform']['dir']
    cmd = 'terraform destroy -force -state=.terraform.{}'.\
        format(deployment_name)
    cwd = 'terraform/{}/cluster'.format(t_dir)
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

    # We must have a deployment defined if we get here.
    # Even if there is just one, it's safe to force the
    # user to specify the deployment.
    if not ARGS.deployment:
        print('ERROR: You need to supply the name of a deployment.'
              ' The following are available:')
        for deployment in deployments:
            # Display the deployment without the path
            # and removing the '.yaml' suffix.
            print(os.path.basename(deployment)[:-5])
        sys.exit(1)
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
