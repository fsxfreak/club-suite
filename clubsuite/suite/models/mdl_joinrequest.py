from django.db import models

class JoinRequest(models.Model):
   uid = models.ForeignKey('User', on_delete=models.CASCADE)
   cid = models.ForeignKey('Club', on_delete=models.CASCADE)


