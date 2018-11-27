# -----------------------------------------------------------------------------
# SSH security group
# -----------------------------------------------------------------------------

resource "aws_security_group" "ssh" {
  name = "ssh"
  description = "Allow SSH connections from anywhere."

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress  {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  vpc_id = "${aws_vpc.bastion.id}"

  tags {
    Name = "${var.resource_tag}"
    "kubernetes.io/cluster/${var.cluster_id}" = "owned"
  }
}

# -----------------------------------------------------------------------------
# Outbound
# -----------------------------------------------------------------------------

resource "aws_security_group" "outbound-general" {
  name = "Outbound"
  description = "Open-up the outbound connections."

  # Any outbound traffic...
  egress  {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  vpc_id = "${aws_vpc.bastion.id}"

  tags {
    Name = "${var.resource_tag}"
    "kubernetes.io/cluster/${var.cluster_id}" = "owned"
  }
}
