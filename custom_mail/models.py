from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
	sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name='remetente')
	recipient = models.ForeignKey(User, on_delete=models.PROTECT, related_name='destinatário')
	text = models.TextField()
	dispatch_date = models.DateTimeField(auto_now_add=True)
	read_status = models.BooleanField(default=False)

	class Meta(object):
		verbose_name = "mensagem"
		verbose_name_plural = "mensagens"
