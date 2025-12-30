"""
URL configuration for V2UResearchApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path as url
from django.views.generic import RedirectView
from django.contrib.sitemaps.views import sitemap 
from V2UResearchApp.sitemaps.products_sitemap import ProductSitemap
from V2UResearchApp.sitemaps.reports_sitemap import ReportsSitemap
from V2UResearchApp.sitemaps.free_reports_sitemap import FreeReportsSitemap
from V2UResearchApp.sitemaps.pages_sitemap import PagesSitemap
from V2UResearchApp.sitemaps.sectors_sitemap import SectorsSitemap
from V2UResearchApp.sitemaps.articles_sitemap import ArticlesSitemap

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views as ckeditor_views
from reports.views import FreeReportListView, SearchReportList

admin.site.site_header = "V2U Research Admin"
admin.site.site_title = "V2U Research Admin Portal"
admin.site.index_title = "Welcome to V2U Research Portal"

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('allauth.urls')),
    path('login', RedirectView.as_view(url='/accounts/login/', permanent=True), name='login_redirect'),
    path('lp/', include('lp.urls')),
    path('report/', include('reports.urls')),
    path('api/', include('apis.urls')),
    path('product/', include('marketing.urls')),
    path('sector/', include('company.urls')),
    path('profile/', include('users.urls')),
    path('free-reports', FreeReportListView.as_view(), name='report-free-listing'),
    path('search', SearchReportList.as_view(), name='search'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),
    # url(r'^ckeditor/upload/', login_required(ckeditor_views.upload), name='ckeditor_upload'),
    # url(r'^ckeditor/browse/', never_cache(login_required(ckeditor_views.browse)), name='ckeditor_browse'),
    path('sitemap.xml', sitemap, {'sitemaps': {
        'Pages': PagesSitemap,
        'Articles': ArticlesSitemap, 
        'Sectors': SectorsSitemap,
        'Products': ProductSitemap, 
        'FreeReports': FreeReportsSitemap,
        'Reports': ReportsSitemap
        }}, name='django.contrib.sitemaps.views.sitemap')
] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Fallback for local uploads (Serving /media/uploads/ from BASE_DIR/uploads)
urlpatterns += static('/media/uploads/', document_root=settings.BASE_DIR / 'uploads')

# if settings.DEBUG:
#    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
