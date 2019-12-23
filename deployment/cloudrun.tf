resource "google_cloud_run_service" "card_generator" {
  name = var.name
  location = var.location

  metadata {
    namespace = "yugiohbot"
  }

  template {
    spec {
      containers {
        image = "${var.image}@${var.digest}"
        resources {
          limits = {
            cpu = "1000m"
            memory = "1024Mi"
          }
        }
      }
    }
  }
}
