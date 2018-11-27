# -----------------------------------------------------------------------------
# PUBLIC Subnet
# -----------------------------------------------------------------------------

resource "aws_subnet" "public-subnet" {
  vpc_id = "${aws_vpc.bastion.id}"

  cidr_block = "${var.public_subnet_cidr}"

  tags {
    Name = "${var.resource_tag}"
  }
}

resource "aws_route_table" "route" {
  vpc_id = "${aws_vpc.bastion.id}"

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.default.id}"
  }

  tags {
    Name = "${var.resource_tag}"
  }
}

resource "aws_route_table_association" "bastion" {
  subnet_id = "${aws_subnet.public-subnet.id}"
  route_table_id = "${aws_route_table.route.id}"
}
