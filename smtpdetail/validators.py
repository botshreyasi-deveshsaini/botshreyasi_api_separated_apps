from django.core.validators import RegexValidator, URLValidator
# from validators.domain import domain

from django.core.exceptions import ValidationError


DOMAIN_NAME_REGEX = r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}?$"
USERNAME_REGEX = r"^[a-zA-Z0-9_.]+$"  # TODO: Ask what should be a good username. Or find yourself because this username is the email username.
HOSTNAME_VALIDATOR_REGEX = DOMAIN_NAME_REGEX
PORT_VALIDATOR_REGEX = r"^\d{1,4}$"

class DomainNameValidator(RegexValidator):

    def __init__(self, *args, **kwargs):

        super().__init__(regex=DOMAIN_NAME_REGEX, *args, **kwargs)

class UsernameValidator(RegexValidator):

    def __init__(self, *args, **kwargs):

        super().__init__(regex=USERNAME_REGEX, *args, **kwargs)

class HostnameValidator(RegexValidator):

    def __init__(self, *args, **kwargs):

        super().__init__(regex=HOSTNAME_VALIDATOR_REGEX, *args, **kwargs)

class PortValidator():

    def __init__(self, *args, **kwargs):
        # super().__init__(regex=PORT_VALIDATOR_REGEX, *args, **kwargs)
        self.message = "Enter port value between 1 and 65535"
        self.code="port_value_invalid"

    def __call__(self, value, *args, **kwargs):

        # If this field is BigIntegerField in models, then it's not required to
        # do isinstance(value, int) validation check. That validation is automatically provided
        # by Django interally by its models's default validator(s)
        if not (0 < value <= 65535):
            raise ValidationError(self.message, code=self.code, params={"value": value})

        # super().__call__(value, *args, **kwargs)


# validate_domain_name = URLValidator()
# validate_domain_name = domain
validate_domain_name = DomainNameValidator()
validate_username = UsernameValidator()
validate_hostname = HostnameValidator()
validate_port = PortValidator()
