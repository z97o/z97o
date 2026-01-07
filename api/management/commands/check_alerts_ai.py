from django.core.management.base import BaseCommand
from dashboard.models import RiskScore

THRESHOLD = 0.7

class Command(BaseCommand):
    help = "Print alerts where risk_prob >= 0.7 (latest entries)."

    def handle(self, *a, **o):
        flagged = RiskScore.objects.filter(risk_prob__gte=THRESHOLD).order_by("-ts")[:50]
        if not flagged:
            self.stdout.write("No high-risk regions.")
            return
        for r in flagged:
            self.stdout.write(self.style.WARNING(f"[ALERT] {r.region.name} @ {r.ts} risk={r.risk_prob:.2f} anomaly={r.anomaly}"))
