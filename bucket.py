import boto3
import boto3.session
from A import settings


class Bucket:

    def __init__(self):
        session = boto3.session.Session()
        self.conn = session.client(
            "s3",
            endpoint_url = settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
        )        

    def get_objects(self):
        result = self.conn.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        return result
    
    def delte_object(self, key):
        self.conn.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
        return True
    

    def download_object(self, key):
        with open(settings.AWS_LOCAL_STOARGE + key, "wb") as file:
            self.conn.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, key, file)


    def delete_all_objects(self):
        objects = self.conn.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        if 'Contents' in objects:
            for obj in objects['Contents']:
                self.conn.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=obj['Key'])
        return True

bucket = Bucket()

