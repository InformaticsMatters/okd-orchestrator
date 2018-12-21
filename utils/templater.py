#!/usr/bin/env python

"""template.py - template rendering.

This module basically replicates the Terraform rendering actions
when orchestrating pre-existing clusters. It is used to replace the
node definitions in the OKD Ansible inventory file (normally found
in 'okd/inventories/?/'.
"""

import codecs
from . import io
import os
from string import Template


def render(deployment, template_ext='.tpl'):
    """Renders the given YAML file using the deployment. This essentially
    replicates the Terraform templating actions.

    :param deployment: The deployment object
    :type deployment: ``Munch``
    :param template_ext: The template file suffix
    :type template_ext: ``str``
    :returns: True on success
    """

    template_file_name = os.path.join('okd', 'inventories',
                                      deployment.okd.inventory_dir,
                                      'inventory.yaml.tpl')

    # The template substitution map will basically consist of
    # a few items from the deployment (e.g. public_hostname)
    # and the 'my-machines' section...
    template_map = {'public_hostname': deployment.cluster.public_hostname,
                    'default_subdomain': deployment.cluster.default_subdomain}
    template_map.update(deployment.my_machines)

    # Read and render the input file...
    with codecs.open(template_file_name, 'r', 'utf8') as input_file:
        raw_content = input_file.read()
        template = Template(raw_content)
        try:
            rendered_content = template.substitute(template_map)
        except KeyError as key_e:
            # There's a ${key} in the file with not corresponding
            # key in the template_map. Report the error
            # stripping the (') that surrounds the key in the error...
            io.error('You need to set a value for "my_machines.{}"'
                     ' in your deployment'.format(str(key_e)[1:-1]))
            return False

    # Write to the output file...
    output_file_name = template_file_name[:-len(template_ext)]
    output_file = codecs.open(output_file_name, 'w', 'utf8')
    output_file.write(rendered_content)
    output_file.close()

    return True
