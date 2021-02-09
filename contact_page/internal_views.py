from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import datetime
from .models import *
from .myforms import *
from json import dumps
from django.contrib.auth.views import PasswordChangeView, PasswordResetDoneView

class ChangePassword(PasswordChangeView):
    template_name = 'contact_page/change_password.html'
    success_url = reverse_lazy('contact_page:password_done')

class PasswordDone(PasswordResetDoneView):
    template_name = 'contact_page/password_reset.html'

def demo(request):
    return HttpResponse('Prick!')

def inside(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('contact_page:hostLogin', args = [True, 'inside']))
    else:
        thishost = Host.objects.get(email = request.user.email)
        meetings = thishost.meetings.filter(fixed = False , ignored = False)
        jsonmeetings = []
        for meeting in meetings:
            details = {}
            visitor = {}
            visitor['first_name'] = meeting.visitor.first_name
            visitor['last_name'] = meeting.visitor.last_name
            visitor['email'] = meeting.visitor.email
            visitor['phone_number'] = meeting.visitor.phone_number
            details['visitor'] = visitor
            details['meeting_date'] = meeting.meeting_date.strftime('%d/%m/%Y')
            details['meeting_begin'] = meeting.meeting_begin.strftime('%H:%M')
            details['meeting_end'] = meeting.meeting_end.strftime('%H:%M')
            details['location'] = meeting.location
            details['deletion_link'] = reverse('contact_page:ignore_meeting', args = [meeting.token])
            details['confirmation_link'] = reverse('contact_page:confirm_meeting', args = [meeting.token])
            details['purpose'] = meeting.purpose
            jsonmeetings.append(details)
        meetings = dumps(jsonmeetings)
        return render(request, 'contact_page/inside.html', {
            'meetings' : meetings
        })

def modify_host_data(request):

    def extract_relevant_details(fields, data):
        info = {}
        for field in fields:
            if field in data:
                info[field] = data[field]
        return info

    def set_attributes(theobject, attributes):
        attributes_val_pairs = {}
        for attribute in attributes:
            attributes_val_pairs[attribute] = attributes[attribute]
        for things in attributes_val_pairs:
            command = f"theobject.{things} = attributes_val_pairs['{things}']"
            print(theobject)
            exec(f"theobject.{things} = attributes_val_pairs['{things}']")
            print(command)
        theobject.save()

    if not request.user.is_authenticated:
        return HttpResponseRedirect('https://www.interpol.int/Crimes/Cybercrime')
    else:
        if request.method == 'POST':
            materials = {}
            thishost = Host.objects.get(email = request.user.email)
            thisUser = User.objects.get(email = request.user.email)
            thisaddress = thishost.mailing_address
            first_name = last_name = phone_number = street_name = house_number = city = postal_code = country = None
            fields_user = ['first_name', 'last_name']
            fields_host = ['first_name', 'last_name', 'phone_number']
            fields_address = ['street_name', 'house_number', 'city', 'postal_code', 'country']
            print(thishost)
            print(thisUser)
            print(thisaddress)
            set_attributes(thisUser, extract_relevant_details(fields_user, request.POST))
            set_attributes(thishost, extract_relevant_details(fields_host, request.POST))
            set_attributes(thisaddress, extract_relevant_details(fields_address, request.POST))
            return render(request, 'contact_page/personal_data.html', {
                'success':True
            })
        else:
            return HttpResponseRedirect(reverse('contact_page:inside'))

def get_fixed_meetings(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('contact_page:hostLogin', args = [True, 'get_fixed_meetings']))
    else:
        thishost = Host.objects.get(email = request.user.email)
        meetings = thishost.meetings.filter(fixed = True)
        jsonmeetings = []
        for meeting in meetings:
            details = {}
            visitor = {}
            visitor['first_name'] = meeting.visitor.first_name
            visitor['last_name'] = meeting.visitor.last_name
            visitor['email'] = meeting.visitor.email
            visitor['phone_number'] = meeting.visitor.phone_number
            details['visitor'] = visitor
            details['meeting_date'] = meeting.meeting_date.strftime('%d/%m/%Y')
            details['meeting_begin'] = meeting.meeting_begin.strftime('%H:%M')
            details['meeting_end'] = meeting.meeting_end.strftime('%H:%M')
            details['location'] = meeting.location
            details['deletion_link'] = reverse('contact_page:ignore_meeting', args = [meeting.token])
            details['purpose'] = meeting.purpose
            jsonmeetings.append(details)
        meetings = dumps(jsonmeetings)
        return render(request, 'contact_page/fixed_meetings.html', {
            'meetings' : meetings
        })

def get_ignored_meetings(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('contact_page:hostlogin', param = [True, 'get_ignored_meetings']))
    else:
        thishost = Host.objects.get(email = request.user.email)
        meetings = thishost.meetings.filter(ignored = True)
        jsonmeetings = []
        for meeting in meetings:
            details = {}
            visitor = {}
            visitor['first_name'] = meeting.visitor.first_name
            visitor['last_name'] = meeting.visitor.last_name
            visitor['email'] = meeting.visitor.email
            visitor['phone_number'] = meeting.visitor.phone_number
            details['visitor'] = visitor
            details['meeting_date'] = meeting.meeting_date.strftime('%d/%m/%Y')
            details['meeting_begin'] = meeting.meeting_begin.strftime('%H:%M')
            details['meeting_end'] = meeting.meeting_end.strftime('%H:%M')
            details['location'] = meeting.location
            details['confirmation_link'] = reverse('contact_page:confirm_meeting', args = [meeting.token])
            details['purpose'] = meeting.purpose
            jsonmeetings.append(details)
        meetings = dumps(jsonmeetings)
        return render(request, 'contact_page/get_ignored_meetings.html', {
            'meetings' : meetings
        })

def ignore_meeting(request, token):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('https://www.interpol.int/Crimes/Cybercrime')
    else:
        the_meeting = Meeting.objects.get(token=token)
        the_meeting.ignored = True
        the_meeting.fixed = False
        the_meeting.save()
        return HttpResponse('ignored')

def confirm_meeting(request, token):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('https://www.interpol.int/Crimes/Cybercrime')
    else:
        the_meeting = Meeting.objects.get(token=token)
        the_meeting.fixed = True
        the_meeting.ignored = False
        the_meeting.save()
        return HttpResponse('confirmed' , content_type = 'text/plain')

def personal_data(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('contact_page:hostLogin', args = [True, 'personal_data']))
    this_host = Host.objects.get(email = request.user.email)
    address = this_host.mailing_address
    host_data = {
        'first_name':{
            'name' : 'first_name',
            'label' : 'First Name',
            'placeholder' : this_host.first_name,
            'type' : 'text',
            'category' :'changeable',
            'class':'personal_info'
        },
        'last_name':{
            'label' : 'Last Name',
            'name': 'last_name',
            'placeholder' : this_host.last_name,
            'type' : 'text',
            'category' : 'changeable',
            'class':'personal_info'
        },
        'email':{
            'label' : 'Email',
            'name':'email',
            'placeholder':this_host.email,
            'type' : 'text',
            'category' : 'changeable',
            'class':'personal_info'
        },
        'username':{
            'name':'username',
            'label':'Username',
            'placeholder':this_host.username.username,
            'type':'text',
            'category':'not_changeable',
            'class':'personal_info'
        },
        'phone_number':{
            'label' : 'Phone Number',
            'name':'phone_number',
            'placeholder':this_host.phone_number,
            'type':'text',
            'category':'changeable',
            'class':'personal_info'
        },
        'street_name':{
            'label':'Street Name',
            'name':'street_name',
            'placeholder':this_host.mailing_address.street_name,
            'type':'text',
            'category':'changeable',
            'class':'address_info'
        },
        'house_number':{
            'label':'House Number',
            'name':'house_number',
            'placeholder':this_host.mailing_address.house_number,
            'type':'number',
            'category':'changeable',
            'class':'address_info'
        },
        'city':{
            'label' : 'City',
            'name':'city',
            'placeholder':this_host.mailing_address.city,
            'type':'text',
            'category':'changeable',
            'class':'address_info'
        },
        'postal_code':{
            'label' : 'Postal Code',
            'name':'postal_code',
            'placeholder':this_host.mailing_address.postal_code,
            'type':'number',
            'category':'changeable',
            'class':'address_info'
        },
        'country':{
            'label': 'Country',
            'name':'country',
            'placeholder':this_host.mailing_address.country,
            'type':'text',
            'category':'changeable',
            'class':'address_info'
        }
    }
    return render(request, 'contact_page/personal_data.html', {
        'data': dumps(host_data),
        'first_load':True
    })

