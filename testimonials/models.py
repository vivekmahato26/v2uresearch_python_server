from django.db import models
from users.models import Region

class ClientTestimonials(models.Model):
    name = models.CharField(max_length=255, null=False)
    testimonial = models.TextField(null=False)
    region = models.ManyToManyField(Region, null=False)

    def __str__(self):
        return self.name
