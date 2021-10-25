from django.db import models
#from api.models import Company

# Create your models here.

class AdminUser(models.Model):
    username = models.TextField(default='')
    password = models.TextField(default='')
    company = models.ForeignKey("api.Company", on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.username