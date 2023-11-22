from ast import mod
from email.headerregistry import Address
from ipaddress import ip_address
from django.db import models
from application.models import Application
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from authorization.models import User
# Create your models here.


class CandidateDetails(models.Model):
    country_code_validator = RegexValidator(
        regex=r'^\+\d{1,3}$',  # Example: +123
        message="Country code must be in the format '+123'."
    )
    mobile_no_validator = RegexValidator(
        regex=r'^\d{4,11}$',  # Example: 4 to 11 digits
        message="mobile_no number must be between 4 and 11 digits."
    )

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45, blank=True, null=True)
    middle_name = models.CharField(max_length=45, blank=True, null=True,)
    last_name = models.CharField(max_length=45, blank=True, null=True)
    candidate_name = models.CharField(max_length=191, blank=True, null=True)
    # mobile_no =  models.CharField(max_length=10, blank=False, null=False, unique=True)
    country_code =  models.CharField(
        max_length=4,
        validators=[country_code_validator],
        blank=False, null=False, default="+91"
    )
    mobile_no = models.CharField(
        max_length=11,
        validators=[mobile_no_validator],
        blank=False, null=False
    )
    email = models.EmailField(blank=False, null=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    pan_no = models.CharField(max_length=6, blank=True, null=True)
    aadharcard_number = models.IntegerField( blank=True, null=True)
    skill_set = models.CharField(max_length=445, blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    current_organization = models.CharField(max_length=90, blank=True, null=True)
    current_designation = models.CharField(max_length=90, blank=True, null=True)
    ovarall_experiance = models.CharField(max_length=90, blank=True, null=True)
    relevant_experiance = models.CharField(max_length=90, blank=True, null=True)
    qualification = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    preferred_location = models.CharField(max_length=190, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    current_salary = models.CharField(max_length=100, blank=True, null=True)
    expected_salary = models.CharField(max_length=100, blank=True, null=True)
    notice_period = models.IntegerField(blank=True, null=True)
    remark = models.CharField(max_length=100, blank=True, null=True)
    industry_type = models.CharField(max_length=100, blank=True, null=True)
    functional_area = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    # source = models.IntegerField(blank=True, null=True)
    resume = models.CharField(max_length=100, blank=True, null=True)
    cvhtml = models.TextField(blank=True, null=True)
    ip_address = models.CharField(max_length=100, blank=True, null=True)
    jobboard_url = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pincode =  models.IntegerField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} - {self.mobile_no} - {self.application}"
    
    def save(self, *args, **kwargs):
        if self.candidate_name:
            self.first_name, self.middle_name, self.last_name = self.parse_candidate_name(self.candidate_name)

        elif self.first_name and self.last_name:
            self.candidate_name = self.generate_candidate_name(self.first_name, self.middle_name, self.last_name)

        super().save(*args, **kwargs)

    @staticmethod
    def parse_candidate_name(candidate_name):
        # Implement your own parsing logic here
        # Split candidate_name into first_name, middle_name, last_name
        # For example:
        parts = candidate_name.split()
        if len(parts) == 1:
            return parts[0], None, None
        elif len(parts) == 2:
            return parts[0], None, parts[1]
        elif len(parts) >= 3:
            return parts[0], parts[1], " ".join(parts[2:])

    @staticmethod
    def generate_candidate_name(first_name, middle_name, last_name):
        # Implement your own logic here to generate candidate_name
        # For example:
        if middle_name:
            return f"{first_name} {middle_name} {last_name}"
        else:
            return f"{first_name} {last_name}"

    def clean(self):
        super().clean()

        if self.country_code and self.mobile_no:
            country_code_details = {
                '+441': {'start': '7', 'length': 11},   # UK: starting number '7', 11-digit mobile_no numbers
                '+123': {'start': '9', 'length': 10},   # Example: starting number '9', 10-digit mobile_no numbers
                '+999': {'start': '6', 'length': 9},    # Example: starting number '6', 9-digit mobile_no numbers
                '+91': {'start': ['9', '7', '8', '6'], 'length': 10},  # India: starting numbers ['9', '7', '8', '6'], 10-digit mobile_no numbers
                '+92': {'start': '3', 'length': 11},    # Pakistan: starting number '3', 11-digit mobile_no numbers
                '+55': {'start': '9', 'length': 11},    # Brazil: starting number '9', 11-digit mobile_no numbers
                '+93': {'start': '7', 'length': 10},    # Afghanistan: starting number '7', 10-digit mobile_no numbers
                '+358': {'start': '4', 'length': [8, 9, 10]},  # Finland: starting number '4', mobile_no numbers can be 8, 9, or 10 digits
                '+213': {'start': '', 'length': 4},     # Algeria: no starting number, 4-digit mobile_no numbers
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
        db_table = 'candidate_details'
        unique_together = (('application', 'email','mobile_no'),)


class CandidateNotes(models.Model):
    candidate = models.ForeignKey(CandidateDetails, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.CharField(max_length=6, blank=False, null=False)
    ip_address = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    class Meta:
        managed = True
        db_table = 'candidate_notes'    