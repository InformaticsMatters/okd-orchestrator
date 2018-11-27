# -----------------------------------------------------------------------------
# Templating
# -----------------------------------------------------------------------------

# -------------------------
# The AWS Bastion Inventory
# -------------------------

data "template_file" "inventory" {
  template = "${file("${var.openshift_dir}/inventories/${var.deployment}/bastion.inventory.tpl")}"

  vars {
    bastion = "${aws_instance.bastion.0.public_ip}"
  }
}

resource "local_file" "inventory" {
  content = "${data.template_file.inventory.rendered}"
  filename = "${var.openshift_dir}/inventories/${var.deployment}/inventory"
}

# -------------------------------------
# The AWS Bastion Environment Variables
# -------------------------------------

data "template_file" "sh" {
  template = "${file("${var.openshift_dir}/inventories/${var.deployment}/bastion.sh.tpl")}"

  vars {
    aws_access_key = "${var.aws_access_key}"
    aws_secret_key = "${var.aws_secret_key}"
    vpc_id = "${aws_vpc.bastion.id}"
    subnet_id = "${aws_subnet.public-subnet.id}"
    okd_admin_password = "${var.okd_admin_password}"
  }
}

resource "local_file" "bastion-sh" {
  content = "${data.template_file.sh.rendered}"
  filename = "${var.openshift_dir}/inventories/${var.deployment}/bastion.sh"
}
