import boto3
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Move misplaced static files from root of S3 bucket into the /static/ folder"

    def handle(self, *args, **options):
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        region = settings.AWS_S3_REGION_NAME

        s3 = boto3.resource(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=region,
        )
        bucket = s3.Bucket(bucket_name)

        moved_files = 0

        for obj in bucket.objects.all():
            key = obj.key

            # skip directories
            if key.endswith("/"):
                continue

            # already in static/ or media/ → skip
            if key.startswith("static/") or key.startswith("media/"):
                continue

            # move to static/
            new_key = f"static/{key}"
            print(f"Moving {key} → {new_key}")

            # copy to new location
            bucket.copy({"Bucket": bucket_name, "Key": key}, new_key)

            # delete old key
            s3.Object(bucket_name, key).delete()

            moved_files += 1

        self.stdout.write(self.style.SUCCESS(f"Moved {moved_files} files into /static/"))

