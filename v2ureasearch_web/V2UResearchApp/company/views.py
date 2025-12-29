from django.shortcuts import render
from django.views.generic import DetailView

from reports.models import Report
from .models import Sector


# Create your views here.

class SectorDetailView(DetailView):
    model = Sector
    template_name = "company/sector_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reports"] = Report.objects.filter(sector=kwargs.get('object'))
        return context