# from rest_framework import generics, status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.permissions import IsAuthenticated
# from helper.views import *
# from smtpdetail.models import SMTPDetails
# from smtpdetail.serializers import SMTPSerializer

# @method_decorator(csrf_exempt,name='dispatch')
# class SMTPdetails(APIView):
#     permission_classes=(IsAuthenticated,)
#     def post(self, request):
#         print(f"SMTP Details:-->>>>>>>>>>>>>>>>>>>>>>>>{request.data}")
#         mutable_data = request.data.copy()
#         mutable_data['application'] = GetAppID()
#         mutable_data['creater'] = GetUserID()
#         serializer = SMTPDetails(data=mutable_data)
#         if serializer.is_valid():
#           Job = serializer.save()
#           return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     

#     def get(self,request,*args,**kwargs):
#         app_id = GetAppID()
#         try:
#             smtpdetails = SMTPSerializer(SMTPDetails.objects.get(application=app_id)).data
#         except:
#             smtpdetails =[]
#         return Response(smtpdetails)


# --------

# from django.shortcuts import render
# from django.http import HttpResponse
# from django.core.exceptions import ValidationError

# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response

# from .models import EmailData

# from .serializers import EmailDataSerializer

# # Create your views here.

# class store_data(APIView):

#     def post(self, request):

#         data = request.data.copy()

#         # senderEmail, username, domainName, smtpHost, smtpPort, password =\
#         #     None, None, None, None, None, None

#         # emailData = EmailData()

#         # if data.get('sender_email'):
#         #     senderEmail = data.get('sender_email')
#         #     emailData.senderEmail = senderEmail

#         # elif data.get('username') and data.get('domain_name'):
#         #     username = data.get('username')
#         #     domainName = data.get('domain_name')

#         #     emailData.username = username
#         #     emailData.domainName = domainName
#         # else:
#         #     return Response(data={"result": "Invalid data"})

#         # smtpHost = data.get('smtp_host')
#         # smtpPort = data.get('smtp_port')
#         # password = data.get('password')

#         # emailData.smtpHost = smtpHost
#         # emailData.smtpPort = smtpPort
#         # emailData.password = password

#         # emailData.save()


#         emaildata = {}

#         if data.get("sender_email"):
#             emaildata['senderEmail'] = data.get('sender_email')
        
#         elif data.get("username") and data.get("domain_name"):
#             emaildata['username'] = data.get('username')
#             emaildata['domainName'] = data.get('domain_name')
#         else:
#             return Response(data={"result": "Invalid data"})
        
#         emaildata['smtpHost'] = data.get('smtp_host')
#         emaildata['smtpPort'] = data.get('smtp_port')
#         emaildata['password'] = data.get('password')


#         emailDataSerializer = EmailDataSerializer(data=emaildata)

#         if emailDataSerializer.is_valid():  # <- We can also use <obj>.is_valid(raise_exception=True)
#             emailDataSerializer.save()
#         else:
#             print(emailDataSerializer.errors)  # Logging
#             return Response(emailDataSerializer.errors)

#         return HttpResponse("Data saved successfully")

# class send_mail(APIView):

#     def post(self, request):

#         import smtplib

#         emaildatas = EmailData.objects.all().values()

#         for emaildata in emaildatas:

#             gmail_user = emaildata['senderEmail']
#             gmail_password = emaildata['password']
#             sent_from = gmail_user
#             to = "devesh.s@botshreyasi.com"
#             msg = "Message from /api/sendmail/"

#             # gmail_user = 'devesh.s@botshreyasi.com'
#             # gmail_password = 'aaaa'

#             # sent_from = gmail_user
#             # to = ["atul.u@botshreyasi.com"]
#             # subject = 'OMG Super Important Message'
#             # # msg = "smtp message"

#             server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#             server.ehlo()
#             server.login(gmail_user, gmail_password)
#             server.sendmail(sent_from, to, msg)
#             server.close()

#             print('Email sent!')

#         return HttpResponse("Emails sent successfully")
#         # return Response(data={"result": "Emails sent successfully!"}, status=status.HTTP_200_OK)



