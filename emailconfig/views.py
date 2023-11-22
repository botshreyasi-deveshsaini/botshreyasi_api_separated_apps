from django.utils import timezone
from rest_framework import  status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# from message_logs.models import MessageLogs
from email_log.models import EmailsLogs,EmailTemplates
from datetime import datetime
from .request import *
from .serializer import EmailTrackerSerializer
from email_log.serializers import EmailLogs_serializer

# Create your views here.
class SendMail(APIView):
    def get(self,request):
        datetime_value = datetime.now()
        emails_list = EmailsLogs.objects.filter(is_send=0, is_otp=0).order_by('id')[:10]
        print(f"Emails list -------------> {emails_list}")
        for email in emails_list:
          # template_list = EmailTemplates.objects.using('mysqlslave').filter(id=email.message_template_id).first()
          sender_name =email.sender_name
          # email_header_footer = template_list.email
          id=email.id
          uid = email.uid
          subject= email.subject
          message = email.message
          sended_by = email.sended_by
          sended_to = email.sended_to
          sended_bcc =email.sended_bcc
          sended_cc = email.sended_cc
          emailSend = sendmail(id,uid,subject,sended_by,sended_to,sended_bcc,sended_cc,message,sender_name)
          # print(emailSend)
          print(f"emails:---->>>>>>>>>>>>>mail Sended")
          emaildata = {'is_send': 1, 'is_update':10}
          # email.issend = 1
          serializer = EmailLogs_serializer(email, data=emaildata,partial=True )
          if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data)
            print(f"Email status updated for email ID {email.id}")

          else:
             print(serializer.errors)

        return Response("mail send")




class EmailTracker(APIView):
   def get(self,request):
       print(request.GET)
       date = datetime.now()
      #  date = timezone.make_aware(now, timezone.get_current_timezone())
       print("track Email")
       print(date)
       email= request.GET.get('email')
       uid = request.GET.get('uid')
       receiver_type = request.GET.get('receiver_type')
       email_log_id = request.GET.get('email_log')
       print(f"receiver_type>>>>>>>>>>>>>>>>>>>>>>>>{receiver_type}")
       if receiver_type == "recipient":
          print("manoj manoj")
          MessageLog = EmailsLogs.objects.filter(sended_to=email, uid=uid, id=email_log_id,is_read=False).update(is_read=True, read_at=timezone.now())
          # print(MessageLog.message)
      # message_log_id = request.data.message_log_id
       ip_address = request.META.get('REMOTE_ADDR')
       mutable_data = request.GET.copy()
       mutable_data['ip_address'] = ip_address
       serializer = EmailTrackerSerializer(data=mutable_data)
       if serializer.is_valid():
          Job = serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


       