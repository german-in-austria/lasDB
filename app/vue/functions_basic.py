from django.contrib.auth import authenticate, login, logout
from django.middleware import csrf
from lasDB.functions import httpOutput
import json


def view_system(request):
	if 'get' in request.POST:
		if request.POST.get('get') == 'status':
			return view_status(request)
		if request.POST.get('get') == 'login':
			return view_login(request)
		if request.POST.get('get') == 'logout':
			return view_logout(request)


def view_status(request):
  status = {}
  status['errors'] = []
  status['user'] = None
  if request.user.is_authenticated:
    status['user'] = { 'name': request.user.username, 'last_login': str(request.user.last_login), 'staff': request.user.is_staff, 'admin': request.user.is_superuser }
  return httpOutput(json.dumps(status), 'application/json')


def view_login(request):
  status = {}
  status['errors'] = []
  user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
  if user is not None:
    login(request, user)
    status['login'] = True
    status['csrf'] = csrf.get_token(request)
  else:
    status['errors'].append({'title': 'Name/Passwort falsch!'})
  return httpOutput(json.dumps(status), 'application/json')


def view_logout(request):
  logout(request)
  status = {}
  status['errors'] = []
  status['logout'] = True
  status['csrf'] = csrf.get_token(request)
  return httpOutput(json.dumps(status), 'application/json')
