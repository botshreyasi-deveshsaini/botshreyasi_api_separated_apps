from django.shortcuts import render
from rest_framework.views import APIView
from helper.views import GetUserID, GetAppID, GetStoreProcedureData, prepare_message
from rest_framework.response import Response
from authorization.models import User
from .models import CandidateStatus
from jobs.models import AddToJob
from referer.models import Referrer
from candidate.models import CandidateDetails
from email_log.models import EmailTemplates
from message_log.models import SmsTemplates
from message_log.views import StoreInMessageLog
from datetime import datetime

# Create your views here.


class CandidateStatusRelations(APIView):
    def get(self, request, id):
        all_status = 0
        if request.GET.get('allstatus') == "1":
            all_status = 1

        job_type = ''

        # if request.GET.get('jobid'):
        #     add_new_job = AddNewJob.objects.filter(id=request.GET.get('jobid')).first()
        #     if add_new_job:
        #         if add_new_job.is_client == 1:
        #             job_type = 'client'
        #         elif add_new_job.is_client == 0:
        #             job_type = 'department'

        param = [id, GetAppID(), GetUserID(), all_status, job_type]
        print(f"PARAM----------------->{param}")
        data = GetStoreProcedureData(
            'showchildstatuswithtype', param)
        return Response(data)

    def post(self, request):
        if request.method == 'POST':
            status = request.POST.get('status')
            noemail = int(request.GET.get('noemail', 0))

            if not status:
                return Response({'error': 'Status is required'})

            ajid = request.POST.get('ajid')
            statusid = request.POST.get('status')
            comment = request.POST.get('comment', '')
            is_interview = request.POST.get('isinterview', False)
            is_interview = '1' if is_interview == True else False
            doj = request.POST.get('doj')
            appid = GetAppID()
            self = GetUserID()
            self_email = User.objects.get(id=self).email
            recruiterid = request.POST.get('recruiterid', 53)
            date = request.POST.get('date', None)
            date = None if date == '2000-01-01' else date
            location = request.POST.get('location', '')
            contactperson = request.POST.get('contactperson', '')
            interviewquestion = request.POST.get('interviewquestion', '')
            interviewer = request.POST.get('Interviewer', '')
            modeofinterview = request.POST.get('modeofinterview', '')
            param = [
                ajid,
                statusid,
                comment,
                appid,
                self,
                date,
                is_interview,
                recruiterid,
                location,
                contactperson,
                interviewquestion,
                modeofinterview,
                interviewer,
                '',
                doj
            ]

            print(f"param----------->{param}")
            maxid = GetStoreProcedureData('candidate_status_insert', param)
            # if request.POST.get('noemail') is false:
            # print("Mail Sended")
            max_id = max(item['maxid'] for item in maxid)

            print(f"maxid  --> {max_id}")
            candidatestatus = CandidateStatus.objects.using(
                'mysqlslave').get(id=status, is_deleted=False)
            print(
                f"Candidate Status------->  {candidatestatus.referer_email_template_id}")
            addtojob = AddToJob.objects.using(
                'mysqlslave').filter(id=ajid).first()
            print(f"Candidate Status------->  {addtojob.id}")

            # Send mail
            params = [ajid, int(max_id)]
            print(noemail)
            if candidatestatus.referer_email_template_id is not None and candidatestatus.referer_email_template_id > 0:
                if addtojob is not None and addtojob.referrer_id is not None:
                    print('')
                    data = GetStoreProcedureData(
                        'getdetailonstatuschange', params)
                    reffer = Referrer.objects.using('mysqlslave').filter(
                        id=addtojob.referrer_id).first()
                    template_obj = EmailTemplates.objects.using('mysqlslave').filter(
                        id=candidatestatus.referer_email_template_id)
                    message = prepare_message(data, template_obj.message)
                    subject = prepare_message(data, template_obj.subject)
                    emailparams = {'application_id': appid,
                                   'added_by': self,
                                   'message': message,
                                   'subject': subject,
                                   'sended_by': template_obj.sended_by,
                                   'sender_name': template_obj.sender_name,
                                   'sended_to': reffer.email,
                                   'email_template_id': template_obj.id,
                                   'candidate_id': addtojob.candidate_id,
                                   }

                    # SendMail = SendMail(reffer.email)

            if candidatestatus.referer_sms_template_id is not None and candidatestatus.referer_sms_template_id > 0:
                if addtojob is not None and addtojob.referrer_id is not None:
                    data = GetStoreProcedureData(
                        'getdetailonstatuschange', params)
                    reffer = Referrer.objects.using('mysqlslave').filter(
                        id=addtojob.referrer_id).first()
                    template_obj = SmsTemplates.objects.using('mysqlslave').filter(
                        id=candidatestatus.referer_sms_template_id)
                    message = prepare_message(data, template_obj.message)
                    smsparams = {'application_id': appid,
                                 'added_by': self,
                                 'message': message,
                                 'sended_by': template_obj.sended_by,
                                 'sender_name': template_obj.sender_name,
                                 'sended_to': reffer.mobile_no,
                                 'sms_template': template_obj.id,
                                 'candidate_id': addtojob.candidate_id,
                                 'dlt_te_id': template_obj.dlt_te_id,
                                 'is_otp': 0,
                                 'sent_date': datetime.now()
                                 }
            if noemail == 0:
                print("done 1")
                if candidatestatus.candidate_email_template_id is not None and candidatestatus.candidate_email_template_id > 0:
                    print("done email")
                    if addtojob is not None and addtojob.candidate_id is not None:
                        data = GetStoreProcedureData(
                            'getdetailonstatuschange', params)
                        candidate = CandidateDetails.objects.using('mysqlslave').filter(
                            id=addtojob.candidate_id).first()
                        template_obj = EmailTemplates.objects.using('mysqlslave').filter(
                            id=candidatestatus.candidate_email_template_id)
                        message = prepare_message(data, template_obj.message)
                        emailparams = {'application_id': appid,
                                       'added_by': self,
                                       'message': message,
                                       'subject': subject,
                                       'sended_by': template_obj.sended_by,
                                       'sender_name': template_obj.sender_name,
                                       'sended_to': candidate.email,
                                       'email_template_id': template_obj.id,
                                       'candidate_id': addtojob.candidate_id,
                                       }
                if candidatestatus.candidate_sms_template_id is not None and candidatestatus.candidate_sms_template_id > 0:
                    print("done sms")
                    if addtojob is not None and addtojob.candidate_id is not None:
                        data = GetStoreProcedureData(
                            'getdetailonstatuschange', params)
                        candidate = CandidateDetails.objects.using('mysqlslave').filter(
                            id=addtojob.candidate_id).first()
                        template_obj = SmsTemplates.objects.using('mysqlslave').filter(
                            id=candidatestatus.candidate_sms_template_id).first()
                        print(
                            f"template_obj  --------->{template_obj.message}")
                        message = prepare_message(data, template_obj.message)
                        smsparams = {'application_id': appid,
                                     'added_by': self,
                                     'message': message,
                                     'sended_by': template_obj.sended_by,
                                     'sender_name': template_obj.sender_name,
                                     'sended_to': candidate.mobile_no,
                                     'sms_template': template_obj.id,
                                     'candidate_id': addtojob.candidate_id,
                                     'dlt_te_id': template_obj.dlt_te_id,
                                     'is_otp': 0,
                                     'sent_date': datetime.now()
                                     }
                        print(f"emaiparms-------->  {smsparams}")
                        sms = StoreInMessageLog.SendSMS(smsparams)
            return Response({'maxid': maxid})

        return Response({'error': 'Invalid request method'})
