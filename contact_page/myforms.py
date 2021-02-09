from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

class CreateUserForm(UserCreationForm):
    #for authentication
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 100, required = True, widget = forms.TextInput(attrs = {
        'placeholder':'Username'
    }))
    password = forms.CharField(max_length = 100, widget = forms.PasswordInput(attrs = {
        'placeholder':'Password'
    }))

class UserModificationForm(ModelForm):
    class Meta:
        model = Host
        fields = ['first_name', 'last_name', 'phone_number']

class PasswordForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['password1', 'password2']

class NewHostForm(ModelForm):
    #for the representation of the user in the database
    class Meta:
        model = Host
        fields = ['phone_number']

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['street_name','house_number','city', 'postal_code','country' ]
        
class VisitorForm(ModelForm):
    class Meta:
        model = Visitor
        fields = '__all__'

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        fields = ['meeting_date', 'meeting_begin', 'meeting_end', 'location']
        #widgets to control the appearence of form fields
        widgets = {
            'meeting_date': DateInput(),
            'meeting_begin': TimeInput(),
            'meeting_end': TimeInput()
        }

class LookUpForm(forms.Form):
    host_last_name = forms.CharField(max_length = 100, required = True, widget = forms.TextInput(attrs = {
        'label':'Host Last Name',
        'placeholder': "Enter the host's last name"
    }))
    visitor_last_name = forms.CharField(max_length = 100, widget = forms.TextInput(attrs = {
        'label':'Your Last Name',
        'placeholder': "Enter the your last name"
    }))
    meeting_token = forms.CharField(max_length = 10, widget = forms.PasswordInput(attrs = {
        'label':'Meeting Token',
        'placeholder': "Enter the meeting's token"
    }))