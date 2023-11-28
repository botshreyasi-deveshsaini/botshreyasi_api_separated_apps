from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
# from validators.domain import domain

from django.core.exceptions import ValidationError

INDIAN_MOBILE_REGEX = r"^(\+91[\-\s])?[6789]\d{9}$"
OFF_DAYS_VALIDATOR = r"\[\]"

class IndianMobileNumberValidator(RegexValidator):

    def __init__(self, *args, **kwargs):
        super().__init__(regex=INDIAN_MOBILE_REGEX, *args, **kwargs)

class OffDaysValidator(RegexValidator):

    def __init__(self, *args, **kwargs):
        self.message = "Please enter valid off days input"
        self.code = "off_days_input_invalid"

    def __call__(self, value, *args, **kwargs):

        try:
            _offdayslist = value.split(",")
            offdayslist = map(int, _offdayslist)

            for day in offdayslist:
                if 0 <= day < 7:
                    pass
                else:
                    raise ValueError

        except ValueError:
            raise ValidationError(self.message, code=self.code, params={'value': value})

validate_email = EmailValidator()
validate_indian_mobile = IndianMobileNumberValidator()
validate_off_days = OffDaysValidator()

# DOMAIN_NAME_REGEX = r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}?$"
# USERNAME_REGEX = r"^[a-zA-Z0-9_.]+$"  # TODO: Ask what should be a good username. Or find yourself because this username is the email username.
# HOSTNAME_VALIDATOR_REGEX = DOMAIN_NAME_REGEX
# PORT_VALIDATOR_REGEX = r"^\d{1,4}$"

# class DomainNameValidator(RegexValidator):

#     def __init__(self, *args, **kwargs):

#         super().__init__(regex=DOMAIN_NAME_REGEX, *args, **kwargs)

# class UsernameValidator(RegexValidator):

#     def __init__(self, *args, **kwargs):

#         super().__init__(regex=USERNAME_REGEX, *args, **kwargs)

# class HostnameValidator(RegexValidator):

#     def __init__(self, *args, **kwargs):

#         super().__init__(regex=HOSTNAME_VALIDATOR_REGEX, *args, **kwargs)

# class PortValidator():

#     def __init__(self, *args, **kwargs):
#         # super().__init__(regex=PORT_VALIDATOR_REGEX, *args, **kwargs)
#         self.message = "Enter port value between 1 and 65535"
#         self.code="port_value_invalid"

#     def __call__(self, value, *args, **kwargs):

#         # If this field is BigIntegerField in models, then it's not required to
#         # do isinstance(value, int) validation check. That validation is automatically provided
#         # by Django interally by its models's default validator(s)
#         if not (0 < value <= 65535):
#             raise ValidationError(self.message, code=self.code, params={"value": value})

#         # super().__call__(value, *args, **kwargs)



# # validate_domain_name = URLValidator()
# # validate_domain_name = domain
# validate_domain_name = DomainNameValidator()
# validate_username = UsernameValidator()
# validate_hostname = HostnameValidator()
# validate_port = PortValidator()
