#!/usr/bin/env python3
"""
Script to update testuser permissions to AUS region products
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

def update_testuser_permissions():
    print("=" * 60)
    print("Updating Test User Permissions for AUS Region")
    print("=" * 60)
    
    # Get testuser
    try:
        testuser = User.objects.get(username='testuser')
    except User.DoesNotExist:
        print("❌ Test user not found! Please run create_test_users.py first.")
        return
    
    # Get AUS region
    aus_region = Region.objects.get(country_code='AUS')
    
    # Get AUS products with reports
    aus_products = Product.objects.filter(regions=aus_region)
    
    # Select products with the most reports
    products_with_reports = []
    for product in aus_products:
        report_count = Report.objects.filter(product=product, region=aus_region).count()
        if report_count > 0:
            products_with_reports.append((product, report_count))
    
    # Sort by report count and select top 3
    products_with_reports.sort(key=lambda x: x[1], reverse=True)
    selected_products = [p[0] for p in products_with_reports[:3]]
    
    if not selected_products:
        print("⚠️  No products with reports found in AUS region!")
        return
    
    # Clear existing permissions
    print(f"\n🔄 Clearing existing permissions for testuser...")
    testuser.user_permissions.clear()
    
    # Get the User content type
    user_content_type = ContentType.objects.get(app_label='users', model='user')
    
    print(f"\n✅ Assigning {len(selected_products)} AUS products with reports:\n")
    
    for product in selected_products:
        # Create permission codename
        perm_codename = f"can_{product.name.lower().replace(' ', '_')}"
        
        # Get or create the permission
        permission, created = Permission.objects.get_or_create(
            codename=perm_codename,
            content_type=user_content_type,
            defaults={'name': f'Can View {product.name}'}
        )
        
        # Assign permission to user
        testuser.user_permissions.add(permission)
        
        # Count reports
        report_count = Report.objects.filter(product=product, region=aus_region).count()
        
        print(f"   ✓ {product.name}")
        print(f"     Permission: {perm_codename}")
        print(f"     Reports in AUS: {report_count}")
    
    print("\n" + "=" * 60)
    print("✅ Permissions updated successfully!")
    print("=" * 60)
    print("\nTest user can now access reports in AUS region.")
    print("Login with: testuser / Test@123\n")

if __name__ == "__main__":
    try:
        update_testuser_permissions()
    except Exception as e:
        print(f"\n❌ Error updating permissions: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
