resource "google_cloud_run_service" "card_generator" {
  name      = var.name
  location  = var.location
  provider  = "google-beta"

  spec {
    containers {
      image = var.image
    }
  }
}

locals {
  cloud_run_status = {
    for cond in google_cloud_run_service.card_generator.status[0].conditions :
    cond.type => cond.status
  }
}

output "isReady" {
  value = local.cloud_run_status["Ready"] == "True"
}