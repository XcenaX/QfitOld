from django.shortcuts import render

#from .forms import UserForm, CommentForm, BlogForm
from api.models import *
from adminpanel.models import *

from django.shortcuts import redirect
from django.urls import reverse

#from .modules.hashutils import check_pw_hash, make_pw_hash

#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.utils import timezone

#import smtplib, ssl

#from .modules.sendEmail import send_email
import itertools
from django.http import HttpResponse, JsonResponse, Http404

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
#from .tokens import account_activation_token
#from django.core.mail import EmailMessage
from django import template
import os
from django.conf import settings

from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

from adminpanel.modules.functions import *
from api.modules.hashutils import check_pw_hash, make_pw_hash
from adminpanel.modules.functions import get_current_user

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        users = AdminUser.objects.filter(username=username)
        if len(users) == 0:
            return render(request, "login.html", {
                "error": "Неверное имя пользователя!",
                "companies": Company.objects.all()
            })
        user = users.first()
        #if check_pw_hash(password, user.password):
        if password == user.password:
            request.session["user"] = user.id
            request.session["company"] = user.company.id
            return redirect(reverse("adminpanel:index"))
        return render(request, "login.html", {
            "error": "Неверный логин или пароль!",
            "companies": Company.objects.all()
        })
    return render(request, "login.html", {
        "companies": Company.objects.all()
    })

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        company_id = request.POST["company"]
        company = Company.objects.get(id=company_id)
        users = AdminUser.objects.filter(username=username) 
        if len(users) > 0:
            return JsonResponse({"error": "Already exist"})
        
        hash_password = make_pw_hash(password)
        
        current_user = AdminUser.objects.create(username=username, password=hash_password, company=company)
        current_user.save()
        
        return redirect(reverse("adminpanel:login"))    
               
    return render(request, "login.html", {
        "success": "NICE"
    })

def index(request):
    current_user = get_current_user(request)
    if not current_user:
        return redirect(reverse("adminpanel:login"))
    train_timers = TrainTimer.objects.filter(company=current_user.company)
    if not current_user:
        return redirect(reverse("adminpanel:login"))
    return render(request, "index.html", {
        "timers": train_timers,
        "company": current_user.company,
        "current_user": current_user,
    })

def support(request):
    current_user = get_current_user(request)
    if not current_user:
        return redirect(reverse("adminpanel:login"))
    return render(request, "support.html", {
        "current_user": current_user,
        "company": current_user.company,
    })

def services(request):
    user = get_current_user(request)
    if not user:
        return redirect(reverse("adminpanel:login"))
    company = user.company
    services = company.services.all()
    service_categories = ServiceCategory.objects.all()
    return render(request, "services.html", {
        "current_user": user,
        "company": company,
        "services": services,
        "days_of_week": DAYS_OF_WEEK,
        "service_categories": service_categories,
    })

def book(request):
    current_timers = Timer.objects.filter(is_confirmed=False)
    accepted_timers = Timer.objects.filter(is_confirmed=True)
    current_user = get_current_user(request)
    if not current_user:
        return redirect(reverse("adminpanel:login"))
    return render(request, "book.html", {
        "current_timers": current_timers,
        "accepted_timers": accepted_timers,
        "current_user": current_user,
        "company": current_user.company,
    })

def history(request):
    current_user = get_current_user(request)
    if not current_user:
        return redirect(reverse("adminpanel:login"))
    histories = FinishedTrain.objects.filter(company=current_user.company).order_by("-start_time")
    return render(request, "history.html", {
        "histories": histories,
        "current_user": current_user,
        "company": current_user.company,
    })

def logout(request): # Пока без выхода
    if request.method == "POST":
        del request.session["user"]
        return redirect(reverse("adminpanel:login"))