import boto3
from botocore.exceptions import NoCredentialsError
from config import settings

class StorageManager:
    def __init__(self):
        protocol = "https" if settings.MINIO_SECURE else "http"
        self.s3 = boto3.client(
            's3',
            endpoint_url=f"{protocol}://{settings.MINIO_ENDPOINT}",
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY,
            region_name='us-east-1'  # MinIO requires a region, but it's ignored
        )
        self.bucket_name = settings.MINIO_BUCKET_NAME

    def upload_file(self, file_obj, object_name):
        try:
            self.s3.upload_fileobj(file_obj, self.bucket_name, object_name)
            return True
        except NoCredentialsError:
            print("Credentials not available")
            return False
        except Exception as e:
            print(f"Error uploading file: {e}")
            return False

    def download_file(self, object_name, file_path):
        try:
            self.s3.download_file(self.bucket_name, object_name, file_path)
            return True
        except Exception as e:
            print(f"Error downloading file: {e}")
            return False

    def delete_file(self, object_name):
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=object_name)
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False

storage_manager = StorageManager()
