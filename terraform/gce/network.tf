# -----------------------------------------------------------------------------
# Network definitions
# -----------------------------------------------------------------------------

resource "google_compute_network" "okd" {
  name = "${var.name_tag}"
}
