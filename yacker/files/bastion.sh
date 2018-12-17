# An okd-orchestrator Packer File
#
# Add (prefix) CentOS user's PATH with $HOME/bin
# Needs prefixing because of potential clash with pre-existing packer binary
export PATH=$HOME/bin:$HOME/bin/oc:$PATH
