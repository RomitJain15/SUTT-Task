# authentication/adapters.py

from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import ValidationError

class RestrictEmailAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        # Allowed domain for the organization
        allowed_domain = 'example.com'

        # Check if the email domain belongs to the allowed organization
        if not email.endswith('@' + allowed_domain):
            raise ValidationError('You can only register with an email from example.com domain.')
        
        return email
