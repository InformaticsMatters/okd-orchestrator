#!/usr/bin/env python

"""io.py - I/O utilities.
"""

import os
import random
import subprocess
import sys

OKD_CONFIG_FILE = 'configuration.yaml'

_OKD_DEPLOYMENTS_DIRECTORY_ENV = 'TF_VAR_deployments_directory'


def error(msg):
    """Prints an error message.

    :param msg: The error
    :type msg: ``str``
    """
    print('ERROR: {}'.format(msg))


def get_confirmation_word():
    """Returns a confirmation word, that has to be entered by the user
    in order to continue the utility. This helps provide a safety mechanism
    to avoid installing or destroying the wrong deployment.

    :returns: A word from a selection
    :rtype: ``str``
    """
    return random.choice(['yes'])


def get_deployments_directory():
    """Returns a defined deployments directory, the value of
    the _OKD_DEPLOYMENTS_DIRECTORY_ENV environment variable,
    or 'deployments' if not defined or empty.

    :returns: The deployments directory or 'deployments'
    :rtype: ``str``
    """
    directory = os.environ.get(_OKD_DEPLOYMENTS_DIRECTORY_ENV)
    return directory if directory else 'deployments'


def get_deployment_config_name(deployment=None,
                               display_deployments=False):
    """Gets the configuration directory name from the deployments directory.
    A deployment does not have to be named if there's only one deployment.

    :param deployment: The deployment name (or None)
    :type deployment: ``str``
    :param display_deployments: Just display the deployments
    :type display_deployments: ``bool``
    :return: A deployment file name (the base-name)
    :rtype: ``str``
    """

    possible_deployments = os.listdir(get_deployments_directory())
    # An entry is only of use if it's a directory
    # and contains a 'configuration.yaml'.
    deployments = []
    for possible_deployment in possible_deployments:
        deployment_dir = os.path.join(get_deployments_directory(),
                                      possible_deployment)
        if os.path.isdir(deployment_dir):
            deployment_cfg = os.path.join(deployment_dir,
                                          OKD_CONFIG_FILE)
            if os.path.isfile(deployment_cfg):
                deployments.append(possible_deployment)

    # If there are no deployments, we can do nothing!
    if not deployments:
        print('Your deployments directory is empty')
        sys.exit(1)

    # Deal with special cases...
    # 1. 'display deployments'
    if display_deployments:
        for deployment in deployments:
            # Display the deployment (a directory name)
            print(deployment)
        sys.exit(0)

    # If a deployment wasn't named, and there's more than one,
    # then the user must name one...
    if not deployment:
        if len(deployments) > 1:
            print('ERROR: You need to supply the name of a deployment.\n'
                  '       The following are available:')
            for deployment in deployments:
                # Display the deployment without the path
                # and removing the '.yaml' suffix.
                print(deployment)
            sys.exit(1)
        deployment_dir = deployments[0]
    else:
        deployment_dir = deployment

    return deployment_dir


def banner(heading, e_dir='', full_heading=False, quiet=False):
    """Prints the string in a banner if not quiet. If not quiet,
    and given 'Blob' it prints:

    +------+
    | Blob |
    +------+

    Otherwise it prints the heading with a prompt symbol:

    > Blob

    :param heading: The message to turn into a banner.
    :type heading: ``str``
    :param e_dir: The execution directory.
    :type e_dir: ``str``
    :param full_heading: True to avoid creating a short heading.
                         This is ignored if 'quiet' is True.
    :type full_heading: ``bool``
    :param quiet: True if quiet (changes banner to more distinctive)
    :type quiet: ``bool``
    """
    if not quiet:
        if full_heading:
            the_heading = heading
        else:
            # Just the first two words (to avoid messy wrapping banners)
            the_heading = " ".join(heading.split()[:2])
            if the_heading != heading:
                the_heading += ' ...'
        heading_w = len(the_heading)
        in_dir = ''
        if e_dir:
            in_dir = '(in {})'.format(e_dir)
        print('')
        print('+' + '-' * (heading_w + 2) + '+')
        print('| {} | {}'.format(the_heading, in_dir))
        print('+' + '-' * (heading_w + 2) + '+')
    else:
        print('> {}'.format(heading))


def run(cmd, cwd, quiet=False):
    """Run a command using subprocess.Popen() returning True on success
    along with the process object.

    :param cmd: The command string
    :type cmd: ``str``
    :param cwd: The execution directory
    :type cwd: ``str``
    :param quiet: True if quiet. If quiet the the stdout/stderr streams
                  will be available in the returned process object.
    :type quiet: ``bool``
    :return: A typle of success and process object
    :rtype: ``tuple``
    """
    expanded_cmd = os.path.expanduser(cmd)
    banner(expanded_cmd, cwd, quiet)
    stdout_type = subprocess.PIPE if quiet else None
    process = subprocess.Popen(expanded_cmd.split(),
                               cwd=os.path.expanduser(cwd),
                               stderr=stdout_type,
                               stdout=stdout_type)
    process.wait()
    if process.returncode:
        error('Process failed (returncode={})'.format(process.returncode))
        print('# stderr follows...')
        if process.stderr:
            with process.stderr as err:
                for line in err:
                    print('# {}'.format(line.strip()))
        return False, process

    return True, process
