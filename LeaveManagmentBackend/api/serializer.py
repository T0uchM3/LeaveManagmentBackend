from rest_framework import serializers
from .models import CustomUser, Leave



class LeaveSerializer(serializers.Serializer):
       startdate = serializers.DateTimeField()
       enddate = serializers.DateTimeField()
       leavetype = serializers.CharField()
       days = serializers.IntegerField()
       reason = serializers.CharField()

       def create(self, validated_data):
           return Leave.objects.create(**validated_data)

class CustomUserSerializer(serializers.ModelSerializer):
      class Meta:
        model = CustomUser
        fields = ('username','userfirstname', 'userlastname', 'email', 
                  'password', 'is_admin', 'gender', 'paternity', 'maternity', 'paid', 'rtt')

