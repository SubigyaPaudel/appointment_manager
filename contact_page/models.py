from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone as tz
import datetime

# Create your models here.

def phonenumber(number):
    if len(number) != 10:
        raise ValidationError(f"{number} is not 10 digits")

def hashvalidator(token):
    if len(token) != 10:
        raise ValidationError('Hash not 64 characters long!')

class Address(models.Model):
    username = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'address', null = True)
    street_name = models.CharField(max_length = 150, null = False, blank = False)
    house_number = models.IntegerField(null = False, blank = False)
    city = models.CharField(max_length = 150, null = False, blank = False)
    postal_code = models.IntegerField(null = False, blank = False)
    country = models.CharField(max_length = 30)

    def __str__(self):
        return f"{self.street_name} {self.house_number}\n{self.city} {self.postal_code}\n{self.country}"

class Visitor(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 256, unique = True, null = False, blank = False)
    phone_number = models.CharField(max_length = 10, validators = [phonenumber], null = False, blank = False, unique = True)
   
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Host(models.Model):
    username = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'logical_account', null = True)
    #The above statement might be a source of confusion. It is a foreign key to the User's table, and not the username of that 
    #user in the table
    first_name = models.CharField(max_length = 100, blank = False, null = True)
    last_name = models.CharField(max_length = 100, blank = False, null = True)
    email = models.EmailField(max_length = 256, unique = True, blank = False, null = True)
    phone_number = models.CharField(max_length = 10, validators = [phonenumber], null = True, unique = True)
    mailing_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='h_office')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Meeting(models.Model):
    host = models.ForeignKey(Host, related_name = 'meetings', on_delete = models.CASCADE, null = True)
    visitor = models.ForeignKey(Visitor, related_name = 'meetings', on_delete = models.CASCADE, null = True)
    meeting_date = models.DateField(auto_now=False, auto_now_add=False, default = tz.now().date().strftime('%d/%m/%y'))
    meeting_begin = models.TimeField(auto_now=False, auto_now_add=False, default = tz.now().date().strftime('%H/%M/%S'))
    meeting_end = models.TimeField(auto_now=False, auto_now_add=False, default =  tz.now().date() .strftime('%H/%M/%S'))
    location = models.TextField(null = False, blank = False, default = 'Undecided')
    fixed = models.BooleanField(default = False)
    token = models.CharField(max_length = 64, blank = False, null = False, validators = [hashvalidator], default = "0"*64)
    ignored = models.BooleanField(default = False)
    purpose = models.TextField(max_length = 2048, null = False, blank = False, default = 'Unspecified')

    def __str__(self):
        return f"{self.visitor} -> {self.host}"
    