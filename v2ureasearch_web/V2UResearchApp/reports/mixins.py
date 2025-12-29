from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from .models import Report
from users.models import User


class ProductPermissionRequiredMixin:

    def dispatch(self, request, *args, **kwargs):

        product=getattr(self.get_object(), 'product').all()
        perms = ["Can View "+p.name for p in product]
        
        permissions = self.request.user.user_permissions.filter(name__in=perms)

        context = {"report": self.get_object()}

        if permissions:
            return super().dispatch(request, *args, **kwargs)
        else:
            return render(request, "home/unsubscribed_report.html", context)