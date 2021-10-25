from .models import *
from rest_framework import serializers
from django.core.serializers import serialize
from django.core.files.base import ContentFile
import base64
import six
import uuid
from .modules.hashutils import make_pw_hash
from .modules.functions import get_random_string
from django.http import Http404, JsonResponse
import json


class RoleField(serializers.RelatedField):
    queryset = Role.objects.all()
    def to_representation(self, value):
        return value.name
    def to_internal_value(self, data):
        try:
            try:
                return Role.objects.get(name=data)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )

class RoleSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Role
        fields = ("id", "name")


class MyImageSerializer(serializers.ModelSerializer):    
    class Meta:
        model = MyImage
        fields = ("id", "image")

class MyImageField(serializers.RelatedField):
    queryset = MyImage.objects.all()
    def to_representation(self, value):
        return value.id
    def to_internal_value(self, data):
        try:
            try:
                return MyImage.objects.get(id=data)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )

class FriendSerializer(serializers.ModelSerializer):
    role = RoleField(many=False, read_only=False)
    class Meta:
        model = User
        fields = ("id", "role", "phone", "avatar", "ref_code", "bonuses", "trains_count", "avarage_train_time", "max_train_time", "most_visited_club")

class UserSerializer(serializers.ModelSerializer):
    role = RoleField(many=False, read_only=False)
    friends = FriendSerializer(many=True, read_only=False)
    class Meta:
        model = User
        fields = ("id", "role", "phone", "avatar", "ref_code", "bonuses", "trains_count", "avarage_train_time", "max_train_time", "most_visited_club", "friends")
    
    def create(self, validated_data):
        try:
            user = User.objects.filter(phone=validated_data["phone"]).first()
            if user:
                raise Exception
            
        except:
            raise serializers.ValidationError("User alredy exist")
        user = User.objects.create(
            role=validated_data['role'],
            phone=validated_data['phone'],
        )
        user.generate_ref_code()
        user.save()
        return user

 
class UserField(serializers.RelatedField):    
    queryset = User.objects.all()
    def to_representation(self, value):
        return value.id
    def to_internal_value(self, data):
        try:
            try:
                return User.objects.get(id=int(data))
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )




class ScheduleField(serializers.RelatedField):
    queryset = Schedule.objects.all()
    def to_representation(self, value):
        return value.id
    def to_internal_value(self, data):
        try:
            try:
                return Schedule.objects.get(id=data)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )

class TimeLineSerializer(serializers.ModelSerializer):     
    class Meta:
        model = TimeLine
        fields = ("id", "price", "limit_people", "start_time", "end_time")

class ScheduleSerializer(serializers.ModelSerializer):    
    timelines = TimeLineSerializer(many=True, read_only=False, required=False)
    class Meta:
        model = Schedule
        fields = ("id", "day", "get_cutted_name", "get_fullname", "timelines")


class ServiceField(serializers.RelatedField):
    queryset = Service.objects.all()
    def to_representation(self, value):
        return value.id
    def to_internal_value(self, data):
        try:
            try:
                return Service.objects.get(id=data)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )

class ServiceCategoryField(serializers.RelatedField):
    queryset = ServiceCategory.objects.all()
    def to_representation(self, value):
        return value.name
    def to_internal_value(self, data):
        try:
            try:
                return ServiceCategory.objects.get(name=data)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )

class ServiceCategorySerializer(serializers.ModelSerializer):    
    class Meta:
        model = ServiceCategory
        fields = ("id", "name", "amount_of_services")

class ServiceSerializer(serializers.ModelSerializer):    
    #days = ScheduleSerializer(many=True, read_only=False, required=False, )
    days = serializers.SerializerMethodField("get_days")
    images = MyImageSerializer(many=True, read_only=False, required=False)
    category = ServiceCategoryField(many=False, read_only=False, required=False)

    def get_days(self, instance):
        days = instance.days.all().order_by("day")
        return ScheduleSerializer(days, many=True, read_only=-False, required=False).data

    class Meta:
        model = Service
        fields = ("id", "category", "description", "days", "images")
    
    def create(self, validated_data):   
        service = Service.objects.create(**validated_data)
        days_list = [] 
        for count in range(0,7):                    
            days_list.append(Schedule.objects.create(day=count))
        service.days.add(*days_list)
        return service

class CompanySerializer(serializers.ModelSerializer):    
    owner = UserField(many=False, read_only=False)
    services = ServiceSerializer(many=True, read_only=False, required=False)
    class Meta:
        model = Company
        fields = [ "id", "name", "owner", "address", "latitude", "longitude", "services", "qr_url", "description"]

    def create(self, validated_data):
        company = Company.objects.create(
            name=validated_data['name'],
            owner=validated_data['owner'],
            address= validated_data['address'],
            latitude= validated_data['latitude'],
            longitude= validated_data['longitude'],
            )
        try:
            services = validated_data['services']
            company.services.set(services)
        except:
            pass
            
        company.qr_url = qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=" + str(company.id)
        company.save()
    
        return company

class CompanyField(serializers.RelatedField):
    queryset = Company.objects.all()
    def to_representation(self, value):
        return value.name
    def to_internal_value(self, data):
        try:
            try:
                return Company.objects.get(name=data)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )

class FinishedTrainSerializer(serializers.ModelSerializer):    
    user = UserField(many=False, read_only=False)
    service = ServiceField(many=False, read_only=False)
    company = CompanyField(many=False, read_only=False)
    class Meta:
        model = FinishedTrain
        fields = ("id", "user", "company", "service", "minutes", "start_time", "end_time", "bill")

class TimerSerializer(serializers.ModelSerializer):    
    user = UserField(many=False, read_only=False)
    service = ServiceField(many=False, read_only=False)
    company = CompanyField(many=False, read_only=False)
    class Meta:
        model = Timer
        fields = ("id", "user", "company", "service", "start_time", "end_time", "is_confirmed", "delete_after_expired")

class TrainTimerSerializer(serializers.ModelSerializer):    
    user = UserField(many=False, read_only=False)
    service = ServiceField(many=False, read_only=False)
    company = CompanyField(many=False, read_only=False)
    class Meta:
        model = TrainTimer
        fields = ("id", "user", "company", "service", "start_time", "end_time", "minutes")