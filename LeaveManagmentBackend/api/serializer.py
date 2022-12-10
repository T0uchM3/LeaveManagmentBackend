from rest_framework import serializers
from .models import CustomUser, Leave



class LeaveSerializer(serializers.ModelSerializer):
       startdate = serializers.DateTimeField()
       enddate = serializers.DateTimeField()
       leavetype = serializers.CharField()
       days = serializers.IntegerField()
       userid = serializers.IntegerField()
       status = serializers.CharField()
       def create(self, validated_data):
           return Leave.objects.create(**validated_data)
       class Meta:
        model = Leave
        fields = ('startdate','enddate', 'leavetype', 'days', 'userid', 'status')
class CustomUserSerializer(serializers.ModelSerializer):
      class Meta:
        model = CustomUser
        fields = ('username','userfirstname', 'userlastname', 'email', 'password', 'is_admin', 'gender', 'paternity', 'maternity', 'paid', 'rtt')

