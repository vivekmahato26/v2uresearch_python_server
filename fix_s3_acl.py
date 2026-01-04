
import os

file_path = r'V2UResearchApp/settings.py'

with open(file_path, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    # Comment out AWS_DEFAULT_ACL to fallback to bucket defaults (usually private/blocked)
    # This solves the 403 when the bucket blocks public ACLs.
    if 'AWS_DEFAULT_ACL' in line:
        new_lines.append(f"# {line}")
    elif 'AWS_QUERYSTRING_AUTH' in line:
        # Also comment strictly false querystring auth if we aren't sure bucket is public
        # Although user probably wants public reads. 
        # But let's start by removing the explicit ACL push.
        # If we remove ACL, files become private by default. 
        # Then we NEED signed URLs (AWS_QUERYSTRING_AUTH = True, default).
        # So we should comment this out too.
        new_lines.append(f"# {line}")
    elif 'AWS_S3_CUSTOM_DOMAIN' in line:
        # If we use signed URLs, custom domain might break signatures if not configured perfectly with cloudfront.
        # But let's assume standard S3 usage for now.
        new_lines.append(line)
    else:
        new_lines.append(line)

with open(file_path, 'w') as f:
    f.writelines(new_lines)

print("Updated settings.py: Commented out AWS_DEFAULT_ACL and AWS_QUERYSTRING_AUTH.")
