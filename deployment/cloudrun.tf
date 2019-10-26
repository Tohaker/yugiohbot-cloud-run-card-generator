resource "google_cloud_run_service" "card_generator" {
  name      = var.name
  location  = var.location
  provider  = "google-beta"

  metadata {
    namespace = "yugiohbot"
  }

  spec {
    containers {
      image = var.image
    }
  }

  resources {
    limits {
      memory = 1Gi
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