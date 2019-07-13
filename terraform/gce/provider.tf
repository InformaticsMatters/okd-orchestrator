# -----------------------------------------------------------------------------
# Various Terraform provider definitions
# -----------------------------------------------------------------------------

terraform {
  required_version = "0.11.14"
}

provider "google" {
  project = "${var.gce_project}"
  credentials = "${file("../../gce-credentials.json")}"
  region = "${var.gce_region}"
  zone = "${var.gce_region}-a"
  version = "2.10.0"
}

provider "local" {
  version = "1.3.0"
}

provider "template" {
  version = "2.1.2"
}
