# -----------------------------------------------------------------------------
# The Bastion node definition
# -----------------------------------------------------------------------------

resource "aws_instance" "bastion" {
  ami = "${var.aws_bastion_ami}"
  instance_type = "${var.bastion_image_type}"
  key_name = "${var.keypair_name}"
  vpc_security_group_ids = ["${aws_security_group.ssh.id}",
                            "${aws_security_group.outbound-general.id}"]
  subnet_id = "${module.vpc.public_subnets[0]}"
  associate_public_ip_address = true
  source_dest_check = false

  root_block_device {
    volume_size = 10
    volume_type = "gp2"
  }

  tags {
    Name = "${var.resource_tag}-bastion"
  }
}