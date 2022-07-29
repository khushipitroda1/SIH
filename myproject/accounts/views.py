from django.shortcuts import render, redirect

# from myproject.web_scraper import web_scrapping
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate
import random
from django.contrib.auth.hashers import check_password
from django.views.decorators.cache import cache_control
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Create your views here.
tokenizer = Tokenizer()
maxlen = 1000

def submitnewsfromuser(request):
    if request.method == "POST":
        text1 = request.POST.get('text1')
        text2 = tokenizer.texts_to_sequences(text1)
        text2 = pad_sequences(text2, maxlen=maxlen)
        model = load_model('model\lstm_0001.h5')
        res = (model.predict(text2)>=0.5)[0][0]
        print(res)
    return render(request,'app/userside.html',{'res':res, 'text1':text1})


def userside(request):
    return render(request, 'app/userside.html')

def submitreport(request):
    return render(request, 'app/submittedreport.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if request.session.get('vendor') == None:
        return redirect('login')
    return render(request, 'app/home.html')


def target(request):
    if request.session.get('vendor') == None:
        return redirect('login')

    if request.method == "POST":
        url1 = request.POST.get('url1','')
        url2 = request.POST.get('url2','')
        url3 = request.POST.get('url3','')
    
        print(url1,url2,url3)

    return render(request, 'app/target.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):

    department = ['health', 'political', 'education', 'tourism', 'sports']

    if request.session.get('vendor') != None:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST['email']
        pwd = request.POST['password']
        dname = request.POST['dname']

        usr = authenticate(email=email,password=pwd)
        if usr:
            usr = CustomUser.objects.get(email=email)
            if usr.user_type == dname :
                if (usr.is_staff == True):
                    vendor = {'vendor_name':usr.username,'vendor_email':usr.email}
                    request.session['vendor'] = vendor
                    request.session['vendor_email'] = usr.email
                    return redirect('home')
                else:                
                    return render(request,'app/login.html',{'department':department})
            else:
                msg = "Incorrect Details!!!"
                return render(request,'app/login.html',{'msg':msg,'department':department})
        else:
            msg = "Incorrect Email or Password!!!"
            return render(request,'app/login.html',{'msg':msg,'department':department})
    
    return render(request,'app/login.html',{'department':department})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    if (request.session.get('vendor') != None):
        request.session.delete()
    else:
        return redirect('login')

    return render(request,'app/logout.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        is_email = CustomUser.objects.filter(email__iexact=email).exists()
        if is_email:
            OTP = random.randint(111111,999999)
            subject = "Password Reset OTP @apparel_vendor"
            message = "Your OTP is, " + str(OTP) + " .Please Follow This Link, --> http://127.0.0.1:8000/otp_verify"
            email_from = settings.EMAIL_HOST_USER
            email_to = [email, ]
            send_mail(subject, message, email_from, email_to)

            # OTP and email set In Session
            request.session["reset_password_OTP"] = OTP
            request.session["reset_password_EMAIL"] = email
            return redirect('otp_sent')
        else:
            msg = "Incorrect Email!!!"
            return render(request,'app/forgot_password.html',{'msg':msg})

    return render(request,'app/forgot_password.html')


def otp_sent(request):
    return render(request,'app/otp_sent.html')


def otp_verify(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        session_otp = request.session.get('reset_password_OTP')
        if str(otp) == str(session_otp):
            return redirect('reset_password')
        else:
            msg = "Invalid OTP!!!"
            return render(request,'app/otp_verification.html',{'msg':msg})

    return render(request,'app/otp_verification.html')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password1']
        c_password = request.POST['password2']

        if password == c_password:
            email = request.session.get('reset_password_EMAIL')
            usr = CustomUser.objects.get(email=email)
            usr.set_password(password)
            usr.save()
            request.session.delete()
            return redirect('login')
        else:
            msg = "Password are not matched!!!"
            return render(request,'app/reset_password.html',{'msg':msg})

    return render(request,'app/reset_password.html')


def change_password(request):
    if request.session.get('vendor') == None:
        return redirect('login')

    elif request.method == 'POST':
        old = request.POST['password']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        if pass1 == pass2:
            if 'vendor' in request.session:
                email = request.session.get('vendor_email')

                usr = CustomUser.objects.get(email__iexact=email)
                if old != pass1:
                    if check_password(old,usr.password):
                        usr.set_password(pass1)
                        usr.save()
                        request.session.delete()
                        return redirect('login')
                else:
                    msg = "Old password and new password are same!!!"
                    return render(request,'app/change_password.html',{'msg':msg})
        else:
                msg = "Password are not matched!!!"
                return render(request,'app/change_password.html',{'msg':msg})

    return render(request,'app/change_password.html')




######### Web Scrapping

from apscheduler.schedulers.background import BackgroundScheduler
from web_scraper import web_scrapping

scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
scheduler.start()

# scheduler.add_job(web_scrapping, 'interval', seconds= 3600)

# web_scrapping()



# *********** Crawler ********

from crawler import crawler

crawler()


