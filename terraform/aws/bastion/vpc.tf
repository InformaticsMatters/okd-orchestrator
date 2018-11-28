# -----------------------------------------------------------------------------
# VPC definitions
# -----------------------------------------------------------------------------

# Using the Module Registry's VPC module we can conveniently
# create a VPC with a NAT and public and private subnets.
#
# See https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/1.46.0

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "1.46.0"

  default_vpc_enable_dns_hostnames = true
  enable_dns_hostnames = true
  single_nat_gateway = true

  cidr = "10.0.0.0/16"

  azs = ["${var.aws_zone}"]
  private_subnets = ["10.0.1.0/24"]
  public_subnets = ["10.0.101.0/24"]

  tags {
    Name = "${var.resource_tag}"
    "kubernetes.io/cluster/${var.cluster_id}" = "owned"
  }
}
