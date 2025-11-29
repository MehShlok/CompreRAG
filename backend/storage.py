import boto3
from botocore.exceptions import NoCredentialsError
from config import settings

class StorageManager:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            endpoint_url=f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            region_name='auto' # R2 doesn't use regions like AWS
        )
        self.bucket_name = settings.R2_BUCKET_NAME

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
