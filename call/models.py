from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from application.models import Application
from authorization.models import User
from jobs.models import AddNewJob
from candidate.models import CandidateDetails
from candidate_status.models import CandidateStatus
from campaign_trigger.models import TriggerActionCampaign,ActionTrigger
from campaign.models import CampaignEvent,Campaign
# Create your models here.


class Calls(models.Model):
    country_code_validator = RegexValidator(
        regex=r'^\+\d{1,3}$',  # Example: +123
        message="Country code must be in the format '+123'."
    )
    mobile_no_validator = RegexValidator(
        regex=r'^\d{4,11}$',  # Example: 4 to 11 digits
        message="mobile_no number must be between 4 and 11 digits."
    )

    country_code = models.CharField(
        max_length=4,
        validators=[country_code_validator]
    )
    mobile_no = models.CharField(
        max_length=11,
        validators=[mobile_no_validator]
    )
    call_status = models.CharField(
        max_length=50, blank=False, null=False, default='sipcall')
    disposition = models.CharField(max_length=50, blank=False, null=False, default='No Status')
    call_language = models.CharField(
        max_length=50, blank=False, null=False, default='en-IN-NeerjaNeural')
    custom_data = models.JSONField(blank=False, null=False)
    conversation = models.TextField(blank=True, null=True)
    last_question = models.TextField(blank=True, null=True)
    call_start_time = models.DateTimeField(blank=True, null=True)
    call_end_time = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    call_duration = models.FloatField(null=True, blank=True)
    to_send_jd = models.BooleanField(default=False)
    interview_time_start = models.DateTimeField(blank=True, null=True)
    interview_time_end = models.DateTimeField(blank=True, null=True)
    gram_check_text = models.TextField(blank=True, null=True)
    gram_check_text_2 = models.TextField(blank=True, null=True)
    gram_check_perc = models.FloatField(blank=True, null=True)
    gram_check_perc_2 = models.FloatField(blank=True, null=True)
    grammer_avg_rating = models.FloatField(blank=True, null=True)
    skill_1 = models.FloatField(blank=True, null=True)
    skill_2 = models.FloatField(blank=True, null=True)
    skill_3 = models.FloatField(blank=True, null=True)
    skill_avg_rating = models.BooleanField(default=False)
    grammer_interview_audio_link1 = models.CharField(
        max_length=500, blank=True, null=True)
    grammer_interview_audio_link2 = models.CharField(
        max_length=500, blank=True, null=True)
    is_validate_conversation = models.BooleanField(default=False)
    call_to = models.CharField(max_length=50, default='bot7')
    islater = models.BooleanField(default=False)
    latter = models.DateTimeField(blank=True, null=True)
    inbound_lead = models.BooleanField(default=False)
    type_of_call = models.CharField(
        max_length=50, blank=False, null=False, default='OUTGOING')
    call_credit = models.CharField(max_length=50, default=1)
    call_initiate_id = models.CharField(max_length=50, default=54120)
    is_data_update = models.BooleanField(default=False)
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    job = models.ForeignKey(AddNewJob, on_delete=models.CASCADE, default=1)
    candidate = models.ForeignKey(
        CandidateDetails, on_delete=models.CASCADE, default=1)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    campaign_trigger_history = models.ForeignKey(TriggerActionCampaign, on_delete=models.SET_NULL, blank=True,null=True)
    campaign_trigger = models.ForeignKey(ActionTrigger, on_delete=models.SET_NULL, blank=True,null=True)
    campaign_event = models.ForeignKey(CampaignEvent, on_delete=models.SET_NULL, blank=True,null=True)
    campaing =  models.ForeignKey(Campaign, on_delete=models.SET_NULL, blank=True,null=True)
    bot_status = models.ForeignKey(CandidateStatus, on_delete=models.CASCADE, default=11)
    is_update = models.IntegerField(blank=True, null=True)
    other_slots = models.TextField(blank=True, null=True)
    call_history_id = models.IntegerField(blank=False,null=False,default=1)
    def clean(self):
        super().clean()

        if self.country_code and self.mobile_no:
            country_code_details = {
                # UK: starting number '7', 11-digit mobile_no numbers
                '+441': {'start': '7', 'length': 11},
                # Example: starting number '9', 10-digit mobile_no numbers
                '+123': {'start': '9', 'length': 10},
                # Example: starting number '6', 9-digit mobile_no numbers
                '+999': {'start': '6', 'length': 9},
                # India: starting numbers ['9', '7', '8', '6'], 10-digit mobile_no numbers
                '+91': {'start': ['9', '7', '8', '6'], 'length': 10},
                # Pakistan: starting number '3', 11-digit mobile_no numbers
                '+92': {'start': '3', 'length': 11},
                # Brazil: starting number '9', 11-digit mobile_no numbers
                '+55': {'start': '9', 'length': 11},
                # Afghanistan: starting number '7', 10-digit mobile_no numbers
                '+93': {'start': '7', 'length': 10},
                # Finland: starting number '4', mobile_no numbers can be 8, 9, or 10 digits
                '+358': {'start': '4', 'length': [8, 9, 10]},
                # Algeria: no starting number, 4-digit mobile_no numbers
                '+213': {'start': '', 'length': 4},
                # Add more country codes and details as needed
            }

            details = country_code_details.get(self.country_code, None)
            if details:
                expected_length = details['length']
                starting_numbers = details['start']
                if starting_numbers and not any(self.mobile_no.startswith(starting_number) for starting_number in starting_numbers):
                    raise ValidationError(
                        f"The mobile_no number does not match the expected format for the country code '{self.country_code}'."
                    )
                if isinstance(expected_length, list) and len(self.mobile_no) not in expected_length:
                    raise ValidationError(
                        f"The mobile_no number length does not match the expected length(s) for the country code '{self.country_code}'."
                    )
                if isinstance(expected_length, int) and len(self.mobile_no) != expected_length:
                    raise ValidationError(
                        f"The mobile_no number length does not match the expected length for the country code '{self.country_code}'."
                    )

    class Meta:
        managed = True
        db_table = 'calls'





class CallsHistories(models.Model):
    id = models.AutoField(primary_key=True)
    call_id = models.IntegerField(unique=True, blank=True, null=True)
    child_id = models.IntegerField(unique=True, blank=True, null=True)
    local_call_id = models.IntegerField(blank=True, null=True)
    child_local_id = models.IntegerField(blank=True, null=True)
    app_id = models.IntegerField(blank=True, null=True)
    candidate_id = models.IntegerField(blank=True, null=True)
    client_id = models.IntegerField(blank=True, null=True)
    recruiter_id = models.IntegerField(blank=True, null=True)
    job_id = models.IntegerField(blank=True, null=True)
    call_status_day1 = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    call_status_day3 = models.CharField(max_length=45, blank=True, null=True)
    conversation_day1 = models.TextField(blank=True, null=True)
    conversation_day3 = models.TextField(blank=True, null=True)
    mobile = models.CharField(max_length=20, db_collation='latin1_swedish_ci', blank=True, null=True)
    custom_data = models.JSONField(blank=False, null=False)
    disposition_day1 = models.CharField(max_length=100, db_collation='latin1_swedish_ci', blank=True, null=True)
    disposition_day3 = models.CharField(max_length=100, blank=True, null=True)
    call_port = models.CharField(max_length=20, db_collation='latin1_swedish_ci', blank=True, null=True)
    day_count = models.IntegerField(blank=True, null=True)
    is_open_mail_day1 = models.CharField(max_length=15, db_collation='latin1_swedish_ci', blank=True, null=True)
    is_open_mail_day2 = models.CharField(max_length=15, db_collation='latin1_swedish_ci', blank=True, null=True)
    is_open_mail_day3 = models.CharField(max_length=15, db_collation='latin1_swedish_ci', blank=True, null=True)
    link_open_in_mail_day1 = models.CharField(max_length=15, db_collation='latin1_swedish_ci', blank=True, null=True)
    link_open_in_mail_day2 = models.CharField(max_length=15, db_collation='latin1_swedish_ci', blank=True, null=True)
    link_open_in_mail_day3 = models.CharField(max_length=15, db_collation='latin1_swedish_ci', blank=True, null=True)
    link_open_in_sms_day1 = models.CharField(max_length=15, db_collation='latin1_swedish_ci', blank=True, null=True)
    link_open_in_sms_day2 = models.CharField(max_length=15, db_collation='latin1_swedish_ci', blank=True, null=True)
    link_open_in_sms_day3 = models.CharField(max_length=15, db_collation='latin1_swedish_ci', blank=True, null=True)
    campaign_name = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    validate_conversation = models.TextField(db_collation='latin1_swedish_ci', blank=True, null=True)
    interviewed_in_past = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    final_disposition = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    final_skill1 = models.IntegerField(blank=True, null=True)
    final_skill2 = models.IntegerField(blank=True, null=True)
    final_skill3 = models.IntegerField(blank=True, null=True)
    final_avg_rating = models.FloatField(blank=True, null=True)
    final_gram_check_perc = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    final_stop_campaign = models.IntegerField(blank=True, null=True)
    final_gram_check_perc2 = models.IntegerField(blank=True, null=True)
    final_is_completed = models.IntegerField(blank=True, null=True)
    final_is_read = models.IntegerField(blank=True, null=True)
    interview_avialibility = models.IntegerField(blank=True, null=True)
    conv_complete_perc = models.IntegerField(blank=True, null=True)
    final_gram_check_text = models.TextField(db_collation='latin1_swedish_ci', blank=True, null=True)
    candidate_status = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    is_validated = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    final_gram_check_text_2 = models.TextField(db_collation='latin1_swedish_ci', blank=True, null=True)
    add_to_job = models.IntegerField(blank=True, null=True)
    later_call_id = models.IntegerField(blank=True, null=True)
    later_child_id = models.IntegerField(blank=True, null=True)
    later_child_local_id = models.IntegerField(blank=True, null=True)
    conversation_later_call = models.TextField(db_collation='latin1_swedish_ci', blank=True, null=True)
    disposition_later_call = models.CharField(max_length=100, db_collation='latin1_swedish_ci', blank=True, null=True)
    call_status_later_call = models.CharField(max_length=100, db_collation='latin1_swedish_ci', blank=True, null=True)
    career_id = models.IntegerField(blank=True, null=True)
    is_complete_final_rating = models.IntegerField(blank=True, null=True)
    is_amcat_done = models.CharField(max_length=10, db_collation='latin1_swedish_ci', blank=True, null=True)
    status = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    responsecode = models.IntegerField(db_column='responseCode', blank=True, null=True)  # Field name made lowercase.
    uniqueid = models.CharField(db_column='uniqueID', max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    autologinurl = models.TextField(db_column='autoLoginURL', db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    message = models.CharField(max_length=450, db_collation='latin1_swedish_ci', blank=True, null=True)
    fresher_experienced = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    target_months = models.IntegerField(blank=True, null=True)
    json_data = models.TextField(db_collation='latin1_swedish_ci', blank=True, null=True)
    interview_link = models.TextField(db_collation='latin1_swedish_ci', blank=True, null=True)
    interview_link2 = models.TextField(db_collation='latin1_swedish_ci', blank=True, null=True)
    old_jobid = models.IntegerField(blank=True, null=True)
    old_preferredlocation = models.CharField(max_length=4500, db_collation='latin1_swedish_ci', blank=True, null=True)
    is_bonus = models.IntegerField(blank=True, null=True)
    bonus_month = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    again_send_mail = models.IntegerField(blank=True, null=True)
    day3_link_expire_time = models.DateTimeField(blank=True, null=True)
    assessment_start_time = models.DateTimeField(blank=True, null=True)
    assessment_end_time = models.DateTimeField(blank=True, null=True)
    last_action_time = models.DateTimeField(blank=True, null=True)
    assessment_completed = models.CharField(db_column='Assessment_Completed', max_length=10, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    assessment_status = models.CharField(db_column='Assessment_Status', max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    campaigncurrentstatus = models.CharField(db_column='CampaignCurrentStatus', max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    campaign_final_status = models.CharField(db_column='Campaign_Final_Status', max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    is_send_thankyou_msg = models.CharField(max_length=10, db_collation='latin1_swedish_ci', blank=True, null=True)
    device_name = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    browser_name = models.CharField(max_length=450, db_collation='latin1_swedish_ci', blank=True, null=True)
    completedbychatday1 = models.CharField(db_column='CompletedByChatDay1', max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    completedbychatday2 = models.CharField(db_column='CompletedByChatDay2', max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    amcat_update_time = models.DateTimeField(blank=True, null=True)
    chat_open_timeday1 = models.DateTimeField(blank=True, null=True)
    chat_open_timeday2 = models.DateTimeField(blank=True, null=True)
    process_name = models.CharField(db_column='Process_name', max_length=100, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    job_title = models.CharField(max_length=450, db_collation='latin1_swedish_ci', blank=True, null=True)
    completedbycallday1 = models.CharField(db_column='CompletedByCallDay1', max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    completedbycallday3 = models.CharField(db_column='CompletedByCallDay3', max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    chatstarttimeday1 = models.DateTimeField(db_column='ChatStarttimeDay1', blank=True, null=True)  # Field name made lowercase.
    chatendtimeday1 = models.DateTimeField(db_column='ChatendtimeDay1', blank=True, null=True)  # Field name made lowercase.
    chatstarttimeday3 = models.DateTimeField(db_column='ChatStarttimeDay3', blank=True, null=True)  # Field name made lowercase.
    chatendtimeday3 = models.DateTimeField(db_column='ChatendtimeDay3', blank=True, null=True)  # Field name made lowercase.
    chat_open_timeday3 = models.DateTimeField(blank=True, null=True)
    recruiter_name = models.CharField(max_length=450, db_collation='latin1_swedish_ci', blank=True, null=True)
    chat_disposition_day1 = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    chat_disposition_day3 = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    call_date_timeday1 = models.DateTimeField(db_column='call_date_timeDay1', blank=True, null=True)  # Field name made lowercase.
    call_date_timeday3 = models.DateTimeField(db_column='call_date_timeDay3', blank=True, null=True)  # Field name made lowercase.
    sms_link_open_count = models.IntegerField(blank=True, null=True)
    email_link_open_count = models.IntegerField(blank=True, null=True)
    total_calls = models.IntegerField(blank=True, null=True)
    max_rating = models.IntegerField(blank=True, null=True)
    recruiter_app_id = models.IntegerField(blank=True, null=True)
    data_log = models.CharField(max_length=100, db_collation='latin1_swedish_ci', blank=True, null=True)
    link_expired = models.IntegerField(blank=True, null=True)
    call_duration = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    call_start_time = models.DateTimeField(blank=True, null=True)
    call_end_time = models.DateTimeField(blank=True, null=True)
    amcat_updated_no_response = models.IntegerField(blank=True, null=True)
    amcat_sent_time_no_response = models.DateTimeField(blank=True, null=True)
    amcat_update_with_response = models.IntegerField(blank=True, null=True)
    amcat_sent_time_with_response = models.DateTimeField(blank=True, null=True)
    base_url = models.TextField(db_collation='latin1_swedish_ci', blank=True, null=True)
    base64_url = models.TextField(db_collation='latin1_swedish_ci', blank=True, null=True)
    final_avg_rating_skills = models.IntegerField(blank=True, null=True)
    is_available = models.CharField(max_length=15, db_collation='latin1_swedish_ci', blank=True, null=True)
    request_time = models.IntegerField(blank=True, null=True)
    submit_to_pannel = models.IntegerField(blank=False, null=False, default=0)
    interview_round = models.IntegerField(blank=False, null=False, default=0)
    status_changed =models.CharField(max_length=15, db_collation='latin1_swedish_ci', blank=True, null=True)
    campaign_trigger = models.ForeignKey(ActionTrigger, on_delete=models.SET_NULL, blank=True,null=True)

    class Meta:
        managed = True
        db_table = 'calls_histories'
