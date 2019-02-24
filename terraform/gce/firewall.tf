# -----------------------------------------------------------------------------
# OKD Firewalls
# -----------------------------------------------------------------------------

resource "google_compute_firewall" "okd-external" {
  name = "${var.name_tag}-okd-ext"
  description = "The External Firewall"
  network = "${google_compute_network.okd.name}"

  allow {
    protocol = "tcp"
    ports = ["80", "443", "8443", "9000"]
  }
}

resource "google_compute_firewall" "internal" {
  name = "${var.name_tag}-int"
  description = "The Internal Firewall"
  network = "${google_compute_network.okd.name}"

  allow {
    protocol = "icmp"
  }

  allow {
    protocol = "tcp"
    ports = ["0-65535"]
  }

  allow {
    protocol = "udp"
    ports = ["0-65535"]
  }

  # IP ranges for auto-0generated sub-netst
  # fit inside the 10.128.0.0/9 CIDR block
  source_ranges = ["10.128.0.0/9"]
}

# -----------------------------------------------------------------------------
# SSH security group
# -----------------------------------------------------------------------------

resource "google_compute_firewall" "ssh" {
  name = "${var.name_tag}-ssh"
  description = "Allow SSH connections"
  network = "${google_compute_network.okd.name}"

  allow {
    protocol = "tcp"
    ports = ["22"]
  }
}
