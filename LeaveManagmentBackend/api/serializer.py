from rest_framework import serializers
from .models import Input, CustomUser, Leave



class InputSerializerPOST(serializers.Serializer):
       temperature = serializers.FloatField()
       humidity = serializers.FloatField()
       water = serializers.FloatField()
       def create(self, validated_data):
           return Input.objects.create(**validated_data)

class InputSerializerGET(serializers.Serializer):
       temperature = serializers.FloatField()
       humidity = serializers.FloatField()
       water = serializers.FloatField()
       created_at = serializers.DateTimeField()
       def create(self, validated_data):
           return Input.objects.create(**validated_data)


class LeaveSerializer(serializers.Serializer):
       startdate = serializers.DateTimeField()
       enddate = serializers.DateTimeField()
       paternity = serializers.IntegerField()
       maternity = serializers.IntegerField()
       paid = serializers.IntegerField()
       rtt = serializers.IntegerField()
       reason = serializers.CharField()

       def create(self, validated_data):
           return Leave.objects.create(**validated_data)

class CustomUserSerializer(serializers.ModelSerializer):
      class Meta:
        model = CustomUser
        fields = ('username','userfirstname', 'userlastname', 'email', 
                  'password', 'is_admin', 'leaveid', 'gender')

