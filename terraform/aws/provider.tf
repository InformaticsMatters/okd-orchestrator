# -----------------------------------------------------------------------------
# Various Terraform provider definitions
# -----------------------------------------------------------------------------

terraform {
  required_version = "0.11.14"
}

provider "aws" {
  region = "${var.aws_region}"
  version = "2.19.0"
}

provider "local" {
  version = "1.3.0"
}

provider "template" {
  version = "2.1.2"
}
