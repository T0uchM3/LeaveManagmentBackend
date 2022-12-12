from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import LeaveSerializer
from .serializer import CustomUserSerializer
from django.conf import settings
from django.contrib.auth import authenticate
from .models import Leave, CustomUser
from django.core.mail import send_mail
import urllib.request
import json
import requests
import json
import urllib.request
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

        if(userGender == "Monsieur"):
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
        if(userGender == "Madame"):
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
        users = CustomUser.objects.filter()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    @staticmethod
    @api_view(['POST'])
    def addleave(request):
        startDate = request.data.get("startdate")
        endtDate = request.data.get("enddate")
        leaveType = request.data.get("leavetype")
        leaveDays = request.data.get("days")
        userID = request.data.get("userid")

        serializer_data = {}
        try:
            user = CustomUser.objects.get(id=userID)
            # only accept these 4 strings as a leave type
            if leaveType not in ("paid","paternity","maternity","rtt"):
                return Response({'status':'error','args': 'leave type must either be: paid,paternity,maternity or rtt',})
            if(leaveDays == 0):
                return Response({'status':'error','args': 'leave days must be > 0',})
            if(leaveType == "paid" and user.paid < int(leaveDays)):
               return Response({'status':'error','args': 'The days you selected are more than your available paid days',})
            if(leaveType == "paternity" and user.paternity < int(leaveDays)):
                return Response({'status':'error','args': 'The days you selected are  more than your available paternity days',})
            if(leaveType == "maternity" and user.maternity < int(leaveDays)):
                return Response({'status':'error','args': 'The days you selected are  more than your available maternity days',})
            if(leaveType == "rtt" and user.rtt < int(leaveDays)):
                return Response({'status':'error','args': 'The days you selected are  more than your available rtt days',})
           
        except:
             return Response({
                 'status':'error',
                 'args': 'no user with this id exist',
            })
        
        serializer_data = {
                "startdate":startDate,
                "enddate":endtDate,
                "leavetype":leaveType,
                "days":leaveDays,
                "userid":userID,
                "status":"pending",
        }
 
        print(serializer_data)
        serializer = LeaveSerializer(data=serializer_data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status':'success',
                'args': 'leave apply successfully sent',
            })
            return Response(serializer.data)
        else:
            return Response({
                'status': 'error',
                'agrs':serializer.errors,
            })

    @staticmethod
    @api_view(['GET'])
    def getuserleaves(request):
        userID = request.GET.get('id')
        leaves = Leave.objects.filter(userid=userID)
        serializer = LeaveSerializer(leaves, many=True)
        return Response(serializer.data)

    @staticmethod
    @api_view(['GET'])
    def getallleaves(request):
        leaves = Leave.objects.filter()
        serializer = LeaveSerializer(leaves, many=True)
        return Response(serializer.data)

    @staticmethod
    @api_view(['POST'])
    def deleteleave(request):
        leaveID = request.data.get("leaveid")
        try:
            leave = Leave.objects.filter(id=leaveID).first().delete()
        except:
             return Response({
                'status': 'error',
                'args':'no leave with this id exist',
            })
        
        leaves = Leave.objects.filter()
        serializer = LeaveSerializer(leaves, many=True)
        return Response(serializer.data)
        

    @staticmethod
    @api_view(['POST'])
    def updateleave(request):
        status = request.data.get("status")
        leaveID = request.data.get("leaveid")
        leave = Leave.objects.filter(id=leaveID).first()
        data = {
            "status": status,
            }
        conge = ""
        if status not in ("approved","canceled"):
             return Response({'status': 'error',
                             'args':'leave status must be changed to either approved or canceled'})
        
        serializer = LeaveSerializer(leave,data=data,partial=True)# updating leave status
        if serializer.is_valid():
               serializer.save() # updating leave status
               user = CustomUser.objects.filter(id=leave.userid).first()
               data = {}
               if leave.leavetype == "paid":
                   conge = "payé"
               if leave.leavetype == "paternity":
                   conge = "paternité"
               if leave.leavetype == "maternity":
                    conge = "maternité"
               if leave.leavetype == "rtt":
                    conge = "RTT"
               if status == "approved":
                  if leave.leavetype == "paid":
                      data = {
                        "paid": user.paid - leave.days,
                        }
                  if leave.leavetype == "paternity":
                      data = {
                        "paternity": user.paternity - leave.days,
                        }
                  if leave.leavetype == "maternity":
                       data = {
                         "maternity": user.maternity - leave.days,
                         }
                  if leave.leavetype == "rtt":
                       data = {
                         "rtt": user.rtt - leave.days,
                         }
                  mailsub = 'Acceptation de votre demande de congé de '
                  mailmessage = user.gender + ', \n \n Nous accusons bonne réception de votre demanddecongé pour ' + conge + ', \n prenons acte qu\'il sera effectué du ' + str(leave.startdate) + ' au ' + str(leave.enddate) + '.' + '\n \n Veuillez agrée, ' + user.gender + ', l\'expression de nos salutations distinguées.'
               if status == "canceled":
                  mailsub = 'Refus de votre demande de congés de '
                  mailmessage = user.gender + ', \n \n Nous accusons bonne réception de votre demande de congé pour ' + conge + ', \n prenons acte qu\'il sera effectué du ' + str(leave.startdate) + ' au ' + str(leave.enddate) + '.' + '\n \n Malheureusement, nous sommes au regret de vous informer que nous ne pouvons pas accepter votre demande.  \n \n Nous vous prions de bien vouloir agréer, ' + user.gender + ', l’expressionde nos sentiments distingués.'
               serializer = CustomUserSerializer(user,data=data,partial=True)# updating user status
               if serializer.is_valid():
                   serializer.save() # updating user status
                   leaves = Leave.objects.filter()
                   serializer = LeaveSerializer(leaves, many=True)
                   send_mail(subject= mailsub + conge,
                       message=mailmessage,
                       from_email=settings.EMAIL_HOST_USER,
                       recipient_list=[user.email,])
               return Response({
                     'status': 'success',
                     'agrs':serializer.data,
                 })
               return Response(serializer.data)
        else:
             return Response({
                'status': 'error',
                'agrs':serializer.errors,
            })


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
                response = {'status':'success',
                            'args':serializer.data}
            else:
                # No?  login failed, return false
                response = {'status': 'error',
                            'args':'wrong password'}
        except:
            # No user was found, return false
            response = {'status': 'error',
                        'args':'no user with this email found'}
        return Response(response)
