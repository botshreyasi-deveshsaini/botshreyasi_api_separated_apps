from django.db import models

# Create your models here.
class InterviewScheduleCalls(models.Model):
    hiring_manager_id = models.IntegerField(blank=True, null=True)
    candidate_id = models.IntegerField()
    call_id = models.IntegerField(blank=True, null=True)
    candidate_name = models.CharField(db_column='candidate_name', max_length=450)  # Field name made lowercase.
    job = models.IntegerField()
    call_type = models.CharField(max_length=45)
    application = models.IntegerField()
    user = models.IntegerField(blank=True, null=True)
    isinterview_schedule = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=450, blank=True, null=True)
    plocation = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    call_date_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    last_action_time = models.DateTimeField(blank=True, null=True)
    is_inbound = models.IntegerField(blank=True, null=True)
    inter_schedule_for = models.CharField(max_length=45, blank=True, null=True)
    interview_date_time1 = models.DateTimeField(blank=True, null=True)
    interview_date_time2 = models.DateTimeField(blank=True, null=True)
    interview_date_time3 = models.DateTimeField(blank=True, null=True)
    candidate_selected_time = models.DateTimeField(blank=True, null=True)
    candidate_comment = models.TextField(blank=True, null=True)
    candidate_confirm = models.IntegerField(blank=True, null=True)
    token = models.CharField(max_length=200, blank=True, null=True)
    request_new_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'interview_schedule_calls'