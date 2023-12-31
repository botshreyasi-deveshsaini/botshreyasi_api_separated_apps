# Generated by Django 3.2.19 on 2023-10-31 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('call', '0020_auto_20231030_1458'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallsHistories',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('call_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('child_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('local_call_id', models.IntegerField(blank=True, null=True)),
                ('child_local_id', models.IntegerField(blank=True, null=True)),
                ('app_id', models.IntegerField(blank=True, null=True)),
                ('candidate_id', models.IntegerField(blank=True, null=True)),
                ('client_id', models.IntegerField(blank=True, null=True)),
                ('recruiter_id', models.IntegerField(blank=True, null=True)),
                ('job_id', models.IntegerField(blank=True, null=True)),
                ('call_status_day1', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=45, null=True)),
                ('call_status_day3', models.CharField(blank=True, max_length=45, null=True)),
                ('conversation_day1', models.TextField(blank=True, null=True)),
                ('conversation_day3', models.TextField(blank=True, null=True)),
                ('mobile', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=20, null=True)),
                ('custom_data', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=1000, null=True)),
                ('disposition_day1', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=100, null=True)),
                ('disposition_day3', models.CharField(blank=True, max_length=100, null=True)),
                ('call_port', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=20, null=True)),
                ('day_count', models.IntegerField(blank=True, null=True)),
                ('is_open_mail_day1', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=15, null=True)),
                ('is_open_mail_day2', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=15, null=True)),
                ('is_open_mail_day3', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=15, null=True)),
                ('link_open_in_mail_day1', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=15, null=True)),
                ('link_open_in_mail_day2', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=15, null=True)),
                ('link_open_in_mail_day3', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=15, null=True)),
                ('link_open_in_sms_day1', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=15, null=True)),
                ('link_open_in_sms_day2', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=15, null=True)),
                ('link_open_in_sms_day3', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=15, null=True)),
                ('campaign_name', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=45, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('validate_conversation', models.TextField(blank=True, db_collation='latin1_swedish_ci', null=True)),
                ('interviewed_in_past', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=45, null=True)),
                ('final_disposition', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=45, null=True)),
                ('final_skill1', models.IntegerField(blank=True, null=True)),
                ('final_skill2', models.IntegerField(blank=True, null=True)),
                ('final_skill3', models.IntegerField(blank=True, null=True)),
                ('final_avg_rating', models.FloatField(blank=True, null=True)),
                ('final_gram_check_perc', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=45, null=True)),
                ('final_stop_campaign', models.IntegerField(blank=True, null=True)),
                ('final_gram_check_perc2', models.IntegerField(blank=True, null=True)),
                ('final_is_completed', models.IntegerField(blank=True, null=True)),
                ('final_is_read', models.IntegerField(blank=True, null=True)),
                ('interview_avialibility', models.IntegerField(blank=True, null=True)),
                ('conv_complete_perc', models.IntegerField(blank=True, null=True)),
                ('final_gram_check_text', models.TextField(blank=True, db_collation='latin1_swedish_ci', null=True)),
                ('candidate_status', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=45, null=True)),
                ('is_validated', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=45, null=True)),
                ('final_gram_check_text_2', models.TextField(blank=True, db_collation='latin1_swedish_ci', null=True)),
                ('add_to_job', models.IntegerField(blank=True, null=True)),
                ('later_call_id', models.IntegerField(blank=True, null=True)),
                ('later_child_id', models.IntegerField(blank=True, null=True)),
                ('later_child_local_id', models.IntegerField(blank=True, null=True)),
                ('conversation_later_call', models.TextField(blank=True, db_collation='latin1_swedish_ci', null=True)),
                ('disposition_later_call', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=100, null=True)),
                ('call_status_later_call', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=100, null=True)),
                ('career_id', models.IntegerField(blank=True, null=True)),
                ('is_complete_final_rating', models.IntegerField(blank=True, null=True)),
                ('is_amcat_done', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=10, null=True)),
                ('status', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=45, null=True)),
                ('responsecode', models.IntegerField(blank=True, db_column='responseCode', null=True)),
                ('uniqueid', models.CharField(blank=True, db_collation='latin1_swedish_ci', db_column='uniqueID', max_length=45, null=True)),
                ('autologinurl', models.TextField(blank=True, db_collation='latin1_swedish_ci', db_column='autoLoginURL', null=True)),
                ('message', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=450, null=True)),
                ('fresher_experienced', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=45, null=True)),
                ('target_months', models.IntegerField(blank=True, null=True)),
                ('json_data', models.TextField(blank=True, db_collation='latin1_swedish_ci', null=True)),
                ('interview_link', models.TextField(blank=True, db_collation='latin1_swedish_ci', null=True)),
                ('interview_link2', models.TextField(blank=True, db_collation='latin1_swedish_ci', null=True)),
                ('old_jobid', models.IntegerField(blank=True, null=True)),
                ('old_preferredlocation', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=4500, null=True)),
                ('is_bonus', models.IntegerField(blank=True, null=True)),
                ('bonus_month', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=45, null=True)),
                ('again_send_mail', models.IntegerField(blank=True, null=True)),
                ('day3_link_expire_time', models.DateTimeField(blank=True, null=True)),
                ('assessment_start_time', models.DateTimeField(blank=True, null=True)),
                ('assessment_end_time', models.DateTimeField(blank=True, null=True)),
                ('last_action_time', models.DateTimeField(blank=True, null=True)),
                ('assessment_completed', models.CharField(blank=True, db_collation='latin1_swedish_ci', db_column='Assessment_Completed', max_length=10, null=True)),
                ('assessment_status', models.CharField(blank=True, db_collation='latin1_swedish_ci', db_column='Assessment_Status', max_length=45, null=True)),
                ('campaigncurrentstatus', models.CharField(blank=True, db_collation='latin1_swedish_ci', db_column='CampaignCurrentStatus', max_length=45, null=True)),
                ('campaign_final_status', models.CharField(blank=True, db_collation='latin1_swedish_ci', db_column='Campaign_Final_Status', max_length=45, null=True)),
                ('is_send_thankyou_msg', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=10, null=True)),
                ('device_name', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=45, null=True)),
                ('browser_name', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=450, null=True)),
                ('completedbychatday1', models.CharField(blank=True, db_collation='latin1_swedish_ci', db_column='CompletedByChatDay1', max_length=45, null=True)),
                ('completedbychatday2', models.CharField(blank=True, db_collation='latin1_swedish_ci', db_column='CompletedByChatDay2', max_length=45, null=True)),
                ('amcat_update_time', models.DateTimeField(blank=True, null=True)),
                ('chat_open_timeday1', models.DateTimeField(blank=True, null=True)),
                ('chat_open_timeday2', models.DateTimeField(blank=True, null=True)),
                ('process_name', models.CharField(blank=True, db_collation='latin1_swedish_ci', db_column='Process_name', max_length=100, null=True)),
                ('job_title', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=450, null=True)),
                ('completedbycallday1', models.CharField(blank=True, db_collation='latin1_swedish_ci', db_column='CompletedByCallDay1', max_length=45, null=True)),
                ('completedbycallday3', models.CharField(blank=True, db_collation='latin1_swedish_ci', db_column='CompletedByCallDay3', max_length=45, null=True)),
                ('chatstarttimeday1', models.DateTimeField(blank=True, db_column='ChatStarttimeDay1', null=True)),
                ('chatendtimeday1', models.DateTimeField(blank=True, db_column='ChatendtimeDay1', null=True)),
                ('chatstarttimeday3', models.DateTimeField(blank=True, db_column='ChatStarttimeDay3', null=True)),
                ('chatendtimeday3', models.DateTimeField(blank=True, db_column='ChatendtimeDay3', null=True)),
                ('chat_open_timeday3', models.DateTimeField(blank=True, null=True)),
                ('recruiter_name', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=450, null=True)),
                ('chat_disposition_day1', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=45, null=True)),
                ('chat_disposition_day3', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=45, null=True)),
                ('call_date_timeday1', models.DateTimeField(blank=True, db_column='call_date_timeDay1', null=True)),
                ('call_date_timeday3', models.DateTimeField(blank=True, db_column='call_date_timeDay3', null=True)),
                ('sms_link_open_count', models.IntegerField(blank=True, null=True)),
                ('email_link_open_count', models.IntegerField(blank=True, null=True)),
                ('total_calls', models.IntegerField(blank=True, null=True)),
                ('max_rating', models.IntegerField(blank=True, null=True)),
                ('recruiter_app_id', models.IntegerField(blank=True, null=True)),
                ('data_log', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=100, null=True)),
                ('link_expired', models.IntegerField(blank=True, null=True)),
                ('call_duration', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=45, null=True)),
                ('call_start_time', models.DateTimeField(blank=True, null=True)),
                ('call_end_time', models.DateTimeField(blank=True, null=True)),
                ('amcat_updated_no_response', models.IntegerField(blank=True, null=True)),
                ('amcat_sent_time_no_response', models.DateTimeField(blank=True, null=True)),
                ('amcat_update_with_response', models.IntegerField(blank=True, null=True)),
                ('amcat_sent_time_with_response', models.DateTimeField(blank=True, null=True)),
                ('base_url', models.TextField(blank=True, db_collation='latin1_swedish_ci', null=True)),
                ('base64_url', models.TextField(blank=True, db_collation='latin1_swedish_ci', null=True)),
                ('final_avg_rating_skills', models.IntegerField(blank=True, null=True)),
                ('is_available', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=15, null=True)),
                ('request_time', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'calls_histories',
                'managed': True,
            },
        ),
    ]
