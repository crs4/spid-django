from django.contrib.auth.models import AbstractUser
from django.db import models


class SpidUser(AbstractUser):
    spid_code = models.CharField(max_length=40, blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    iva_code = models.CharField(max_length=20, blank=True, null=True)
    place_of_birth = models.CharField(max_length=40, blank=True, null=True)
    company_name = models.CharField(max_length=50, blank=True, null=True)
    mobile_phone = models.CharField(max_length=12, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    digital_address = models.EmailField(blank=True, null=True)
    registered_office = models.CharField(max_length=100, blank=True, null=True)
    id_card = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    county_of_birth = models.CharField(max_length=2, blank=True, null=True)
