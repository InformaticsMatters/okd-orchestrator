#!/usr/bin/env python

"""A Python 2/3 jinja2-based template renderer.

This utility uses YAML-based _deployment_ configurations to size
the cluster prior to its formation. The intention is to have
a deployment configuration for each customer/cluster that
is used to render a number of key orchestration files.

Given a deployment (the name of a file in the deployments directory
excluding the .yaml extension) this module loads the file
and uses the content to render all the .j2 files it can find
(that do not reside in the openshift-ansible) directory.

This module automatically adds a variable that represents the name
of the deployment, that can be exploited in the .j2 files. The
built-in variable is give the name ``deployment``.
"""

from __future__ import print_function

import argparse
import os
import sys
import yaml
import jinja2

_TEMPLATE_EXTENSION = '.j2'
_PROJECT_ROOT = '.'
_DEPLOYMENT_DIR = 'deployments'
_EXCLUDE = ['openshift-ansible']


def error(message):
    """Stop with an error message.
    """
    print('ERROR: {}'.format(message))
    sys.exit(1)


def translate(template_file, context):
    """Renders the supplied template file, returning the
    rendered content to the caller.

    :param template_file: The jinja2 file to render
    :param context: The dictionary to use for the rendering
    :return: The rendered content
    """
    path, filename = os.path.split(template_file)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader([path, os.path.dirname(path)]),
        keep_trailing_newline=True
    ).get_template(filename).render(context)


def load_deployment_configuration(deployment):
    """Loads the deployment configuration.

    :param deployment: The deployment. The file basename, i.e. 'snic'.
                       Expected to be present in the _DEPLOYMENT_DIR.
    :type deployment: ``str``
    :return: The deployment configuration (a dictionary)
    """
    deployment_file = os.path.join(_DEPLOYMENT_DIR, deployment + '.yaml')
    if not os.path.exists(deployment_file):
        error('Deployment is not known ({})'.format(deployment_file))

    deployment_configuration = {}
    with open(deployment_file, 'r') as stream:
        try:
            deployment_configuration = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    # Add the deployment name to the dictionary,
    # so .j2 files can have access to the deployment name.
    deployment_configuration['deployment'] = deployment
    return deployment_configuration


def find_template_files(deployment_config):
    """Locate all the potential Jinja2 template files.
    All those that end with the right extension but only process the named
    terraform directory. Other directories may contain variables not present
    in our template file.

    :param deployment_config: The deployment configuration
    :type deployment_config: ``dict``
    :return: A list of template files.
    """
    terraform_dir = deployment_config['terraform']['dir']
    files = []
    for root, _, file_names in os.walk(_PROJECT_ROOT):
        exclude = False
        # In excluded list?
        for directory in _EXCLUDE:
            if root.find(directory) >= 0:
                exclude = True
                break
        # Not our terraform directory?
        if (root.startswith('./terraform/') and
                not root.startswith('./terraform/{}'.format(terraform_dir))):
            exclude = True
        # If the directory's not been excluded then
        # add it to our jinja2 search list....
        if not exclude:
            for filename in file_names:
                if filename.endswith(_TEMPLATE_EXTENSION):
                    files.append(os.path.join(root, filename))

    return files


def translate_template_files(file_set, config):
    """Translates all the files using the deployment configuration.

    :param file_set: The list of translation (jin ja2) files
    :param config: The deployment configuration (a dictionary)
    """
    print('Rendering...')

    num_translated = 0
    for template_file in file_set:
        print('+ {}'.format(template_file))
        output_filename = template_file[:-(len(_TEMPLATE_EXTENSION))]
        translation = translate(template_file, config)
        with open(output_filename, 'w') as output_file:
            output_file.write(translation)
        num_translated += 1

    print('Rendered ({}).'.format(num_translated))


if __name__ == '__main__':

    # Construct command-line parser.
    # We expect one file - the configuration file
    parser = argparse.ArgumentParser(
        description='The Orchestration Configuration Renderer.'
                    ' This tool applies the defined deployment configuration'
                    ' to dynamic portions of the orchestration (typically'
                    ' the Terraform and Ansible configuration files).')

    parser.add_argument('deployment',
                        help='The deployment configuration to apply')
    args = parser.parse_args()

    deployment_config = load_deployment_configuration(args.deployment)
    template_files = find_template_files(deployment_config)
    translate_template_files(template_files, deployment_config)
