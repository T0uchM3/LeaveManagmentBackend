from pickletools import long1
from numpy import dtype
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import LeaveSerializer
from .serializer import CustomUserSerializer

from django.contrib.auth import authenticate
from .models import Leave, CustomUser

import urllib.request
import json
import cloudinary.uploader
import requests
import json
import urllib.request
import os
import numpy as np
from datetime import datetime
from rest_framework.decorators import action
from rest_framework.decorators import api_view

class AccountView(APIView):

    @staticmethod
    @api_view(['POST'])
    def addaccount(request):
        userFirstname = request.data.get('firstname')
        userLasname = request.data.get('lasname')
        userMail = request.data.get('email')
        userPassword = request.data.get('password')
        is_admin = request.data.get('is_admin')
        userGender = request.data.get('gender')


        #leave = self.createLeave(userGender)
        #print("leave ",leave)
        if(userGender == "male"):
            serializer_data = {
                    "username":userFirstname + userLasname,
                    "userfirstname":userFirstname,
                    "userlastname":userLasname,
                    "email":userMail,
                    "password":userPassword,
                    "is_admin":is_admin,
                    "gender":userGender,
                    "paternity":3,
                    "maternity":0,
                    "paid":30,
                    "rtt":0,
                    #"leaveid":leave
            }
        if(userGender == "female"):
            serializer_data = {
                    "username":userFirstname + userLasname,
                    "userfirstname":userFirstname,
                    "userlastname":userLasname,
                    "email":userMail,
                    "password":userPassword,
                    "is_admin":is_admin,
                    "gender":userGender,
                    "paternity":0,
                    "maternity":60,
                    "paid":30,
                    "rtt":0,
            }

        serializer = CustomUserSerializer(data=serializer_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response({
                'status': 'error',
                'agrs':serializer.errors,
            })
    def get(self,request):
      return Response({
                'status': 'good???',
               })
    @staticmethod
    @api_view(['POST'])
    def addleave(request):
        startDate = request.data.get("startdate")
        endtDate = request.data.get("enddate")
        leaveType = request.data.get("leavetype")
        leaveDay = request.data.get("days")
        leaveReason = request.data.get("reason")
        serializer_data = {}

        serializer_data = {
                "startdate":datetime.now(),
                "enddate":datetime.now(),
                "leavetype":leaveType,
                "days":leaveDay,
                "reason":leaveReason,
        }
 
        print(serializer_data)
        serializer = LeaveSerializer(data=serializer_data)
        if serializer.is_valid():
            serializer.save()
            print("LEAVE SAVED")
        else:
            print(serializer.errors)
            print("LEAVE NNNOOOOTT  SAVED")
        lastInstance = Leave.objects.last()
        return lastInstance


   ### TODO:
   ### send an email if admin agree
    def post(self,request):
        userPass = request.data.get("password")
        userMail = request.data.get("email")
        try:
            # Try to find a user matching userMail
            user = CustomUser.objects.get(email=userMail)

            #  Check the password if it match
            if (userPass == user.password):
                # Yes?  return a user
                #leaveInfo = Leave.objects.filter(id = user.leaveid)
                #serializer = LeaveSerializer(leaveInfo, many = True)
                serializer = CustomUserSerializer(user)
                response = serializer.data
            else:
                # No?  login failed, return false
                response = {"login": 'false'}
        except:
            # No user was found, return false
            response = {"login": 'false'}
        return Response(response)


#user can create a leave instance
#eave has "pending" attrib (True/fase)


#get list of pending application
#admin can open application: => get leave instance
#agree = change pending to false;
