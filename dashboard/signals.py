from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Complaint, TowerStatusEvent
from .utils import create_alert

ADMIN_EMAIL = getattr(settings, "ALERT_ADMIN_EMAIL", None)

@receiver(post_save, sender=Complaint)
def complaint_alert(sender, instance, created, **kwargs):
    if not created:
        return

    # مثال: إذا الشكوى Critical أو impact عالي (حسب بياناتك)
    if (instance.impact_level or "").lower() in ["high", "critical"] or (instance.status or "").lower() == "open":
        create_alert(
            title="New High Impact Complaint",
            message=f"Complaint in {instance.region}. Type: {instance.complaint_type}. Status: {instance.status}",
            severity="WARNING",
            region=instance.region,
            email_to=ADMIN_EMAIL
        )

@receiver(post_save, sender=TowerStatusEvent)
def tower_status_alert(sender, instance, created, **kwargs):
    if not created:
        return

    # مثال: إذا البرج صار Down
    if (instance.status or "").lower() in ["down", "offline", "outage"]:
        create_alert(
            title="Tower Down Detected",
            message=f"Tower {instance.tower.tower_id} in {instance.tower.region} changed status to {instance.status}",
            severity="CRITICAL",
            region=instance.tower.region,
            email_to=ADMIN_EMAIL
        )
