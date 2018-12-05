# -------------------
# Interactive Outputs
# -------------------

output "bastion_ip" {
  value = "${aws_instance.bastion.public_ip}"
}

output "openshift_master_ip" {
  value = "${aws_instance.master.0.public_ip}"
}

output "openshift_infra_ip" {
  value = "${aws_instance.infra.0.public_ip}"
}
