#!/usr/bin/env python3
"""
Script to create test users for V2U Research platform
Creates:
1. Admin user with superuser privileges
2. Regular user with access to 2-3 random products
"""

import os
import sys
import django
import random

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'V2UResearchApp.settings')
django.setup()

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from marketing.models import Product

def create_users():
    print("=" * 60)
    print("Creating Test Users for V2U Research")
    print("=" * 60)
    
    # 1. Create Admin User
    admin_username = "admin_test"
    admin_email = "admin@v2uresearch.com"
    admin_password = "Admin@123"
    
    if User.objects.filter(username=admin_username).exists():
        print(f"\n⚠️  Admin user '{admin_username}' already exists. Deleting and recreating...")
        User.objects.filter(username=admin_username).delete()
    
    admin_user = User.objects.create_superuser(
        username=admin_username,
        email=admin_email,
        password=admin_password,
        first_name="Admin",
        last_name="User"
    )
    print(f"\n✅ Created Admin User:")
    print(f"   Username: {admin_username}")
    print(f"   Email: {admin_email}")
    print(f"   Password: {admin_password}")
    print(f"   Superuser: Yes")
    
    # 2. Create Regular User with limited access
    regular_username = "testuser"
    regular_email = "testuser@v2uresearch.com"
    regular_password = "Test@123"
    
    if User.objects.filter(username=regular_username).exists():
        print(f"\n⚠️  Regular user '{regular_username}' already exists. Deleting and recreating...")
        User.objects.filter(username=regular_username).delete()
    
    regular_user = User.objects.create_user(
        username=regular_username,
        email=regular_email,
        password=regular_password,
        first_name="Test",
        last_name="User"
    )
    
    # Get all available products
    all_products = list(Product.objects.all())
    
    if not all_products:
        print("\n⚠️  No products found in database. Creating user without permissions.")
    else:
        # Select 2-3 random products
        num_products = min(random.randint(2, 3), len(all_products))
        selected_products = random.sample(all_products, num_products)
        
        print(f"\n✅ Created Regular User:")
        print(f"   Username: {regular_username}")
        print(f"   Email: {regular_email}")
        print(f"   Password: {regular_password}")
        print(f"   Superuser: No")
        print(f"\n📋 Assigned Permissions for {num_products} products:")
        
        # Get the User content type (for permissions)
        user_content_type = ContentType.objects.get(app_label='users', model='user')
        
        for product in selected_products:
            # Create permission codename matching the Product model's format
            perm_codename = f"can_{product.name.lower().replace(' ', '_')}"
            
            # Get or create the permission
            permission, created = Permission.objects.get_or_create(
                codename=perm_codename,
                content_type=user_content_type,
                defaults={'name': f'Can View {product.name}'}
            )
            
            # Assign permission to user
            regular_user.user_permissions.add(permission)
            
            status = "✓" if created else "↻"
            print(f"   {status} {product.name} (permission: {perm_codename})")
    
    print("\n" + "=" * 60)
    print("✅ User creation completed!")
    print("=" * 60)
    print("\nYou can now log in with either:")
    print(f"1. Admin: {admin_username} / {admin_password}")
    print(f"2. Regular: {regular_username} / {regular_password}")
    print("\n")

if __name__ == "__main__":
    try:
        create_users()
    except Exception as e:
        print(f"\n❌ Error creating users: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
