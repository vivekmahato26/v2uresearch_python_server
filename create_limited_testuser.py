#!/usr/bin/env python3
"""
Script to create a test user with limited access to only 2-3 specific products
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'V2UResearchApp.settings')
django.setup()

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from marketing.models import Product
from users.models import Region
from reports.models import Report

def create_limited_testuser():
    print("=" * 60)
    print("Creating Test User with Limited Product Access")
    print("=" * 60)
    
    # Get or create testuser
    username = "testuser"
    password = "Test@123"
    
    try:
        testuser = User.objects.get(username=username)
        print(f"\n🔄 User '{username}' exists, updating permissions...")
    except User.DoesNotExist:
        testuser = User.objects.create_user(
            username=username,
            email="testuser@v2uresearch.com",
            password=password,
            first_name="Test",
            last_name="User"
        )
        print(f"\n✅ Created user '{username}'")
    
    # Clear existing permissions
    testuser.user_permissions.clear()
    
    # Get AUS region
    aus_region = Region.objects.get(country_code='AUS')
    
    # Select specific products with good report counts
    selected_product_names = [
        'AU Daily Report',      # 152 reports
        'AU Mining Report',     # 35 reports
        'US Equity (AU)'        # 41 reports
    ]
    
    # Get the User content type
    user_content_type = ContentType.objects.get(app_label='users', model='user')
    
    print(f"\n✅ Granting access to {len(selected_product_names)} products:\n")
    
    total_reports = 0
    for prod_name in selected_product_names:
        try:
            product = Product.objects.get(name=prod_name)
            
            # Create permission codename
            perm_codename = f"can_{prod_name.lower().replace(' ', '_')}"
            
            # Get or create the permission
            permission, created = Permission.objects.get_or_create(
                codename=perm_codename,
                content_type=user_content_type,
                defaults={'name': f'Can View {prod_name}'}
            )
            
            # Assign permission to user
            testuser.user_permissions.add(permission)
            
            # Count reports
            report_count = Report.objects.filter(product=product, region=aus_region).count()
            total_reports += report_count
            
            print(f"   ✓ {prod_name}")
            print(f"     Permission: {perm_codename}")
            print(f"     Reports in AUS: {report_count}")
            
        except Product.DoesNotExist:
            print(f"   ⚠️  Product '{prod_name}' not found")
    
    print("\n" + "=" * 60)
    print(f"✅ Limited access configured!")
    print("=" * 60)
    print(f"\nUser: {username}")
    print(f"Password: {password}")
    print(f"Products: {len(selected_product_names)}")
    print(f"Total accessible reports: {total_reports}")
    print("\nLogin and verify you see ONLY reports from these 3 products.\n")

if __name__ == "__main__":
    try:
        create_limited_testuser()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
