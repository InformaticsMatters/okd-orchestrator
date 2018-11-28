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
    vpc_id = "${module.vpc.vpc_id}"
    public_subnet_id = "${module.vpc.public_subnets[0]}"
    private_subnet_id = "${module.vpc.private_subnets[0]}"
  }
}

resource "local_file" "bastion-sh" {
  content = "${data.template_file.sh.rendered}"
  filename = "${var.openshift_dir}/inventories/${var.deployment}/bastion.sh"
}
