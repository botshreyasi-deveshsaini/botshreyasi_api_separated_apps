from django.db import models
from authorization.models import User
from application.models import Application
from candidate_status.models import CandidateStatus
from jobs.models import AddToJob,AddNewJob
from departments.models import Department
from candidate.models import CandidateDetails
from campaign.models import Campaign, CampaignEvent, CampaignChannel
# Create your models here.
class ActionTrigger(models.Model):
    status = models.ForeignKey(CandidateStatus, on_delete=models.SET_NULL, blank=True, null=True,default=1)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, default=1)
    candidate = models.ForeignKey(CandidateDetails, on_delete=models.CASCADE, default=1)
    add_to_job =models.ForeignKey(AddToJob, on_delete=models.CASCADE, default=1)
    job = models.ForeignKey(AddNewJob, on_delete=models.CASCADE, default=1)
    client_department = models.ForeignKey(Department, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1,)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, default=1)
    ip_address = models.CharField(blank=False, null=False, max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    later_time = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'campaign_triggers'



class TriggerActionCampaign(models.Model):
    status = models.ForeignKey(CandidateStatus, on_delete=models.SET_NULL, blank=True, null=True,default=1)
    action_name = models.CharField(max_length=45, blank=False, null=False)
    action_root_name = models.CharField(max_length=45, blank=False, null=False)
    action_temp_id = models.IntegerField(blank=True, null=True, default=1)
    channel = models.ForeignKey(CampaignChannel, on_delete=models.CASCADE, default=1)
    action_run_time = models.DateTimeField(auto_now_add=True)
    next_action_time = models.DateTimeField(blank=True,null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, default=1)
    candidate = models.ForeignKey(CandidateDetails, on_delete=models.CASCADE, default=1)
    add_to_job =models.ForeignKey(AddToJob, on_delete=models.CASCADE, default=1)
    event = models.ForeignKey(CampaignEvent, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1,)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, default=1)
    ip_address = models.CharField(blank=False, null=False, max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    is_action = models.BooleanField(default=False)
    is_next_action = models.BooleanField(default=False)
    job = models.ForeignKey(AddNewJob, on_delete=models.CASCADE, default=1)
    client_department = models.ForeignKey(Department, on_delete=models.CASCADE, default=1)
    is_ready_to_next_event = models.BooleanField(default=False)
    trigger = models.ForeignKey(ActionTrigger, on_delete=models.CASCADE, default=1)
    call_type = models.CharField(blank=True, null=True, max_length=45)
    class Meta:
        managed = True
        db_table = 'campaign_triggers_history'