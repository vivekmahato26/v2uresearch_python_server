import boto3
from botocore.exceptions import ClientError
import os
import sys

# Credentials from settings.py
AWS_ACCESS_KEY_ID = 'AKIAVKOA3APQ6OOGB46N'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'v2uresearch'
AWS_S3_REGION_NAME = 'ap-southeast-2'

def verify_aws():
    print(f"Testing access for bucket: {AWS_STORAGE_BUCKET_NAME}")
    
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_S3_REGION_NAME
    )
    
    s3 = session.client('s3')
    
    # 1. Test Credentials (List Buckets)
    print("\n1. Testing Credentials (List Buckets)...")
    try:
        response = s3.list_buckets()
        print("Success! Credentials are valid.")
        buckets = [b['Name'] for b in response['Buckets']]
        if AWS_STORAGE_BUCKET_NAME not in buckets:
            print(f"Warning: Target bucket '{AWS_STORAGE_BUCKET_NAME}' not found in account buckets.")
        else:
            print(f"Target bucket '{AWS_STORAGE_BUCKET_NAME}' found.")
    except ClientError as e:
        print(f"Error listing buckets: {e}")
        return

    # 2. Check Bucket Location
    print(f"\n2. Verifying Bucket Region ({AWS_S3_REGION_NAME})...")
    try:
        response = s3.get_bucket_location(Bucket=AWS_STORAGE_BUCKET_NAME)
        location = response['LocationConstraint']
        print(f"Bucket Location: {location}")
        if location != AWS_S3_REGION_NAME:
            print(f"MISMATCH: Configured region is {AWS_S3_REGION_NAME}, but bucket is in {location}")
    except ClientError as e:
        print(f"Error checking location: {e}")

    # 3. Check Public Access Block
    print("\n3. Checking Public Access Block Configuration...")
    try:
        response = s3.get_public_access_block(Bucket=AWS_STORAGE_BUCKET_NAME)
        print("Public Access Block Configuration:")
        print(response.get('PublicAccessBlockConfiguration'))
    except ClientError as e:
        print(f"Error checking public access block (might verify permissions): {e}")

    # 4. Try to Put Object with public-read ACL
    print("\n4. Testing Upload with 'public-read' ACL...")
    try:
        s3.put_object(
            Bucket=AWS_STORAGE_BUCKET_NAME,
            Key='test_permission_check.txt',
            Body=b'test',
            ACL='public-read'
        )
        print("Success: Uploaded object with 'public-read' ACL. Bucket allows public objects.")
    except ClientError as e:
        print(f"Error uploading public object: {e}")
        if e.response['Error']['Code'] == 'AccessDenied':
            print(">> likely 'Block Public Access' is enabled on the bucket.")

    # 5. List Recent Objects and Check ACL
    print("\n5. Checking ACL of recent objects...")
    try:
        response = s3.list_objects_v2(Bucket=AWS_STORAGE_BUCKET_NAME, MaxKeys=5)
        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                print(f"Checking ACL for: {key}")
                try:
                    acl_resp = s3.get_object_acl(Bucket=AWS_STORAGE_BUCKET_NAME, Key=key)
                    grants = acl_resp['Grants']
                    is_public = any(
                        g['Grantee'].get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers' 
                        for g in grants
                    )
                    print(f"  - Public Read: {is_public}")
                except ClientError as e:
                    print(f"  - Error getting ACL: {e}")
        else:
            print("No objects found in bucket.")
    except ClientError as e:
        print(f"Error listing objects: {e}")

if __name__ == "__main__":
    verify_aws()
