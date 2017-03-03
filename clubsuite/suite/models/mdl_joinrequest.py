from django.db import models

class JoinRequest(models.Model):
   cid = models.ForeignKey('Club', on_delete=models.CASCADE)
   uid = models.ForeignKey('User', on_delete=models.CASCADE)
   reason = models.CharField(max_length=200)

   def __str__(self):
     return 'JoinRequest: ' + self.uid.get_full_name() + ' wants to join ' + str(self.cid)+ ' because ' + self.reason

