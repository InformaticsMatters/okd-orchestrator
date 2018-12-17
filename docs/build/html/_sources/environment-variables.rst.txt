#####################
Environment Variables
#####################

All the environment variables used by the OKD Orchestrator are documented
in the ``provider-env`` directory. Variables vary between providers so you
should inspect the *template* file for your provider. For example, the
variables used when orchestrating an AWS cluster can be found in
``provider-env/setenv-aws-template.sh``.
