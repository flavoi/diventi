from storages.backends.s3boto3 import S3Boto3Storage


class DiventiMediaStorage(S3Boto3Storage):
    location = 'media'