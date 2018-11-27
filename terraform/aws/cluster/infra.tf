# -----------------------------------------------------------------------------
# Infra instance definitions
# -----------------------------------------------------------------------------

resource "aws_instance" "infra" {
  ami = "${var.node_ami}"
  instance_type = "${var.infra_image_type}"
  count = "${var.infra_count}"
  key_name = "${var.keypair_name}"
  vpc_security_group_ids = ["${aws_security_group.openshift.id}",
                            "${aws_security_group.ssh.id}",
                            "${aws_security_group.outbound-general.id}"]
  subnet_id = "${var.subnet_id}"
  source_dest_check = false

  associate_public_ip_address = true

  root_block_device {
    volume_size = 30
    volume_type = "gp2"
  }

  tags {
    Name = "${var.resource_tag}-infra"
    "kubernetes.io/cluster/${var.cluster_id}" = "owned"
  }
}
