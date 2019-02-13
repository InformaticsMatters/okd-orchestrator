# -----------------------------------------------------------------------------
# Various Terraform provider definitions
# -----------------------------------------------------------------------------

terraform {
  required_version = "0.11.11"
}

provider "aws" {
  region = "${var.aws_region}"
  version = "1.58.0"
}

provider "local" {
  version = "1.1.0"
}

provider "template" {
  version = "1.0.0"
}
