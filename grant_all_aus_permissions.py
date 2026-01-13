#!/usr/bin/env python3
"""
Script to grant testuser permissions for ALL products used by AUS reports
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

def grant_all_aus_permissions():
    print("=" * 60)
    print("Granting ALL AUS Report Product Permissions to Test User")
    print("=" * 60)
    
    # Get testuser
    try:
        testuser = User.objects.get(username='testuser')
    except User.DoesNotExist:
        print("❌ Test user not found!")
        return
    
    # Get AUS region
    aus_region = Region.objects.get(country_code='AUS')
    
    # Find ALL unique products used by AUS reports
    aus_reports = Report.objects.filter(region=aus_region)
    product_names = set()
    
    for report in aus_reports:
        for prod in report.product.all():
            product_names.add(prod.name)
    
    print(f"\n📋 Found {len(product_names)} unique products used by AUS reports")
    
    # Clear existing permissions
    print(f"\n🔄 Clearing existing permissions...")
    testuser.user_permissions.clear()
    
    # Get the User content type
    user_content_type = ContentType.objects.get(app_label='users', model='user')
    
    print(f"\n✅ Granting permissions for all products:\n")
    
    granted_count = 0
    for prod_name in sorted(product_names):
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
            
            # Count reports using this product in AUS
            report_count = Report.objects.filter(product=product, region=aus_region).count()
            
            print(f"   ✓ {prod_name} ({report_count} reports)")
            granted_count += 1
            
        except Product.DoesNotExist:
            print(f"   ⚠️  Product '{prod_name}' not found in database")
    
    print("\n" + "=" * 60)
    print(f"✅ Granted {granted_count} permissions successfully!")
    print("=" * 60)
    print("\nTest user now has access to ALL reports in AUS region.")
    print("Login with: testuser / Test@123\n")

if __name__ == "__main__":
    try:
        grant_all_aus_permissions()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
