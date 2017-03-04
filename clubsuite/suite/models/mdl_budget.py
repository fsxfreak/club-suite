from django.db import models

from .mdl_division import Division

class Budget(models.Model):
    did = models.ForeignKey('Division', on_delete=models.CASCADE, null=True)

    planned = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        s=str(self.did)+' '+str(self.planned)
        return "Division and Plan: "+s
