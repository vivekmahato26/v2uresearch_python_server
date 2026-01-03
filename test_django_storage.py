import os
import django
import urllib.request
import urllib.error
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'V2UResearchApp.settings')
django.setup()

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def test_storage():
    filename = 'test_upload_public_acl.txt'
    content = b'This is a test for public-read ACL.'
    
    print(f"Attempting to upload {filename} using default storage...")
    
    # Clean up if exists
    if default_storage.exists(filename):
        default_storage.delete(filename)
        
    try:
        saved_name = default_storage.save(filename, ContentFile(content))
        print(f"File saved as: {saved_name}")
        
        file_url = default_storage.url(saved_name)
        print(f"File URL: {file_url}")
        
        # Verify Signed URL
        if '?' in file_url and ('Signature=' in file_url or 'X-Amz-Signature=' in file_url):
             print("SUCCESS: URL appears to be signed (contains query parameters).")
        else:
             print("WARNING: URL does not appear to be signed.")

        # Test Access
        print("Testing access to Signed URL...")
        try:
            with urllib.request.urlopen(file_url) as response:
                if response.status == 200:
                    print("SUCCESS: File is accessible via signed URL (HTTP 200).")
                    print(f"Content: {response.read().decode('utf-8')}")
                else:
                    print(f"FAILURE: Unexpected status code: {response.status}")
        except urllib.error.HTTPError as e:
            print(f"FAILURE: HTTP Error: {e.code} - {e.reason}")
            print("Access Denied. Signature might be invalid or permissions incorrect.")
        except Exception as e:
            print(f"FAILURE: Error accessing URL: {e}")
            
    except Exception as e:
        print(f"Error during upload/verification: {e}")

if __name__ == "__main__":
    test_storage()
