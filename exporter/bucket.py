import os
import boto3
from botocore import exceptions
from google.cloud import storage
from exporter import config


class Bucket:
    def get_all_objects(self):
        raise NotImplementedError

    def download_file(self, name, output_dir):
        raise NotImplementedError

    @staticmethod
    def get_output_dir(output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        return output_dir

    @staticmethod
    def get_file_name(obj):
        raise NotImplementedError


class UploadFailed(Exception): ...


class BucketAws(Bucket):
    def __init__(self, name):
        self.name = name
        self.resource = boto3.resource("s3")
        self.bucket = self.resource.Bucket(self.name)

    def get_all_objects(self):
        return self.bucket.objects.all()

    def download_file(self, file_name):
        full_dir = self.get_output_dir(config.RAW_DATA_DIR)
        self.resource.Object(self.name, file_name).download_file(
            os.path.join(full_dir, file_name)
        )

    def upload_file(self, file_name, object_name=None):
        if object_name is None:
            object_name = file_name
        try:
            response = self.resource.meta.client.upload_file(file_name, self.name, object_name)
        except exceptions.ClientError as e:
            raise UploadFailed

    @staticmethod
    def get_file_name(obj):
        return obj.key


class BucketGcp(Bucket):
    def __init__(self, name):
        self.name = name
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.get_bucket(name)

    def get_all_objects(self):
        return self.bucket.list_blobs()

    def download_file(self, file_name):
        full_dir = self.get_output_dir(config.RAW_DATA_DIR)
        bucket = self.storage_client.get_bucket(self.name)
        blob = bucket.blob(file_name)
        blob.download_to_filename(os.path.join(full_dir, blob.name.split("/")[-1]))

    @staticmethod
    def get_file_name(obj):
        return obj.name
