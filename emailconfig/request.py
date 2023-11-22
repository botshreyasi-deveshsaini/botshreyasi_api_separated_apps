from django.core.mail import EmailMessage
from django.conf import settings
from email.utils import formataddr

def sendmail(id,uid,subject,sended_by,sended_to,sended_bcc,sended_cc,message,sender_name):
    request_url  = "http://localhost:8000/"
    sender_email = f"{sended_by}@{settings.EMAIL_DOMAIN}"
    sender = formataddr((sender_name, sender_email))
    print(f"From Email >>>>>>>>>>>>>{sender}")

    message_header = "<h1>Send By Mr. Manoj singh bisht</h1>"
    message_footer = "<h4><b>Thank You<b></h4>"
    

    if sended_to is not None:
        recipient_list = sended_to.split(',')
        for recipient in recipient_list:
            recipient_tracking_url = f'<img src="{request_url}send-email/mail-track/?email={recipient}&email_log={id}&uid={uid}&receiver_type=recipient" alt="Recipient Tracking" style="display: none;"/>'
            recipient_message = message_header + message + recipient_tracking_url + message_footer
            email = EmailMessage(subject, recipient_message, sender, [sended_to])
            email.content_subtype = 'html'
            email.send()
    else :
        
        return "recipient Email is none"    
    if sended_cc is not None:
        cc_list = sended_cc.split(',')
        for cc in cc_list:
            cc_tracking_url = f'<img src="{request_url}email/mail-track/?email={cc}&message_log={id}&uid={uid}&receiver_type=cc" alt="CC Tracking" style="display: none;"/>'
            cc_message = message_header + message + cc_tracking_url + message_footer
            email = EmailMessage(subject, cc_message, sender, [cc])
            email.content_subtype = 'html'
            email.send()
    else :
        cc_list = []
    
    if sended_bcc is not None:
        bcc_list = sended_bcc.split(',')
        for bcc in bcc_list:
            bcc_tracking_url = f'<img src="{request_url}email/mail-track/?email={bcc}&message_log={id}&uid={uid}&receiver_type=bcc" alt="BCC Tracking" style="display: none;"/>'
            bcc_message = message_header + message + bcc_tracking_url + message_footer
            email = EmailMessage(subject, bcc_message, sender, [bcc])
            email.content_subtype = 'html'
            email.send()
        
    else :
        bcc_list = []
