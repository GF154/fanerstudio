import os
from google.cloud import storage

def get_storage_client():
    return storage.Client()

def upload_to_gcs(local_path, remote_path, bucket_name, make_public=True):
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(remote_path)
    blob.upload_from_filename(local_path)
    print(f"✅ Uploaded {local_path} → gs://{bucket_name}/{remote_path}")

    # Si w vle fè fichye a piblik
    if make_public:
        blob.make_public()
        print(f"🌍 Lien piblik: {blob.public_url}")
        return blob.public_url
    return None

def download_from_gcs(remote_path, local_path, bucket_name):
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(remote_path)
    blob.download_to_filename(local_path)
    print(f"⬇️ Downloaded gs://{bucket_name}/{remote_path} → {local_path}")

