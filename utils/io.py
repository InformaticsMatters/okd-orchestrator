#!/usr/bin/env python

"""io.py - I/O utilities.
"""

import os
import random
import subprocess
import sys

_OKD_CONFIG_BASE = 'configuration'
_OKD_CONFIG_EXTENSIONS = ['.yml', '.yaml']

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
    """Returns a defined deployments directory. This is the value of
    the _OKD_DEPLOYMENTS_DIRECTORY_ENV environment variable if it's defined,
    or 'deployments'.

    :returns: The deployments directory or 'deployments'
    :rtype: ``str``
    """
    directory = os.environ.get(_OKD_DEPLOYMENTS_DIRECTORY_ENV)
    return directory if directory else 'deployments'


def get_deployment_config_filename(deployment):
    """Returns the configuration file from the configuration directory.
    If there are two files then the one with the shortened extension ('.yml) is
    returned.

    :param deployment: The deployment directory
    :type deployment: ``str``
    :returns: The configuration file name (without the directory)
              or None if a configuration file does not exist
    '"""
    deployment_dir = os.path.join(get_deployments_directory(), deployment)
    for ext in _OKD_CONFIG_EXTENSIONS:
        filename = _OKD_CONFIG_BASE + ext
        if os.path.isfile(os.path.join(deployment_dir, filename)):
            return filename
    # Not found...
    return None


def get_deployment_config_name(deployment=None,
                               display_deployments=False):
    """Gets the configuration directory name from the deployments directory.
    A deployment does not have to be named if there's only one deployment.
    A deployment exists if s directory exists that contains a 'configuration'
    file.

    A configuration file ends '.yaml' or .'yml'.

    :param deployment: The deployment name (or None)
    :type deployment: ``str``
    :param display_deployments: Just display the deployments
    :type display_deployments: ``bool``
    :return: A deployment file name (the base-name)
    :rtype: ``str``
    """

    possible_deployments = []
    deployment_dir = get_deployments_directory()
    if not os.path.isdir(deployment_dir):
        print('Ooops - your deployments directory does not exist (%s)'
              % deployment_dir)
        sys.exit(1)

    # An entry is only of use if it's a directory
    # and contains a 'configuration.yaml'.
    deployments = []
    possible_deployments += os.listdir(deployment_dir)
    for possible_deployment in possible_deployments:
        deployment_dir = os.path.join(get_deployments_directory(),
                                      possible_deployment)
        if os.path.isdir(deployment_dir):
            if get_deployment_config_filename(possible_deployment):
                deployments.append(possible_deployment)

    # If there are no deployments, we can do nothing!
    if not deployments:
        print('Your deployments directory is empty')
        sys.exit(1)

    # Deal with special cases...
    # 1. 'display deployments'
    if display_deployments:
        for deployment in sorted(deployments):
            # Display the deployment (a directory name)
            print(deployment)
        sys.exit(0)

    # If a deployment wasn't named, and there's more than one,
    # then the user must name one...
    if not deployment:
        if len(deployments) > 1:
            print('ERROR: You need to supply the name of a deployment.\n'
                  '       The following are available:')
            for deployment in sorted(deployments):
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


def description(deployment_description):
    """Renders the deployment description to the screen.
    Usually used after the initial banner.

    :param deployment_description: A description
    """
    leader = '| Description: '
    rendered = ''
    line = leader
    for word in deployment_description.split():
        if len(line) > 60:
            rendered += line + '\n'
            line = ' ' * len(leader)
        line += word + ' '
    if line:
        rendered += line.rstrip()
    print(rendered.strip() + '\n')


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
