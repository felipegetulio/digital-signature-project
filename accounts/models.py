from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Key(models.Model):

	user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='key_owner')
	public_key = models.TextField()

	class Meta(object):
		verbose_name = "chave"
		verbose_name_plural = "chaves"