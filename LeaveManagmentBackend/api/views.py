from pickletools import long1
from numpy import dtype
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import InputSerializerPOST
from .serializer import LeaveSerializer
from .serializer import CustomUserSerializer

from django.contrib.auth import authenticate
from .models import Input, Leave, CustomUser

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
    @api_view(['GET'])
    def test(request):
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        response = {"login": 'false'}
        return Response(response)
    def get(self,request):
        userFirstname = request.GET.get('firstname')
        userLasname = request.GET.get('lasname')
        userMail = request.GET.get('email')
        userPassword = request.GET.get('password')
        is_admin = request.GET.get('is_admin')
        userGender = request.GET.get('gender')


        leave = self.createLeave(userGender)
        print("leave ",leave)
        serializer_data = {
                "username":userFirstname+userLasname,
                "userfirstname":userFirstname,
                "userlastname":userLasname,
                "email":userMail,
                "password":userPassword,
                "is_admin":is_admin,
                "gender":userGender,
                "leaveid":leave
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
     
    def createLeave(self,gender):
        serializer_data ={}
        if(gender=="male"):
            print("male")
            serializer_data = {
                    "startdate":datetime.now(),
                    "enddate":'2022-12-04 20:40:43.419308+01',
                    "paternity":3,
                    "maternity":0,
                    "paid":30,
                    "rtt":0,
                    "reason":"aaa"
            }
        if(gender=="female"):
            print("female")
            serializer_data = {
                    "startdate":datetime.now(),
                    "enddate":datetime.now(),
                    "paternity":0,
                    "maternity":60,
                    "paid":30,
                    "rtt":0,
                    "reason":"aaa"
            }
        print(serializer_data)
        serializer = LeaveSerializer(data=serializer_data)
        if serializer.is_valid():
            serializer.save()
            print("LEAVE SAVED")
        else:
            print(serializer.errors)
            print("LEAVE NNNOOOOTT  SAVED")
        lastInstance= Leave.objects.last()
        return lastInstance


   ### TODO:
   # send an email if admin agree
    def post(self,request):
        userPass = request.data.get("password")
        userMail = request.data.get("email")
        try:
            # Try to find a user matching userMail
            user = CustomUser.objects.get(email=userMail)

            #  Check the password if it match
            if (userPass==user.password):
                # Yes? return true
                leaveInfo = Leave.objects.filter(id = user.leaveid)
                serializer = LeaveSerializer(leaveInfo, many = True)
                response = serializer.data
            else:
                # No? login failed, return false
                response = {"login": 'false'}
        except:
            # No user was found, return false 
            response = {"login": 'false'}
        return Response(response)
