from django.db import models

class JoinRequest(models.Model):
   cid = models.ForeignKey('Club', on_delete=models.CASCADE)
   uid = models.ForeignKey('User', on_delete=models.CASCADE)


