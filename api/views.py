
from api.models import *
from rest_framework import viewsets
from api.serializers import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User as Auth_User
import secrets
from django.shortcuts import render
from django.core.files import File
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from qfit.settings import BASE_DIR

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from urllib.request import urlopen

from django.template.loader import render_to_string

import requests

from rest_framework.permissions import AllowAny

#from .filters import FoundItemFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from django.views.decorators.csrf import csrf_exempt

from tempfile import NamedTemporaryFile
import mimetypes

from api.modules.sendEmail import send_email

from django.http import HttpResponse, FileResponse

from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from datetime import timedelta
from datetime import datetime, date
API_KEY = "AIzaSyCcHCB9lx35nurrIOy2KvphPIvmsflB4mE"

from adminpanel.modules.functions import broadcast_ticks, get_current_user
from .modules.functions import check_image_type, check_timelines, send_sms

LIMIT_FRIENDS = 2

#import googlemaps

# import mysql.connector
# from mysql.connector import Error
# import shutil

from .modules.hashutils import check_pw_hash, make_pw_hash

import threading

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class CompanyViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["name", "services"]
    #authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def retrieve(self, request, pk=None):
        queryset = Company.objects.all()
        try:
            item = Company.objects.get(id=pk)
            serializer = CompanySerializer(item)
            return Response(serializer.data)
        except:
            raise Http404


class UserViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["phone", "role", "ref_code", "bonuses"]
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        try:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except:
            raise Http404


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = (IsAuthenticated,)
    def retrieve(self, request, pk=None):
        queryset = Role.objects.all()
        try:
            role = Role.objects.get(id=pk)
            serializer = RoleSerializer(role)
            return Response(serializer.data)
        except:
            raise Http404


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = (IsAuthenticated,)
    def retrieve(self, request, pk=None):
        queryset = Schedule.objects.all()
        try:
            schedule = Schedule.objects.get(id=pk)
            serializer = ScheduleSerializer(schedule)
            return Response(serializer.data)
        except:
            raise Http404

class ServiceViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["category__name", "id"]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = (IsAuthenticated,)
    def retrieve(self, request, pk=None):
        queryset = Service.objects.all()
        try:
            service = Service.objects.get(id=pk)
            serializer = ServiceSerializer(service)
            return Response(serializer.data)
        except:
            raise Http404

class FinishedTrainViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["company", "service", "user", "start_time", "end_time"]
    permission_classes = (IsAuthenticated,)
    queryset = FinishedTrain.objects.all()
    serializer_class = FinishedTrainSerializer

    def retrieve(self, request, pk=None):
        queryset = FinishedTrain.objects.all()
        try:
            item = FinishedTrain.objects.get(id=pk)
            serializer = FinishedTrainSerializer(item)
            return Response(serializer.data)
        except:
            raise Http404

class MyImageViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = MyImage.objects.all()
    serializer_class = MyImageSerializer

    def retrieve(self, request, pk=None):
        queryset = MyImage.objects.all()
        try:
            item = MyImage.objects.get(id=pk)
            serializer = MyImageSerializer(item)
            return Response(serializer.data)
        except:
            raise Http404
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

class TimeLineViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = TimeLine.objects.all()
    serializer_class = TimeLineSerializer

    def retrieve(self, request, pk=None):
        queryset = TimeLine.objects.all()
        try:
            item = TimeLine.objects.get(id=pk)
            serializer = TimeLineSerializer(item)
            return Response(serializer.data)
        except:
            raise Http404

class TimerViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["company", "service", "user", "start_time"]
    queryset = Timer.objects.all()
    serializer_class = TimerSerializer

    def retrieve(self, request, pk=None):
        queryset = Timer.objects.all()
        try:
            item = Timer.objects.get(id=pk)
            serializer = TimerSerializer(item)
            return Response(serializer.data)
        except:
            raise Http404

class TrainTimerViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = TrainTimer.objects.all()
    serializer_class = TrainTimerSerializer

    def retrieve(self, request, pk=None):
        queryset = TrainTimer.objects.all()
        try:
            item = TrainTimer.objects.get(id=pk)
            serializer = TrainTimerSerializer(item)
            return Response(serializer.data)
        except:
            raise Http404

class ServiceCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer

    def retrieve(self, request, pk=None):
        queryset = ServiceCategory.objects.all()
        try:
            item = ServiceCategory.objects.get(id=pk)
            serializer = ServiceCategorySerializer(item)
            return Response(serializer.data)
        except:
            raise Http404

class DownloadFile(APIView):
    def get(self, request):
        fl_path = '/file/path'
        filename = 'downloaded_file_name.extension'

        fl = open(fl_path, 'r')
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response


class AddFriend(APIView):
    permission_classes = (IsAuthenticated,)  

    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})

    def post(self, request):
        current_user_id = int(request.POST["current_user"])
        code = int(request.POST["code"])
        current_user = User.objects.filter(id=current_user_id)
        if len(current_user) == 0:
            return Response({"error": "User with this id nit found!"})
        current_user = current_user.first()
        friend = User.objects.filter(ref_code=code)
        if len(friend) == 0:
            return Response({"error": "User with this REF CODE nit found!"})
        friend = friend.first()

        current_user.friends.add(friend)
        friend.friends.add(current_user)
        
        current_user.save()
        friend.save()
        
        return Response({"success": True}) 

class SendCode(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        phone = None
        code_type = None
        try:
            phone = request.POST["phone"]
            code_type = request.POST["code_type"] # Либо login либо register
        except:
            return Response({"error": "Не передан один из параметров: phone, code_type"})
        message = None
        if code_type == "register":
            if len(User.objects.filter(phone=phone)) > 0:
                return Response({"error": "Пользователь с таким телефоном уже существует!"})
            message = "Ваш код для регистрации в QFIT: "
        elif code_type == "login":
            if len(User.objects.filter(phone=phone)) == 0:
                return Response({"error": "Телефон не найден!"})
            message = "Ваш код для входа в QFIT: "
        else:
            return Response({"error": "Нужно передать параметр code_type. Это либо login либо register"})
        # Выслать код
        another_verification = VerificationPhone.objects.filter(phone=phone).first()
        if another_verification:
            another_verification.delete()

        verification_phone = VerificationPhone.objects.create(phone=phone)
        verification_phone.generate_code()
        
        message += verification_phone.code
        send_sms(phone, message)
        return Response({"success": True})

class CheckCode(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        code = None
        phone = None
        code_type = None
        try:
            code = int(request.POST["code"])
            phone = request.POST["phone"]
            code_type = request.POST["code_type"]
        except:
            return Response({"error": "Не передан один из параметров: code, phone, code_type"})
        
        verification_phone = VerificationPhone.objects.filter(phone=phone, code=code).first()
        if not verification_phone:
            return Response({"error": "Неправильный код!"})
        verification_phone.delete()
        user = User.objects.filter(phone=phone).first()
        if code_type == "login":
            return Response({"success": True, "user":{
                "id": user.id,
                "phone": user.phone,
                "role": user.role.name,
                "avatar": user.avatar.url,
                "ref_code": user.ref_code,
                "bonuses": user.bonuses,
                "email": user.email,
                "name": user.name,
                "sex": user.sex
            }})
        elif code_type == "register":
            return Response({"success": True})    
        
        
            

class Register(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        phone = None
        name = None
        email = None
        sex = None
        try:
            phone = request.POST["phone"]
            name = request.POST["name"]
            email = request.POST["email"]
            sex = request.POST["sex"]
        except:
            return Response({"error": "Не передан один из параметров: name, email, sex, phone"})
        
        user = User.objects.create(phone=phone, name=name, email=email, sex=sex)
        user.save()
        return Response({"success": True, "user":{
            "id": user.id,
            "phone": user.phone,
            "ref_code": user.ref_code,
            "bonuses": user.bonuses,
            "email": user.email,
            "name": user.name,
            "sex": user.sex
        }})

class BookTime(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        user_id = int(request.POST["user_id"])
        company_id = int(request.POST["company_id"])
        service_id = int(request.POST["service_id"])
        book_time = request.POST["book_time"]
        date_book_time = datetime.strptime(book_time, '%d-%m-%Y %H:%M')
        
        user = User.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({"error": "Not authorized!"})
        
        company = Company.objects.filter(id=company_id).first()
        if not company:
            return JsonResponse({"error": "Company not exist!"})

        services = company.services.all()
        service = None
        has_places = False
        for current_service in services:
            for day in current_service.days.all():
                if int(day.day) == date_book_time.weekday():
                    for timeline in day.timelines.all():
                        if timeline.start_time <= date_book_time.time() and timeline.end_time > date_book_time.time():
                            has_places = True
                            service = current_service
                            break

        if not has_places:
            return JsonResponse({"error": "В это время по этой услуге заниматься нельзя!"})   
        
        timer = Timer.objects.create(user=user,company=company, service=service, end_time=date_book_time + timedelta(minutes=20), start_time=date_book_time)
        timer.save()
        
        broadcast_ticks({
            "new_book": True,
            "timer_id": timer.id,
            "timer_start": str(timer.start_time),
            "timer_end": str(timer.end_time),
            "timer_service": timer.service.category.name,
            "timer_user": timer.user.phone,
            "company_id": timer.company.id,
        })
        return JsonResponse({"success": "Company was booked!"})

class ConfirmBoook(APIView):
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        user_id = int(request.POST["user_id"])
        company_id = int(request.POST["company_id"])
        current_time = request.POST["current_time"]
        date_current_time = datetime.strptime(current_time, '%d-%m-%Y %H:%M')
        
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({"error": "Not authorized!"})
        
        company = Company.objects.filter(id=company_id).first()
        if not company:
            return Response({"error": "Company not exist!"})
        
        book_timers = Timer.objects.filter(user=user, company=company)
        book_timer = None
        for timer in book_timers:
            if(timer.start_time - timedelta(minutes=10) <= date_current_time and timer.end_time > date_current_time):
                book_timer = timer
                break
        
        if not book_timer:
            if(len(book_timers) > 0):
                return Response({"error": "Вы сможете подтвердить бронь только в " + str(book_timers[0].start_time - timedelta(minutes=10))})
            else:
                return Response({"error": "Бронь не найдена!"})
        elif not book_timer.is_confirmed:
            return Response({"error": "Ваша бронь не подтверждена!"})
        else:
            timer = TrainTimer.objects.create(user=user,company=company, service=book_timer.service, start_time=date_current_time)
            timer.save()
            book_timer.delete()
            #book_timer.delete()
            
            broadcast_ticks({
                "new_timer": True,
                "timer_id": timer.id,
                "timer_start": str(timer.start_time),
                "timer_service": timer.service.category.name,
                "timer_user": timer.user.phone,
                "company_id": timer.company.id,
            })
            return Response({"success": "Тренировка началась!"})

class AcceptBook(APIView):
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        timer_id = int(request.POST["timer_id"])
        timer = Timer.objects.filter(id=timer_id).first() 
        if not timer:
            return Response({"success": "Такой брони уже не существует!"})     
        timer.is_confirmed = True
        timer.save()
        broadcast_ticks({
            "company_id": timer.company.id,
            "accept_book": True,
            "service": timer.service.category.name,
            "start_time": str(timer.start_time),
            "end_time": str(timer.end_time),
            "user": timer.user.phone,
            "timer_id": timer_id,
        })
        return Response({"success": "Бронь подтверждена!"})

class DeclineBook(APIView):
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        timer_id = int(request.POST["timer_id"])
        timer = Timer.objects.filter(id=timer_id).first() 
        timer.delete()
        broadcast_ticks({
            "company_id": timer.company.id,
            "decline_book": True,
            "timer_id": timer_id,
        })
        return Response({"success": "Бронь подтверждена!"})

class EndTrain(APIView):
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        user_id = int(request.POST["user_id"])
        company_id = int(request.POST["company_id"])
        current_time_str = request.POST["end_time"]
        if len(current_time_str) == 16:
            current_time_str += ":00"
        current_time = datetime.strptime(current_time_str, '%d-%m-%Y %H:%M:%S')
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({"error": "Not authorized!"})
        
        company = Company.objects.filter(id=company_id).first()
        if not company:
            return Response({"error": "Company not exist!"})
        
        train_timer = TrainTimer.objects.filter(user=user, company=company).first()
        minutes = (current_time - train_timer.start_time).seconds//60
        
        price = minutes * train_timer.service.get_price(train_timer.start_time.weekday(), train_timer.start_time)
        if price < 0:
            return Response({"error": "Цена бля!"})
        finished_train = FinishedTrain.objects.create(start_time=train_timer.start_time, end_time=current_time, user=user, company=company, service=train_timer.service, minutes=minutes, bill=price)
        finished_train.save()
        train_timer.delete()
        broadcast_ticks({
            "new_history": True,
            "phone": finished_train.user.phone,
            "service": finished_train.service.category.name,
            "start_time": str(finished_train.start_time),
            "end_time": str(finished_train.end_time),
            "minutes": minutes,
            "bill": finished_train.bill,
            "history_id": finished_train.id,
        })
        
        return Response({"success": "Тренировка окончена!", "bill": price})

class GetMinutes(APIView):
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        current_time_str = request.POST["current_time"]
        
        if len(current_time_str) == 16:
            current_time_str += ":10"
        current_time = datetime.strptime(current_time_str, '%d-%m-%Y %H:%M:%S')
        train_timer_id = request.POST["timer_id"]
        train_timer = TrainTimer.objects.filter(id=int(train_timer_id)).first()
        if not train_timer:
            return Response({"error": "Train timer with ID " + train_timer_id + " not found!"})
        minutes = (current_time - train_timer.start_time).seconds//60
        return Response({"minutes": minutes})

class UpdateSchedules(APIView):
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        schedules_json = request.POST["schedules"]
        schedules = json.loads(schedules_json)
        service_id = int(request.POST["service"])
        service = Service.objects.get(id=service_id)
        category_id = int(request.POST["category"])
        service.category = ServiceCategory.objects.get(id=category_id)
        service.description = request.POST["description"]
        service.save()
        if not check_timelines(schedules):
            return Response({"error": "Нельзя накладывать время занятия друг на друга!"})
        for schedule in schedules:
            current_schedule = service.days.all().filter(day=schedule["day"]).first()
            for timeline in schedule["timelines"]:
                db_timeline = TimeLine.objects.filter(id=timeline["id"]).first()
                
                if db_timeline:
                    start_time = datetime.strptime(timeline["start_time"], '%H:%M')
                    end_time = datetime.strptime(timeline["end_time"], '%H:%M')
                    
                    db_timeline.price = timeline["price"]
                    db_timeline.start_time = start_time
                    db_timeline.end_time = end_time
                    db_timeline.limit_people = timeline["limit_people"]
                    db_timeline.save()
            current_schedule.save()
        return Response({"success": "NICE BOY!"})


class AddTimeline(APIView):
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        schedule_id = request.POST["schedule"]
        schedule = Schedule.objects.get(id=schedule_id)
        
        new_timeline = TimeLine.objects.create()
        schedule.timelines.add(new_timeline)
        schedule.save()
        return Response({"id": new_timeline.id, "start_time": str(new_timeline.start_time)[:-3], "end_time": str(new_timeline.end_time)[:-3], "limit_people": new_timeline.limit_people, "price": new_timeline.price})


class AddImage(APIView):
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        image = request.FILES["image"]
        service_id = request.POST["service"]
        if(check_image_type(image)):
            model_image = MyImage.objects.create(image=image)
            model_image.save()
            service = Service.objects.get(id=service_id)
            service.images.add(model_image)
            service.save()
            return Response({"image": model_image.image.url, "id": model_image.id})
        else:
            upload_error = "Выберите .jpg или .png формат!" 
            return Response({"error": upload_error})

class AddService(APIView):
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        service_id = request.POST["service"]
        user = get_current_user(request)
        service = Service.objects.get(id=service_id)
        user.company.services.add(service)
        user.save()
        
        return Response({"success":True})

@permission_classes((AllowAny, ))
class SubmitForm(APIView):
    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})
    def post(self, request):
        club_name = request.POST["club_name"]
        description = request.POST["description"]
        city = request.POST["city"]
        #<input type="checkbox" name="has_optional_services" placeholder="Есть ли доп услуги">

        has_optional_services = request.POST["has_optional_services"]

        optional_services = request.POST["optional_services"]
        phone = request.POST["phone"]
        email = request.POST["email"]

        mail_subject = "Заявка на регистрацию клуба"
        message = render_to_string('submit_form_message.html', {
            'club_name': club_name,
            'description': description,
            'city': city,
            'has_optional_services': has_optional_services if has_optional_services else False,
            "optional_services": optional_services,
            "phone": phone,
            "email": email,
        })
        

        send_email(message, mail_subject, settings.EMAIL_HOST_USER)
        
        return Response({"success": True})



def test(request):
    return render(request, "test.html", {})


# @csrf_exempt
# def add_to_history(request):
#     if request.method == "POST":
        
        
#     return JsonResponse({"error": request.method + " method not allowed!"})


@receiver(pre_delete, sender=MyImage)
def item_delete(sender, instance, **kwargs):
    instance.image.delete(False)

# @receiver(pre_delete, sender=Document)
# def document_delete(sender, instance, **kwargs):
#     instance.image.delete(False)
