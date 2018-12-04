# -----------------------------------------------------------------------------
# Allocate Elastic IPs for our cluster
# -----------------------------------------------------------------------------

resource "aws_eip" "master" {
  instance = "${aws_instance.master.0.id}"

  tags {
    Name = "${var.resource_tag}-master"
  }
}

resource "aws_eip" "infra" {
  instance = "${aws_instance.infra.0.id}"

  tags {
    Name = "${var.resource_tag}-infra"
  }
}
