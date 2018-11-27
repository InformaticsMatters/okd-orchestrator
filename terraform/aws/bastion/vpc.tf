# -----------------------------------------------------------------------------
# VPC definitions
# -----------------------------------------------------------------------------

resource "aws_vpc" "bastion" {
  cidr_block = "${var.vpc_cidr}"
  enable_dns_hostnames = true

  tags {
    Name = "${var.resource_tag}"
    "kubernetes.io/cluster/${var.cluster_id}" = "owned"
  }
}

resource "aws_internet_gateway" "default" {
  vpc_id = "${aws_vpc.bastion.id}"

  tags {
    Name = "${var.resource_tag}"
    "kubernetes.io/cluster/${var.cluster_id}" = "owned"
  }
}
