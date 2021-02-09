from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.timezone import timezone as tz
from datetime import datetime
from .models import *
from .myforms import *
from json import dumps
from hashlib import sha256

# Create your views here.

def tokengenerator(combined):
    hash_obj = sha256(bytearray(combined, encoding = 'utf-8'))
    return hash_obj.hexdigest()[10:20]

def search(request):
    return render(request, 'contact_page/search.html')

def welcome(request):
    return render(request, "contact_page/welcome.html")

def wrong_page(request, name):
    return HttpResponseNotFound(f"The page contact_page/{name} does not exist")

def hostlogin(request, redirect = 'False', destination = 'did_not_happen'):
    #this function should only be called after checking whether the user has been authenticated or not
    #the checking of the authentication status of the user below is just to address the situation whereby
    #an authenticated user clicks the login button on the landing page
    redirected = None
    print(redirect)
    if redirect.upper() == 'TRUE':
        redirected = True
    else:
        redirected = False
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('contact_page:inside'))
    if request.method == 'GET':
        if redirected: #redirected shows whether the user was compelled to sign in or not
            materials = {'form':LoginForm(), 'redirected': True, 'message': 'Please sign in before you continue' ,'destination':destination}
        else:
            materials = {'form':LoginForm(), 'redirected': False, 'destination' : 'inside'}
        print(materials)
        return render(request, 'contact_page/hostlogin.html', materials)
    elif request.method == 'POST':
        credentials = LoginForm(request.POST)
        materials = {
            'form':credentials,
            'redirected' : redirect,
            'destination' : destination
        }
        if credentials.is_valid():
            username = credentials.cleaned_data.get('username')
            password = credentials.cleaned_data.get('password')
            user = authenticate(request, username = username, password = password)
            if not user is None:
                login(request, user)
                if materials['redirected'] != 'did_not_happen':
                    return HttpResponseRedirect(reverse('contact_page:' + materials['destination']))
                else:
                    return HttpResponseRedirect(reverse('contact_page:inside'))
            else:
                materials['message'] = 'Invalid sign-in credentials'
                return render(request, 'contact_page/hostlogin.html', materials)
        else:
            materials['message'] = 'Incompatible sign-in credentials'
            return render(request, 'contact_page/hostlogin.html', materials)

def hostlogout(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('contact_page:welcome'))
    else:
        logout(request)
        return HttpResponseRedirect(reverse('contact_page:welcome'))

def signup(request):
    if request.method == 'GET':
        return render(request, 'contact_page/hostsignup.html', {
            'authform': CreateUserForm(),
            'userdataform': NewHostForm(),
            'addressform': AddressForm()
        })
    elif request.method == 'POST':
        data1 = CreateUserForm(request.POST)
        data2 = NewHostForm(request.POST)
        data3 = AddressForm(request.POST)
        if data1.is_valid() and data2.is_valid() and data3.is_valid():
            data1.save() #Creating the user
            First_name = data1.cleaned_data.get('first_name')
            Last_name = data1.cleaned_data.get('last_name')
            Email_address = data1.cleaned_data.get('email')
            Phonenumber = data2.cleaned_data.get('phone_number')
            Street_name = data3.cleaned_data.get('street_name')
            House_number = data3.cleaned_data.get('house_number')
            City = data3.cleaned_data.get('city')
            Postal_code = data3.cleaned_data.get('postal_code')
            Username = User.objects.get(email = Email_address) #getting the authetication version of the user to link it with the logical version of the user.
                                                                #Works because every user is supposed to have a different email
            Country = data3.cleaned_data.get('country')
            host_address = Address(username = Username, street_name = Street_name, house_number = House_number, city = City, postal_code = Postal_code, country = Country)
            host_address.save() # Putting a new entry in the address table
            newhost = Host(username = Username, first_name = First_name, last_name = Last_name, email = Email_address, phone_number = Phonenumber, mailing_address = host_address)
            newhost.save()
            return HttpResponseRedirect(reverse('contact_page:inside'))
        else:
            message = 'Invalid data, please fill the form again\n'
            if not data1.is_valid():
                print('data1 invalid')
                message += 'Sign in details are invalid\n'
            if not data2.is_valid():
                print('data1 invalid')
                message += 'Personal details are invalid\n'
            if not data3.is_valid():
                print('data1 invalid')
                message += 'Address details are invalid\n'
            return render(request, 'contact_page/hostsignup.html', {
                'authform': data1,
                'userdataform': data2,
                'addressform': data3,
                'message': message
            })

def autocomplete(request):
    table_name = request.GET.get('table', 'Empty')
    column_name = request.GET.get('column', 'Empty')
    like = request.GET.get('like', 'nothing')
    if like != 'nothing' and column_name != 'Empty' and table_name != 'Empty':
        query = f"""SELECT DISTINCT id, {column_name}
        FROM contact_page_{table_name} T
        WHERE T.{column_name} LIKE "{like}%%";
        """
        result = eval(f"{table_name}.objects.raw(query)")
        response = {}
        for i in result:
            response[i.id] = eval(f"i.{column_name}")
        return JsonResponse(response)
    else:
        return JsonResponse(data = {})

def search_results(request):
    if request.method == 'POST':
        search_method = request.POST['searchtype']
        if search_method == 'NameSearch':
            FirstName, LastName = request.POST['FirstName'], request.POST['LastName']
            query = f"""SELECT * 
            FROM contact_page_HOST H
            WHERE H.first_name LIKE "{FirstName}%%" AND H.last_name LIKE "{LastName}%%";"""
            results = Host.objects.raw(query)
            jsondata = {}
            for result in results:
                jsondata[result.id] = {'first_name':result.first_name, 'last_name':result.last_name, 'email' : result.email}
            final_data = dumps(jsondata)
            print(final_data)
            return render(request, 'contact_page/search_results.html', {
                'hosts' : final_data
            })
        elif search_method == 'EmailSearch':
            email = request.POST['Email']
            query = f"""SELECT * 
            FROM contact_page_HOST H
            WHERE H.email LIKE "{email}%%";"""
            results = Host.objects.raw(query)
            jsondata = {}
            for result in results:
                jsondata[result.id] = {'first_name':result.first_name, 'last_name':result.last_name, 'email' : result.email}
            final_data = dumps(jsondata)
            print(final_data)
            return render(request, 'contact_page/search_results.html', {
                'hosts' : final_data
            })
        else:
            return HttpResponseRedirect(reverse('contact_page:welcome'))
    else:
        return render(request, 'contact_page/search_results.html')

def search_further(request):
    Email_address = request.GET.get('email')
    result = Host.objects.get(email = Email_address)
    return render(request, 'contact_page/individual.html', {
        'result':result
    })


def schedule_a_meeting(request):
    #Here the first_name, last_name, and the email refer to that of the host
    now = tz.now().date()
    time_now = now.strftime('%H:%M')
    date_now = now.strftime('%d/%m/%y')
    if request.method == 'GET':
        firstname, lastname, email = request.GET.get('host_first_name'),  request.GET.get('host_last_name'), request.GET.get('host_email') 
        return render(request, 'contact_page/schedule.html', {
            'host_first_name':firstname,
            'host_last_name':lastname,
            'host_email':email,
            'visitor_form':VisitorForm(),
            'meeting_form':MeetingForm(),
            'today': date_now,
            'now':time_now,
        })
    elif request.method == 'POST':
        redirect = False
        new_visitor = None
        visitor_exists = False
        form1 = VisitorForm(request.POST)
        form2 = MeetingForm(request.POST)
        visitor_email = request.POST['email']
        if len(Visitor.objects.filter(email = visitor_email)) == 0 :
            if form1.is_valid():
                visitor_first_name = form1.cleaned_data.get('first_name')
                visitor_last_name = form1.cleaned_data.get('last_name')
                visitor_phone_number = form1.cleaned_data.get('phone_number')
                new_visitor = Visitor(first_name = visitor_first_name, last_name = visitor_last_name, email = visitor_email, phone_number = visitor_phone_number)
                new_visitor.save()
                visitor_exists = True
            else:
                redirect = True
        else:
            new_visitor = Visitor.objects.filter(email = visitor_email).first()
            visitor_exists = True
            print('Visitor exists')
        if not redirect and form2.is_valid():
            host_email = request.POST['host_email']
            intended_host = Host.objects.get(email = host_email)
            Meeting_date = form2.cleaned_data.get('meeting_date')
            Meeting_begin = form2.cleaned_data.get('meeting_begin')
            Meeting_end = form2.cleaned_data.get('meeting_end')
            Meeting_location = form2.cleaned_data.get('location')
            token_input = intended_host.email + new_visitor.first_name + Meeting_date.strftime('%d/%M/%Y') + Meeting_end.strftime('%H:%M')
            Token = tokengenerator(token_input)
            new_meeting = Meeting(host = intended_host, visitor = new_visitor, meeting_date = Meeting_date, meeting_begin = Meeting_begin, meeting_end = Meeting_end, location = Meeting_location, token = Token)
            new_meeting.save()
            return render(request, 'contact_page/success.html', {'message':'Your meeting was registered successfully', 'meeting_token':Token})
        redirect = True
        message = 'Invalid data: '
        if not form1.is_valid() and not visitor_exists:
            message += 'Your personal data is invalid. '
        if not form2.is_valid():
            message += 'The meeting details are invalid. '
        return render(request, 'contact_page/schedule.html', {
            'host_first_name':request.POST['host_first_name'],
            'host_last_name':request.POST['host_last_name'],
            'host_email':request.POST['host_email'],
            'visitor_form':form1,
            'meeting_form': form2,
            'today': date_now,
            'now':time_now,
            'message': message,
            'visitor_exists':visitor_exists
        })
    else:
        return HttpResponseRedirect(reverse('contact_page:welcome'))

def followup(request):
    def consisentency_check(host_last_name, visitor_last_name, meeting):
        first = host_last_name == meeting.host.last_name
        print(f"meeting.host.last_name = {meeting.host.last_name}")
        second = visitor_last_name == meeting.visitor.last_name
        print(f"meeting.host.last_name = {meeting.visitor.last_name}")
        return first and second

    if request.method == 'GET':
        return render(request, 'contact_page/followup.html', {
            'form' : LookUpForm()
        })
    elif request.method == 'POST':
        meeting_details = {}
        meeting_token = request.POST['meeting_token']
        host_last_name = request.POST['host_last_name']
        visitor_last_name = request.POST['visitor_last_name']
        possibilities = Meeting.objects.filter(token = meeting_token)
        for meeting in possibilities:
            if consisentency_check(host_last_name, visitor_last_name, meeting):
                    meeting_details = {
                        1:{
                            'category':'fixed',
                            'label':'Host Name',
                            'value' : meeting.host.first_name + " "+ meeting.host.last_name
                        },
                        2:{
                            'category':'fixed',
                            'label':'Visitor Name',
                            'value': meeting.visitor.first_name + " " + meeting.visitor.last_name
                        },
                        3:{
                            'label':'Meeting Date',
                            'category':'input',
                            'name':'meeting_date',
                            'placeholder': meeting.meeting_date.strftime('%d/%m/%Y'),
                            'type':'date'
                        },
                        4:{
                            'label':'Start time',
                            'category':'input',
                            'name':'meeting_begin',
                            'placeholder':meeting.meeting_begin.strftime('%H:%M'),
                            'type':'time'
                        },
                        5:{
                            'label':'End time',
                            'category':'input',
                            'name':'meeting_end',
                            'placeholder': meeting.meeting_end.strftime('%H:%M'),
                            'type':'time'
                        },
                        6:{
                            'label':'Meeting Location',
                            'category':'input',
                            'name':'location',
                            'placeholder':meeting.location,
                            'type':'textarea'
                        },
                        7:{
                            'label':'Status',
                            'category':'determining',
                            'placeholder':meeting.fixed 
                        },
                        8:{
                            'name':'token',
                            'category':'hidden',
                            'value':meeting.token
                        }
                    }
        print(dumps(meeting_details))
        return render(request, 'contact_page/followup.html', {
            'result': True,
            'meeting' : dumps(meeting_details)
        })
        
    else:
        return HttpResponseRedirect(reverse('contact_page:welcome'))

def update(request):
    start = request.POST['meeting_begin']
    end = request.POST['meeting_end']
    location = request.POST['location']
    date = request.POST['meeting_date']
    token = request.POST['token']
    the_meeting = Meeting.objects.get(token = token)
    the_meeting.meeting_begin = start
    the_meeting.meeting_end = end
    the_meeting.location = location
    the_meeting.date = date
    the_meeting.save()
    return render(request, 'contact_page/success.html', {'message':'The meeting details were updated successfully'})

