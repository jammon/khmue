from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


@receiver(user_logged_in)
def write_company_id_to_session(sender, **kwargs):
    user = kwargs["user"]
    if hasattr(user, "site_user"):
        request = kwargs["request"]
        request.session["company_id"] = user.site_user.company_id
