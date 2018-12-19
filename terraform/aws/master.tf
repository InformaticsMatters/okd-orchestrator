# -----------------------------------------------------------------------------
# Master instance definitions
# -----------------------------------------------------------------------------

resource "aws_instance" "master" {
  ami = "${data.aws_ami.cluster.id}"
  instance_type = "${var.master_image_type}"
  count = "${var.master_count}"
  key_name = "${var.keypair_name}"
  availability_zone = "${element(data.aws_availability_zones.available.names, count.index)}"
  vpc_security_group_ids = ["${aws_security_group.openshift.id}",
                            "${aws_security_group.ssh.id}",
                            "${aws_security_group.outbound-general.id}"]
  subnet_id = "${module.vpc.public_subnets[0]}"
  source_dest_check = false

  associate_public_ip_address = true

  # OpenShift 3.6 recommends
  # at least 40GiB for mass-storage on the master.
  root_block_device {
    volume_size = 30
    volume_type = "gp2"
  }

  tags {
    Name = "${var.name_tag}-master-${format("%02d", count.index + 1)}"
    "kubernetes.io/cluster/${var.cluster_id}" = "owned"
  }
}
