from django.urls import path
from accounts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.userside,name='userside'),
    path('home/',views.home,name='home'),
    path('target/',views.target,name='target'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('otp_sent/',views.otp_sent,name='otp_sent'),
    path('otp_verify/',views.otp_verify,name='otp_verify'),
    path('reset_password/',views.reset_password,name='reset_password'),
    path('change_password/',views.change_password,name='change_password'),

    path('submitreport/',views.submitreport,name='submitreport'),

    path('submitnewsfromuser/',views.submitnewsfromuser,name='submitnewsfromuser'),
]
# ]+ static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
