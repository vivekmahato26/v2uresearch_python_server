from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"

class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = True  # Bypass existence check to avoid 403 (HeadObject)
    default_acl = None  # Explicitly disable ACLs for "Block Public Access" buckets

