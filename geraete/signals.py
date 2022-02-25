from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


@receiver(user_logged_in)
def write_company_id_to_session(sender, **kwargs):
    print("write_company_id_to_session started")
    user = kwargs["user"]
    print(f"{user=} ")
    if hasattr(user, "site_user"):
        print("hasattr site-user")
        request = kwargs["request"]
        request.session["company_id"] = user.site_user.company_id
