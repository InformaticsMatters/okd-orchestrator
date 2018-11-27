# -----------------------------------------------------------------------------
# Associate Elastic IPs with our cluster
# -----------------------------------------------------------------------------

resource "aws_eip_association" "master" {
  instance_id = "${aws_instance.master.0.id}"
  allocation_id = "${var.master_aws_elastic_ip_allocation_id}"
}

resource "aws_eip_association" "infra" {
  instance_id = "${aws_instance.infra.0.id}"
  allocation_id = "${var.infra_aws_elastic_ip_allocation_id}"
}
