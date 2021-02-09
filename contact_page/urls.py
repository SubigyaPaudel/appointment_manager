from django.urls import path
from . import views
from . import internal_views

app_name = "contact_page"
urlpatterns = [
    path("", views.welcome, name="welcome"),
    path('login/<str:redirect>/<str:destination>', views.hostlogin, name="hostLogin"),
    path("signup/", views.signup, name="signup"),
    path('logout/', views.hostlogout, name = 'logout'),
    path('welcome', internal_views.inside, name='inside'),
    path('search/', views.search, name = 'search'),
    path('autocomplete_util/', views.autocomplete, name = "autocomplete"),
    path('search_results/', views.search_results, name = 'search_results'),
    path('search_results_further/', views.search_further, name = 'further_search'),
    path('schedule/', views.schedule_a_meeting, name='schedule'),
    path('followup/', views.followup, name = 'followup'),
    path('update/', views.update, name = 'update'),
    path('personal_data/', internal_views.personal_data, name = 'personal_data'),
    path('inside/', internal_views.inside, name = 'inside'),
    path('get_fixed_meetings/', internal_views.get_fixed_meetings, name = 'get_fixed_meetings'),
    path('get_ignored_meetings/', internal_views.get_ignored_meetings, name = 'get_ignored_meetings'),
    path('ignore_meeting/<str:token>',internal_views.ignore_meeting, name = 'ignore_meeting'),
    path('confirm_meeting/<str:token>', internal_views.confirm_meeting, name = 'confirm_meeting'),
    path('modify_host_data/', internal_views.modify_host_data, name = 'modify_host_data'),
    path('change_password/', internal_views.ChangePassword.as_view(), name = 'change_password'),
    path('password_reset/', internal_views.PasswordDone.as_view(), name = 'password_done')
]