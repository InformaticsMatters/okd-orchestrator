# -----------------------------------------------------------------------------
# Allocate/Associate Elastic IPs in our cluster
# -----------------------------------------------------------------------------
# We allocate new Elastic IPs if fixed values have not been assigned.
# We associate pre-allocated Elastic IPs to their respective instances.

# Allocate new EIPs...
# --------------------

resource "aws_eip" "master" {
  # Do this if an EIP has not been provided
  count = "${var.master_fixed_ip_id == "" ? 1 : 0}"

  instance = "${aws_instance.master.0.id}"

  tags {
    Name = "${var.resource_tag}-master"
  }
}

resource "aws_eip" "infra" {
  # Do this if an EIP has not been provided
  count = "${var.infra_fixed_ip_id == "" ? 1 : 0}"

  instance = "${aws_instance.infra.0.id}"

  tags {
    Name = "${var.resource_tag}-infra"
  }
}

# Associate pre-existing EIPs...
# ------------------------------

resource "aws_eip_association" "master" {
  # Do this if an EIP has been provided
  count = "${var.master_fixed_ip_id != "" ? 1 : 0}"

  instance_id   = "${aws_instance.master.0.id}"
  allocation_id = "${var.master_fixed_ip_id}"
}

resource "aws_eip_association" "infra" {
  # Do this if an EIP has been provided
  count = "${var.infra_fixed_ip_id != "" ? 1 : 0}"

  instance_id   = "${aws_instance.infra.0.id}"
  allocation_id = "${var.infra_fixed_ip_id}"
}
