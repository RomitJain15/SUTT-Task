from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.socialaccount.models import SocialAccount

class DomainRestrictionBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email and email.endswith('@pilani.bits-pilani.ac.in'):
            # Allow authentication for users with specified email domain
            try:
                # Check if the user's email domain matches the allowed domain
                social_account = SocialAccount.objects.get(email=email, provider=GoogleProvider.id)
                return social_account.user
            except SocialAccount.DoesNotExist:
                pass
        return None
