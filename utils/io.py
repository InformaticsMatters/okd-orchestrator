#!/usr/bin/env python

"""io.py - I/O utilities.
"""

import os
import random
import subprocess


def error(msg):
    """Prints an error message.

    :param msg: The error
    :type msg: ``str``
    """
    print('ERROR: {}'.format(msg))


def get_confirmation_word():
    """Returns a confirmation word, that has to be entered by the user
    in order to continue the utility. This helps provide a safety mechanism
    to avoid installing or destoryin the wrong deployment.

    :returns: A word from a selection
    :rtype: ``str``
    """
    return random.choice(['fine', 'go', 'ok', 'okay', 'start', 'yes'])


def banner(heading, quiet=False):
    """Prints the string in a banner if not quiet. If not quiet,
    and given 'Blob' it prints:

    +------+
    | Blob |
    +------+

    Otherwise it prints the heading with a prompt symbol:

    > Blob

    :param heading: The message to turn into a banner.
    :type heading: ``str``
    :param quiet: True if quiet (changes banner to more distinctive)
    :type quiet: ``bool``
    """
    if not quiet:
        heading_w = len(heading)
        print('')
        print('+' + '-' * (heading_w + 2) + '+')
        print('| {} |'.format(heading))
        print('+' + '-' * (heading_w + 2) + '+')
    else:
        print('> {}'.format(heading))


def run(cmd, cwd, quiet=False):
    """Run a command using subprocess.Popen() returning True on success.

    :param cmd: The command string
    :type cmd: ``str``
    :param cwd: The execution directory
    :type cwd: ``str``
    :param quiet: True if quiet
    :type quiet: ``bool``
    :return: True on success
    :rtype: ``bool``
    """
    expnaded_cmd = os.path.expanduser(cmd)
    banner(expnaded_cmd, quiet)
    stdout_type = subprocess.PIPE if quiet else None
    process = subprocess.Popen(expnaded_cmd.split(),
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
        return False

    return True
