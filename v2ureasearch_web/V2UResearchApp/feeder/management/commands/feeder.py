from django.core.management.base import BaseCommand, CommandError
from os import path
import json
from users.models import Region
from marketing.models import Product
from company.models import Sector, ResearchTypes
from home.models import Pages
from company.models import Company
from time import time
import datetime
import random
from reports.models import Report
from django.contrib.auth.models import User 
from django.utils.text import slugify

class Command(BaseCommand):
    help = "Generating the default feed data."

    def source_check(self, file_name='stub-data.json'):
        stub_file_path = path.abspath('./') + '/feeder/' + file_name
        if not path.isfile(stub_file_path):
            return False
        else:
            return open(stub_file_path)

    def add_arguments(self, parser):
        parser.add_argument("actions", nargs="+", type=str)

    def feed_region(self, obj_data=[]):
        for region_data in obj_data:
            obj, created = Region.objects.update_or_create(
                country_name = region_data['RegionName'],
                timezone = region_data['Timezone'],
                country_code = region_data['RegionCode'],
                currency = region_data['Currency'],
                is_default = region_data['IsDefault'],
            )
            obj.save()
            print(obj, created)
        return obj, created

    def feed_product(self, obj_data=[]):
        for product_data in obj_data:
            region_obj = Region.objects.get(country_code=product_data["region"])
            obj, created = Product.objects.update_or_create(
                name = product_data["Name"],
                slug = product_data["Slug"],
                duration = product_data["Duration"],
                cost = product_data["Cost"],
                description = product_data["Description"],
                hot = product_data["Hot"],
                new = product_data["New"],
                most_sellable = product_data["MostSellable"],
                feature_image_url = product_data["FeaturedImage_URL"],
                is_active = product_data["IsActive"],
                region = region_obj
            )
            obj.save()
            print(obj, created)
        return obj, created
    
    def feed_sector(self, obj_data=[]):
        for sector_data in obj_data:
            region_obj = Region.objects.get(country_code=sector_data["Region"])
            obj, created = Sector.objects.update_or_create(
                sector_name = sector_data["Name"],
                slug = sector_data["Slug"],
                feature_image_url = sector_data["FeatureImageURL"],
                description = sector_data["Description"],
                region = region_obj
            )
            obj.save()
            print(obj, created)
        return obj, created
    
    def feed_page(self, obj_data=[]):
        for page_data in obj_data:
            region_obj = Region.objects.get(country_code=page_data["PageRegion"])
            obj, created = Pages.objects.update_or_create(
                title = page_data["PageTitle"],
                slug = page_data["PageSlug"],
                feature_image_url = "",
                description = page_data["PageContent"],
                summary = "",
                region = region_obj
            )
            obj.save()
            print(obj, created)
        return obj, created
    
    def feed_researchtypes(self, obj_data=[]):
        for sector_data in obj_data:
            region_obj = Region.objects.get(country_code=sector_data["Region"])
            obj, created = ResearchTypes.objects.update_or_create(
                name = sector_data["Name"],
                slug = sector_data["Slug"],
                region = region_obj
            )
            obj.save()
            print(obj, created)
        return obj, created
    
    def feed_company(self, obj_data=[]):
        for company_data in obj_data:
            region_obj = Region.objects.get(country_code=company_data["Region"])
            p, sector_obj = Sector.objects.get_or_create(
                sector_name=company_data['Sector'],
                region=region_obj,
                defaults={"feature_image_url":"", "description":""}
            )
            print(p, sector_obj)
            obj, created = Company.objects.update_or_create(
                name = company_data["Name"],
                slug = company_data["Slug"],
                symbol = company_data["Symbol"],
                description = company_data["Name"],
                region = region_obj
            )
            obj.sector.set([p])
            obj.save()
            print(obj, created)
        return obj, created

    def feed_report(self, report_data):
        report_template_prime = report_data['ReportContent']
        region_obj = Region.objects.get(country_code=report_data["ReportRegion"])
        researchtypes = ResearchTypes.objects.filter(region=region_obj)
        researchtype_obj = random.choices(researchtypes)[0]
        products = Product.objects.filter(region=region_obj)
        product_obj = random.choices(products)
        user_obj = User.objects.get(id=1)
        start_date = datetime.date(2023, 1, 1)
        end_date = datetime.date.today()
        # end_date = datetime.date(2022, 1, 2)
        while start_date <= end_date:
            # print(start_date.weekday(), start_date.weekday() + 10 )
            sector_obj = Sector.objects.get(id=start_date.weekday() + 10, region=region_obj)
            companies = Company.objects.filter(sector=sector_obj, region=region_obj)
            selected_company = random.choices(companies)[0]
            rc_count = len(Report.objects.filter(company__id=selected_company.id))
            print(rc_count)
            report_slug = slugify(selected_company.name + ' ' + str(rc_count)) 
            # print(companies, len(companies), selected_company['name'])
            # print(selected_company.name)
            report_template = report_template_prime.replace("COMPANY__NAME", selected_company.name)
            report_template = report_template.replace("COMPANY__SECTOR", sector_obj.sector_name)
            report_template = report_template.replace("COMPANY_REPORT_DATE", start_date.strftime("%B, %d, %Y"))
            # print(report_template)
            r_time = datetime.time(0,0,0,0)
            report_datetime = datetime.datetime.combine(start_date, r_time)
            obj_p = Report(
                title=selected_company.name,
                slug=report_slug,
                short_description="",
                description=report_template,
                author=user_obj,
                published_date=report_datetime,
                draft_date=report_datetime,
                segment=researchtype_obj,
                traget_price=int(random.random() * 1000),
                is_free=False,
                is_featured=False,
                feature_image_url="",
            )

            obj_p.save()

            obj_p.product.set(product_obj)
            obj_p.sector.set([sector_obj])
            obj_p.company.set([selected_company])
            obj_p.region.set([region_obj])
            obj_p.save()

            start_date = start_date + datetime.timedelta(days=1)
        # Reset products created and updated dates

    def handle(self, *args, **options):
        stub_check = self.source_check()
        if not stub_check:
            print("Error! Source file does not existed.")
            return
        else:
            try:
                json_file_data = json.load(stub_check)
            except Exception as Ex:
                print("Error! Source file parsing error.", Ex)
                return

        for action in options['actions']:
            if action == "region":
                obj, created = self.feed_region(json_file_data['Regions'])
            elif action == "product":
                obj, created = self.feed_product(json_file_data['Products'])
            elif action == "sectors":
                obj_created = self.feed_sector(json_file_data['Sectors'])
            elif action == "researchtypes":
                obj_created = self.feed_researchtypes(json_file_data['ResearchTypes'])
            elif action == "pages":
                obj_created = self.feed_page(json_file_data['Pages'])
            elif action == "companies":
                obj_created = self.feed_company(json_file_data['Companies'])
            elif action == "reports":
                obj_created = self.feed_report(json_file_data['ReportTemplate'])
            else:
                print("Un-identifying acction. Kindly re-check before executing.")