import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User as AuthUser
from users.models import User as AppUser, Region
from company.models import Sector, ResearchTypes, Company
from marketing.models import Product, Lead, SocialHandle, Articles
from reports.models import Report
from sales.models import Package, Invoice, Payment
from testimonials.models import ClientTestimonials
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populates the database with dummy data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        self.stdout.write('Creating dummy data...')

        # 1. Regions
        regions = []
        for _ in range(10):
            region = Region.objects.create(
                country_name=fake.country(),
                timezone=timezone.now().time(),
                country_code=fake.country_code(),
                currency=fake.currency_code(),
                is_default=False,
                corp_address=fake.address(),
                corp_contact=fake.name(),
                corp_email=fake.company_email(),
                corp_text=fake.catch_phrase(),
                corp_number=fake.phone_number()[:20],
                is_active=True,
                tradingview_exchange_code='NYSE',
                region_hostname=fake.domain_name()
            )
            regions.append(region)
        self.stdout.write(self.style.SUCCESS(f'Created {len(regions)} Regions'))

        # 2. Auth Users
        auth_users = []
        for _ in range(10):
            user = AuthUser.objects.create_user(
                username=fake.user_name() + str(random.randint(1000, 9999)),
                email=fake.email(),
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            auth_users.append(user)
        self.stdout.write(self.style.SUCCESS(f'Created {len(auth_users)} Auth Users'))

        # 3. App Users
        app_users = []
        for _ in range(10):
            user = AppUser.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone=random.randint(100000000, 2147483647),
                subscription_status='Active',
                sex=random.choice(['Male', 'Female']),
                secondary_email=fake.email(),
                secondary_phone=random.randint(100000000, 2147483647),
                address=fake.address(),
                zip_code=fake.zipcode(),
                income=fake.email(), # Field says income but type is EmailField in model... keeping it safe
                registered_device_1=random.randint(1, 100),
                registered_device_2=random.randint(1, 100),
                free_trial=fake.boolean(),
                expire_date=fake.future_date()
            )
            app_users.append(user)
        self.stdout.write(self.style.SUCCESS(f'Created {len(app_users)} App Users'))

        # 4. Sectors
        sectors = []
        for _ in range(10):
            sector = Sector.objects.create(
                sector_name=fake.job(),
                slug=fake.slug() + str(random.randint(1000,9999)),
                description=fake.text(),
                region=random.choice(regions)
            )
            sector.regions.set(random.sample(regions, k=random.randint(1, 3)))
            sectors.append(sector)
        self.stdout.write(self.style.SUCCESS(f'Created {len(sectors)} Sectors'))

        # 5. ResearchTypes
        research_types = []
        for _ in range(10):
            rt = ResearchTypes.objects.create(
                name=fake.bs(),
                slug=fake.slug() + str(random.randint(1000,9999)),
                region=random.choice(regions)
            )
            rt.regions.set(random.sample(regions, k=random.randint(1, 3)))
            research_types.append(rt)
        self.stdout.write(self.style.SUCCESS(f'Created {len(research_types)} ResearchTypes'))

        # 6. Companies
        companies = []
        for _ in range(10):
            company = Company.objects.create(
                name=fake.company(),
                symbol=fake.lexify(text="????").upper(),
                description=fake.text(),
                slug=fake.slug() + str(random.randint(1000,9999)),
                region=random.choice(regions)
            )
            company.sector.set(random.sample(sectors, k=random.randint(1, 3)))
            company.regions.set(random.sample(regions, k=random.randint(1, 3)))
            companies.append(company)
        self.stdout.write(self.style.SUCCESS(f'Created {len(companies)} Companies'))

        # 7. Products
        products = []
        for _ in range(10):
            product = Product.objects.create(
                name=fake.catch_phrase(),
                slug=fake.slug() + str(random.randint(1000,9999)),
                duration="1 Month",
                cost=random.randint(10, 1000),
                description=fake.text(),
                hot=fake.boolean(),
                new=fake.boolean(),
                most_sellable=fake.boolean(),
                is_platinum=fake.boolean(),
                is_active=True,
                spec_1=fake.word(),
                spec_2=fake.word(),
                spec_3=fake.word(),
                spec_4=fake.word(),
                spec_5=fake.word()
            )
            product.regions.set(random.sample(regions, k=random.randint(1, 3)))
            products.append(product)
        self.stdout.write(self.style.SUCCESS(f'Created {len(products)} Products'))

        # 8. Packages
        packages = []
        for _ in range(10):
            package = Package.objects.create(
                name=fake.bs(),
                duration="1 Year",
                cost=random.randint(100, 5000),
                description=fake.text(),
                hot=fake.boolean(),
                new=fake.boolean(),
                most_sellable=fake.boolean(),
                feature_image_url=fake.image_url()
            )
            package.products.set(random.sample(products, k=random.randint(1, 3)))
            packages.append(package)
        self.stdout.write(self.style.SUCCESS(f'Created {len(packages)} Packages'))

        # 9. Invoices
        invoices = []
        for _ in range(10):
            invoice = Invoice.objects.create(
                user=random.choice(app_users),
                package=random.choice(packages),
                amount=random.randint(100, 5000),
                discount=random.randint(0, 50),
                created_by=random.choice(app_users) 
            )
            invoices.append(invoice)
        self.stdout.write(self.style.SUCCESS(f'Created {len(invoices)} Invoices'))

        # 10. Reports
        for _ in range(10):
            report = Report.objects.create(
                title=fake.sentence(),
                slug=fake.slug() + str(random.randint(1000,9999)),
                short_description=fake.text(max_nb_chars=200),
                summary_title=fake.sentence(),
                description=fake.text(),
                left_description=fake.text(),
                author=random.choice(auth_users),
                published_date=timezone.now(),
                traget_price=round(random.uniform(10.0, 500.0), 2),
                cmp=round(random.uniform(10.0, 500.0), 2),
                risk_level=random.choice(Report.RiskLevelChoices.values),
                recommendation=random.choice(Report.RecommendationChoices.values),
                segment=random.choice(research_types),
                is_free=fake.boolean(),
                is_featured=fake.boolean(),
                is_daily=fake.boolean()
            )
            report.product.set(random.sample(products, k=random.randint(1, 3)))
            report.region.set(random.sample(regions, k=random.randint(1, 3)))
            report.sector.set(random.sample(sectors, k=random.randint(1, 3)))
            report.company.set(random.sample(companies, k=random.randint(1, 3)))
        self.stdout.write(self.style.SUCCESS('Created 10 Reports'))

        # 11. Leads
        for _ in range(10):
            Lead.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                source=fake.word(),
                email=fake.email(),
                phone=fake.phone_number()[:15], 
                user_agent={},
                setup_password=fake.password(),
                is_free_trial=fake.boolean(),
                first_time=fake.boolean()
            )
        self.stdout.write(self.style.SUCCESS('Created 10 Leads'))

        # 12. Testimonials
        for _ in range(10):
            testimonial = ClientTestimonials.objects.create(
                name=fake.name(),
                testimonial=fake.paragraph(nb_sentences=3)
            )
            testimonial.region.set([random.choice(regions)])
        self.stdout.write(self.style.SUCCESS('Created 10 Testimonials'))

        # 13. More Reports (for Carousel)
        for _ in range(20):
            report = Report.objects.create(
                title=fake.catch_phrase(),
                slug=fake.slug() + str(random.randint(10000,99999)),
                short_description=fake.text(max_nb_chars=200),
                summary_title=fake.sentence(),
                description=fake.text(),
                left_description=fake.text(),
                author=random.choice(auth_users),
                published_date=timezone.now(),
                risk_level=random.choice(Report.RiskLevelChoices.values),
                recommendation=random.choice(Report.RecommendationChoices.values),
                segment=random.choice(research_types),
                is_free=random.choice([True, False]),
                is_featured=True, # Force some to be featured for carousel
                is_daily=random.choice([True, False])
            )
            report.product.set(random.sample(products, k=1))
            report.region.set(random.sample(regions, k=1))
        self.stdout.write(self.style.SUCCESS('Created 20 More Reports (Mixed Featured)'))

        self.stdout.write(self.style.SUCCESS('Dummy data population complete!'))
