from urllib import urlencode

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from chaperone.models import Event

Message = lambda request, msg: render(request, 'message.html', {'msg': msg})

def index(request):
    if request.user.is_authenticated():
        profile = request.user.get_absolute_url()
        profile += '?' + urlencode({'home': True})
        response = redirect(profile)
    else:
        response = render(request, 'index.html')
    return response

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)


def loginView(request):
    redirectUrl = request.GET.get('next') or '/'
    if request.method == 'POST': # If the form has been submitted...
        form = LoginForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(redirectUrl) # Redirect after POST
                else:
                    return Message(request, 'Your account has been disabled!')
            else:
                return Message(request, 'Your username and password were wrong')

    else:
        form = LoginForm() # An unbound form

    return render(request, 'login.html', {
        'form': form,
    })


def logoutView(request):
    logout(request)
    return Message(request, 'Logged out!')

def userPage(request, username):
    params = {}
    user = get_object_or_404(User, username=username)
    events = []
    for event in Event.objects.all():
        pks = event.getPks()
        if user.pk in pks:
            events.append(event)
    expired = []
    active = []
    for event in events:
        if event.expired():
            expired.append(event)
        else:
            active.append(event)
    params['expired'] = expired
    params['active'] = active
    params['user'] = user
    params['home'] = request.GET.get('home')
    return render(request, 'userPage.html', params)


def temp(request, username):
    user = User.objects.get(username=username)
    events = Event.future_events().order_by('date')[:5]
    return render(request, 'email/duty.html', {'user': user, 'events': events})
