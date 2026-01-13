# Admin Guide: Granting Report Access to Users

This guide explains how to grant users access to specific reports through the V2U Research platform.

## Table of Contents

1. [Understanding the Permission System](#understanding-the-permission-system)
2. [Method 1: Django Admin Panel (Recommended)](#method-1-django-admin-panel-recommended)
3. [Method 2: Programmatic Access (Advanced)](#method-2-programmatic-access-advanced)
4. [Troubleshooting](#troubleshooting)

---

## Understanding the Permission System

### How Report Access Works

Reports are controlled by **Product-based permissions**. Each product has an associated permission that grants access to all reports tagged with that product.

**Permission Format:** `can_{product_name}`

- Example: `can_au_daily_report` grants access to all "AU Daily Report" reports

### Permission Structure

```
User → Permission → Product → Reports
```

When a user has permission for a product, they can:

- ✅ View all reports associated with that product
- ✅ Download PDFs (if available)
- ✅ Access full report content

---

## Method 1: Django Admin Panel (Recommended)

### Step 1: Access the Admin Panel

1. Navigate to: `http://your-domain.com/admin`
2. Log in with superuser credentials:
   - Username: `admin_test`
   - Password: `Admin@123`

### Step 2: Navigate to Users

1. Click on **"Users"** in the left sidebar (under Authentication and Authorization)
2. Find and click on the user you want to grant access to

### Step 3: Assign Permissions

1. Scroll down to the **"User permissions"** section
2. In the **"Available user permissions"** box, find permissions that start with `can_`
3. Look for product-specific permissions like:

   - `users | user | Can View AU Daily Report`
   - `users | user | Can View AU Mining Report`
   - `users | user | Can View US Equity (AU)`

4. **Select the permissions** you want to grant:

   - Hold `Ctrl` (Windows/Linux) or `Cmd` (Mac) to select multiple
   - Click the **right arrow (→)** to move them to "Chosen user permissions"

5. Click **"Save"** at the bottom of the page

### Step 4: Verify Access

1. Log out of admin
2. Log in as the user you just granted permissions to
3. Navigate to the Reports page
4. Verify that reports from the assigned products show **"View Report"** instead of **"Subscribe to Access"**

---

## Method 2: Programmatic Access (Advanced)

### Using Django Shell

```bash
cd /home/cs/Desktop/v2uresearch/v2uresearch_python_server
source venv/bin/activate
python3 manage.py shell
```

### Grant Access to a User

```python
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

# Get the user
user = User.objects.get(username='username_here')

# Get the content type for permissions
user_ct = ContentType.objects.get(app_label='users', model='user')

# Grant access to specific products
product_permissions = [
    'can_au_daily_report',
    'can_au_mining_report',
    'can_us_equity_(au)'
]

for perm_codename in product_permissions:
    permission = Permission.objects.get(
        codename=perm_codename,
        content_type=user_ct
    )
    user.user_permissions.add(permission)
    print(f'✓ Granted: {permission.name}')

print(f'\nUser {user.username} now has access to {len(product_permissions)} products')
```

### Remove Access from a User

```python
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

# Get the user
user = User.objects.get(username='username_here')

# Get the content type
user_ct = ContentType.objects.get(app_label='users', model='user')

# Remove specific permission
permission = Permission.objects.get(
    codename='can_au_daily_report',
    content_type=user_ct
)
user.user_permissions.remove(permission)
print(f'✓ Removed: {permission.name}')

# Or remove all permissions
user.user_permissions.clear()
print('✓ Removed all permissions')
```

### List User's Current Permissions

```python
from django.contrib.auth.models import User

user = User.objects.get(username='username_here')
perms = user.user_permissions.filter(
    content_type__app_label='users',
    content_type__model='user'
)

print(f'\n{user.username} has access to:')
for perm in perms:
    print(f'  - {perm.name} ({perm.codename})')
```

---

## Available Products and Permissions

### Common AUS Region Products

| Product Name              | Permission Codename             | Typical Report Count |
| ------------------------- | ------------------------------- | -------------------- |
| AU Daily Report           | `can_au_daily_report`           | 152                  |
| AU Mining Report          | `can_au_mining_report`          | 35                   |
| US Equity (AU)            | `can_us_equity_(au)`            | 41                   |
| AU Swing Trade Report     | `can_au_swing_trade_report`     | 33                   |
| AU Value Stocks Report    | `can_au_value_stocks_report`    | 34                   |
| AU Dividend Income Report | `can_au_dividend_income_report` | 21                   |

---

## Troubleshooting

### User Still Sees "Subscribe to Access"

**Check:**

1. ✅ User has the correct permission assigned
2. ✅ Permission content type is `users.user` (not `auth.user`)
3. ✅ User is logged in
4. ✅ User has refreshed the page after permission grant
5. ✅ Report is tagged with the product the user has permission for

**Verify Permission:**

```python
from django.contrib.auth.models import User

user = User.objects.get(username='username')
has_perm = user.has_perm('users.can_au_daily_report')
print(f'Has permission: {has_perm}')
```

---

## Quick Reference

### Grant Access (Admin Panel)

1. Admin → Users → Select User
2. Scroll to "User permissions"
3. Find `can_` permissions
4. Move to "Chosen user permissions"
5. Save

### Grant Access (Command Line)

```bash
python3 manage.py shell
>>> from django.contrib.auth.models import User, Permission
>>> from django.contrib.contenttypes.models import ContentType
>>> user = User.objects.get(username='username')
>>> ct = ContentType.objects.get(app_label='users', model='user')
>>> perm = Permission.objects.get(codename='can_au_daily_report', content_type=ct)
>>> user.user_permissions.add(perm)
```
