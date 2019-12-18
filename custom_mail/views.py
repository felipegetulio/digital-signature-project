from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from custom_mail.models import Message

from django.contrib.auth import login, authenticate

from django.core.signing import Signer
from django.core import signing

@login_required
def index(request):
    return HttpResponse("Hello, world. You're at the mail index.")


@login_required
def inbox(request):
	current_user = request.user
	messages_new = Message.objects.filter(read_status=False, recipient=current_user)
	messages_sent = Message.objects.filter(sender=current_user)
	messages_read = Message.objects.filter(read_status=True, recipient=current_user)

	users = User.objects.all()

	context = {
		'users': users,
		'sent': messages_sent,
		'new': messages_new,
		'read': messages_read,
	}

	return render(request, 'custom_mail/inbox.html', context)

@login_required
def message_view(request, message_id):
	message = get_object_or_404(Message, pk=message_id)

	try:
	   signer = Signer()
	   original = signer.unsign(message.text)
	   messages.success(request, 'Tudo certo! Nós garantimos a autenticidade dessa mensagem.')
	   message.read_status = True
	   message.save()

	   return render(request, 'custom_mail/message_view.html', context={'message': message, 'message_text':  original})

	except signing.BadSignature:
	   messages.warning(request, 'Ops! Houve um problema, a mensagem pode ter sido corrompida.')
	   return redirect('inbox')	
	   print("Tampering detected!")

	


@login_required
def message_send(request):
	if request.method == "POST":
		current_user = request.user

		data = request.POST.dict()

		message = Message()	

		signer = Signer()
		value = signer.sign(data["message_text"])

		message.text = value
		message.sender = current_user

		recipient = get_object_or_404(User, pk=data["recipient"])

		if recipient:
			message.recipient = recipient
			message.save()

			messages.success(request, 'Tudo certo! Mensagem enviada com sucesso.')	
		else:
			messages.warning(request, 'Ops! Parece que não conseguimos enviar sua mensagem.')	


		return redirect('inbox')


