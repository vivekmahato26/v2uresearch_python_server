import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'V2UResearchApp.settings')
django.setup()

from users.models import Region
from marketing.models import Product
from reports.models import Report

def debug():
    print("Checking Regions...")
    regions = Region.objects.all()
    for r in regions:
        print(f"Region: {r.id} - {r.country_code}")

    # Simulate EssentialsMixin logic (simplified)
    try:
        region = Region.objects.get(country_code='CAN') # Assuming CAN exists from default fallback
    except:
        try:
            region = Region.objects.first()
            if not region:
                print("No regions found!")
                return
        except:
             print("Error finding region")
             return

    print(f"Selected Region: {region}")

    print("Checking Product Filter...")
    try:
        products = Product.objects.filter(is_active=True, regions=region)
        print(f"Products found: {products.count()}")
    except Exception as e:
        print(f"Product Filter Error: {e}")

    # Check suspicious filter with empty ID
    print("Checking suspicious filter with empty id...")
    try:
        products = Product.objects.filter(is_active=True, regions='')
        print(f"Products found: {products.count()}")
    except Exception as e:
        print(f"Error confirmed: {e}")

    # Check Report object
    print("Checking Report...")
    reports = Report.objects.all()
    if reports.exists():
        r = reports.first()
        print(f"Report: {r.slug}")
        try:
            p = r.product.all()
            print(f"Report products: {p.count()}")
        except Exception as e:
            print(f"Report Product Error: {e}")

if __name__ == '__main__':
    debug()
