from django import template
from reports.models import Report

register = template.Library()

@register.filter
def has_access(report, user):
    """
    Check if the user has access to view the report.
    Access granted if:
    1. Report is free.
    2. User has 'can_view_<product>' permission for any of the report's products.
    """
    if not user:
        return False
        
    if report.is_free:
        return True
        
    if not user.is_authenticated:
        return False

    # Check permissions based on products
    # Note: permissions are created with app_label 'users' in some contexts, or content_type mapping
    # The Product model creates permissions with codename 'can_{product_name}' (see marketing/models.py line 76)
    
    for prod in report.product.all():
        # Match the permission format created in Product.save(): can_{product_name}
        perm_codename = f'can_{prod.name.lower().replace(" ", "_")}'
        if user.has_perm(f'users.{perm_codename}'):
            return True
            
    return False
