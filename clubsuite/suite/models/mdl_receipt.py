from django.db import models

class Receipt(models.Model):
    did=models.ForeignKey('Division')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    who_purchase = models.CharField(max_length=50)

    PENDING = 'P'
    REQUESTED = 'R'
    ACCEPTED = 'A'
    DENIED = 'D'
    S_CHOICES = (
        (PENDING, "Pending"),
        (REQUESTED, "Requested"),
        (ACCEPTED, "Accepted"),
        (DENIED, "Denied")
    )
    status = models.CharField(
        max_length=1,
        choices=S_CHOICES,
        default=PENDING
    )

    notes = models.CharField(max_length=1000, blank=True)
