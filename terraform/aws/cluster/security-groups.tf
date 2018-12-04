# -----------------------------------------------------------------------------
# OpenShift Master Nodes
# -----------------------------------------------------------------------------

resource "aws_security_group" "openshift" {
  name = "${var.resource_tag}-openshift"
  description = "The Master Security Group."

  # Open to the outside...
  ingress {
    from_port = 9000
    to_port = 9000
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 8443
    to_port = 8443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Open to receive anything from anyone (internally)...
  ingress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    self = true
  }

  vpc_id = "${module.vpc.vpc_id}"

  tags {
    Name = "${var.resource_tag}"
    "kubernetes.io/cluster/${var.cluster_id}" = "owned"
  }
}

# -----------------------------------------------------------------------------
# SSH security group
# -----------------------------------------------------------------------------

resource "aws_security_group" "ssh" {
  name = "${var.resource_tag}-ssh"
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

  vpc_id = "${module.vpc.vpc_id}"

  tags {
    Name = "${var.resource_tag}"
    "kubernetes.io/cluster/${var.cluster_id}" = "owned"
  }
}

# -----------------------------------------------------------------------------
# Outbound
# -----------------------------------------------------------------------------

resource "aws_security_group" "outbound-general" {
  name = "${var.resource_tag}-outbound"
  description = "Open-up the outbound connections."

  # Any outbound traffic...
  egress  {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  vpc_id = "${module.vpc.vpc_id}"

  tags {
    Name = "${var.resource_tag}"
    "kubernetes.io/cluster/${var.cluster_id}" = "owned"
  }
}
