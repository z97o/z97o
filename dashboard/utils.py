from django.conf import settings
from django.core.mail import send_mail
from .models import Alert

def create_alert(title, message, severity="INFO", region=None, email_to=None):
    alert = Alert.objects.create(
        title=title,
        message=message,
        severity=severity,
        region=region,
    )

    # إرسال إيميل (إذا مفعل)
    if email_to:
        try:
            send_mail(
                subject=f"[{severity}] {title}",
                message=message,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                recipient_list=[email_to],
                fail_silently=True,
            )
        except:
            pass

    return alert
