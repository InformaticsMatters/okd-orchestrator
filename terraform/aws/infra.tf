# -----------------------------------------------------------------------------
# Infra instance definitions
# -----------------------------------------------------------------------------

resource "aws_instance" "infra" {
  ami = "${data.aws_ami.cluster.id}"
  instance_type = "${var.infra_image_type}"
  count = "${var.infra_count}"
  key_name = "${var.keypair_name}"
  availability_zone = "${element(data.aws_availability_zones.available.names, count.index)}"
  vpc_security_group_ids = ["${aws_security_group.openshift.id}",
                            "${aws_security_group.ssh.id}",
                            "${aws_security_group.outbound-general.id}"]
  subnet_id = "${module.vpc.public_subnets[0]}"
  source_dest_check = false

  associate_public_ip_address = true

  root_block_device {
    volume_size = 30
    volume_type = "gp2"
  }

  tags {
    Name = "${var.name_tag}-infra-${format("%03d", count.index + 1)}"
    "kubernetes.io/cluster/${var.cluster_id}" = "owned"
  }
}
