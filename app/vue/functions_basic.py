from pickle import TRUE
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
    if request.POST.get('get') == 'variantgroup':
      return view_variantgroup(request)


def view_variantgroup(request):
  status = {}
  status['errors'] = []
  status['variantgroup'] = None
  if request.user.is_authenticated:
    from django.apps import apps
    from django.apps import apps
    aModel = apps.get_model(app_label='db', model_name='lex_variantgroup')
    status['variantgroup'] = { 'withoutVariableCount': aModel.objects.filter(lex_variable = None).count(), 'count': aModel.objects.all().count() }
    if 'check' in request.POST and request.POST.get('check'):
      aQuery = aModel.objects.filter(lex_variable = None)[0:100]
      status['check'] = []
      for aVG in aQuery:
        aVGvariables = []
        for aVtVG in aVG.lex_variant_to_variantgroup_set.select_related('lex_variant').all():
          if aVtVG.lex_variant:
            for aDiVtVG in aVtVG.lex_variant.data_set.select_related('lex_variable').all():
              aDiVtVGObj = { 'id': aDiVtVG.lex_variable.id, 'name': str(aDiVtVG.lex_variable) }
              if aDiVtVGObj not in aVGvariables:
                aVGvariables.append(aDiVtVGObj)
        aCheck = {
            'id': aVG.id,
            'name': str(aVG),
            'variables': aVGvariables
          }
        if len(aVGvariables) == 1:
          aVG.lex_variable_id = aVGvariables[0]['id']
          aVG.save()
          aCheck['repaired'] = True
        status['check'].append(aCheck)
      status['variantgroup']['withoutVariableCount'] = aModel.objects.filter(lex_variable = None).count()

  return httpOutput(json.dumps(status), 'application/json')

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
    status['errors'].append({'title': 'Name/Password wrong!'})
  return httpOutput(json.dumps(status), 'application/json')


def view_logout(request):
  logout(request)
  status = {}
  status['errors'] = []
  status['logout'] = True
  status['csrf'] = csrf.get_token(request)
  return httpOutput(json.dumps(status), 'application/json')
