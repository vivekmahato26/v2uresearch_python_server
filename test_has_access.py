#!/usr/bin/env python3
"""
Test script to verify the has_access template filter is working correctly
"""

import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'V2UResearchApp.settings')
django.setup()

from django.contrib.auth.models import User
from reports.models import Report
from users.models import Region
from reports.templatetags.report_tags import has_access

def test_has_access():
    print("=" * 60)
    print("Testing has_access Template Filter")
    print("=" * 60)
    
    # Get testuser
    testuser = User.objects.get(username='testuser')
    aus_region = Region.objects.get(country_code='AUS')
    
    # Test with AU Daily Report
    reports = Report.objects.filter(
        product__name='AU Daily Report',
        region=aus_region
    )[:5]
    
    print(f"\nTesting {reports.count()} AU Daily Report reports:\n")
    
    for report in reports:
        result = has_access(report, testuser)
        status = "✅ CAN ACCESS" if result else "❌ NO ACCESS"
        print(f"{status}: {report.title}")
        print(f"  Products: {[p.name for p in report.product.all()]}")
        print(f"  Result: {result}\n")
    
    # Test with a report user shouldn't have access to
    other_reports = Report.objects.filter(region=aus_region).exclude(
        product__name__in=['AU Daily Report', 'AU Mining Report', 'US Equity (AU)']
    )[:2]
    
    if other_reports:
        print("\nTesting reports user should NOT have access to:\n")
        for report in other_reports:
            result = has_access(report, testuser)
            status = "✅ CAN ACCESS" if result else "❌ NO ACCESS"
            print(f"{status}: {report.title}")
            print(f"  Products: {[p.name for p in report.product.all()]}")
            print(f"  Result: {result}\n")
    
    print("=" * 60)
    print("Test Complete")
    print("=" * 60)
    print("\nIf the filter is working correctly:")
    print("  ✅ AU Daily Report reports should show 'CAN ACCESS'")
    print("  ❌ Other reports should show 'NO ACCESS'")
    print("\nIf homepage still shows 'Subscribe to Access':")
    print("  1. Restart the Django server")
    print("  2. Clear browser cache (Ctrl+Shift+R)")
    print("  3. Log out and log back in")

if __name__ == "__main__":
    try:
        test_has_access()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
