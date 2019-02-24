# -----------------------------------------------------------------------------
# Various Terraform provider definitions
# -----------------------------------------------------------------------------

terraform {
  required_version = "0.11.11"
}

provider "google" {
  project = "${var.gce_project}"
  credentials = "${file("../../gce-credentials.json")}"
  region = "${var.gce_region}"
  zone = "${var.gce_region}-a"
  version = "1.20.0"
}

provider "local" {
  version = "1.1.0"
}

provider "template" {
  version = "1.0.0"
}
