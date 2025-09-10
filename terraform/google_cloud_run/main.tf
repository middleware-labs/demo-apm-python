terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.3.0"
}

provider "google" {
  project = "project-id"
  region  = "region1"
}

resource "google_cloud_run_service" "default" {
    name     = "demo-cloud-run-python-apm"
    location = "asia-south1"

    template {
        spec {
            containers {
                image = "advait11/python-django-gunicorn-apm"
                ports {
                    container_port = 8000
                }
                env {
                    name  = "MW_API_KEY"
                    value = "whkvkobudfitutobptgonaezuxpjjypnejbb"
                }
                env {
                    name = "MW_TARGET"
                    value = "https://myapp.middleware.io:443"
                }
                env {
                    name = "MW_SERVICE_NAME"
                    value = "MyTerraformPythonApp"
                }
            }
        }
    }

    traffic {
        percent         = 100
        latest_revision = true
    }
}

# Optional: allow unauthenticated requests
resource "google_cloud_run_service_iam_member" "noauth" {
  location = google_cloud_run_service.default.location
  project  = google_cloud_run_service.default.project
  service  = google_cloud_run_service.default.name

  role   = "roles/run.invoker"
  member = "allUsers"
}
