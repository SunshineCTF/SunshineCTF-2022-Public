provider "google" {
  project = "sunshine-2022-challenges"
  region  = "us-central1"
}

################################################################
## Listy Leaderboard Buckets
################################################################

resource "google_storage_bucket" "listy-leaderboard-prod" {
  name          = "ssctf22-listy-leaderboard-prod"
  location      = "US"
  force_destroy = true
}

resource "google_storage_bucket_object" "listy-leaderboard-prod" {
  name   = "leaderboard.csv"
  bucket = google_storage_bucket.listy-leaderboard-prod.name
  source = "./leaderboards/leaderboard-prod.csv"
}


resource "google_storage_bucket" "listy-leaderboard-dev" {
  name          = "ssctf22-listy-leaderboard-dev"
  location      = "US"
  force_destroy = true
}

resource "google_storage_bucket_object" "listy-leaderboard-dev" {
  name   = "leaderboard.csv"
  bucket = google_storage_bucket.listy-leaderboard-dev.name
  source = "./leaderboards/leaderboard-dev.csv"
}


################################################################
## Listy Cloud Function
################################################################

data "archive_file" "function-source" {
  type        = "zip"
  source_dir  = "./function"
  output_path = "./function.zip"
}

resource "google_storage_bucket" "listy-function" {
  name          = "listy-function"
  location      = "US"
  force_destroy = true
}

# By having the MD5sum of the function source as part of the name, we can
# force a new version of the function to be deployed when the source changes.
resource "google_storage_bucket_object" "listy-function" {
  name   = "listy-prod-${data.archive_file.function-source.output_md5}.zip"
  bucket = google_storage_bucket.listy-function.name
  source = data.archive_file.function-source.output_path
}

# GCP Service Account with Permissions to read from the leaderboard buckets
resource "google_service_account" "listy-function-sa" {
  account_id   = "listy-function-sa"
  display_name = "Listy Function SA"
}

resource "google_storage_bucket_iam_member" "listy-function-sa-prod" {
  bucket = google_storage_bucket.listy-leaderboard-prod.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.listy-function-sa.email}"
}

resource "google_storage_bucket_iam_member" "listy-function-sa-dev" {
  bucket = google_storage_bucket.listy-leaderboard-dev.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.listy-function-sa.email}"
}

resource "google_cloudfunctions_function" "listy" {
  name                  = "listy"
  description           = "listy function"
  available_memory_mb   = 256
  runtime               = "python310"
  timeout               = 60
  source_archive_bucket = google_storage_bucket.listy-function.name
  trigger_http          = true
  entry_point           = "handler"
  service_account_email = google_service_account.listy-function-sa.email
  source_archive_object = google_storage_bucket_object.listy-function.name
}

resource "google_service_account" "listy" {
  account_id   = "listy-service-account"
  display_name = "Listy service account"
}

resource "google_cloudfunctions_function_iam_member" "listy" {
  project        = google_cloudfunctions_function.listy.project
  region         = google_cloudfunctions_function.listy.region
  cloud_function = google_cloudfunctions_function.listy.name
  role           = "roles/cloudfunctions.invoker"
  member         = "serviceAccount:${google_service_account.listy.email}"
}

################################################################
## Listy Frontend Cloud Run
################################################################

resource "google_service_account" "listy-developer" {
  account_id   = "listy-developer"
  display_name = "Listy development service account"
}

resource "google_cloudfunctions_function_iam_member" "listy-developer" {
  project        = google_cloudfunctions_function.listy.project
  region         = google_cloudfunctions_function.listy.region
  cloud_function = google_cloudfunctions_function.listy.name
  role           = "roles/cloudfunctions.invoker"
  member         = "serviceAccount:${google_service_account.listy-developer.email}"
}

resource "google_service_account_key" "listy-developer" {
  service_account_id = google_service_account.listy-developer.name
}

resource "local_file" "key" {
  filename = "/tmp/listy-devkey.json"
  content  = base64decode(google_service_account_key.listy-developer.private_key)
}

resource "google_service_account" "listy-web" {
  account_id   = "listy-web"
  display_name = "Listy frontend service account"
}

resource "google_cloudfunctions_function_iam_member" "listy-web" {
  project        = google_cloudfunctions_function.listy.project
  region         = google_cloudfunctions_function.listy.region
  cloud_function = google_cloudfunctions_function.listy.name
  role           = "roles/cloudfunctions.invoker"
  member         = "serviceAccount:${google_service_account.listy-web.email}"
}

resource "google_cloud_run_service" "listy-web" {
  name     = "listy-web"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/sunshine-2022-challenges/listy-web"
      }
      service_account_name = google_service_account.listy-web.email
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }

}
