from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from .models import Key

from Crypto.PublicKey import RSA

secret_code = 'Unguessable'

def create_key_pairs(secret_code, username):
    key = RAS.generate(2048)
    private_key = key.export_key(passphrase=secret_code, pkcs=8, protection='scryptAndAES128-CBC')
    file_out = open('{}__rsa_key.bin'.format(username), 'wb')
    file_out.write(private_key)
    file_out.close()

    return key.publickey().export_key()

def save_public_key(key, user):
    Key.objects.create(user=user, public_key=key)
 
def signup(request):

    print(Key.objects.all())

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            
            public_key = create_key_pairs(secret_code, user.username)
            save_public_key(public_key, user)

            user = authenticate(username=user.username, password=raw_password)

            print(Key.objects.all())

            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

