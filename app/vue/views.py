from lasDB.functions import httpOutput
from django.views.decorators.csrf import csrf_exempt
import json


def start(request):
	from django.shortcuts import render
	return render(request, 'vue/start.html')


def system(request):
	from .functions_basic import view_system
	return view_system(request)


def hcbDiagram(request):
	if not request.user.is_authenticated:
		return httpOutput(json.dumps({'errors': 'Not authenticated!'}), 'application/json')
	from hcbDiagram.views import getModels
	return httpOutput(json.dumps(getModels(request)), 'application/json')


def editData(request):
	from .functions_editdata import view_editData
	return view_editData(request)


def form(request):
	from .functions_forms import view_form
	return view_form(request)


def variantgroups(request):
	from .functions_variantgroups import view_variantgroups
	return view_variantgroups(request)


def mapToVariantgroups(request):
	from .functions_mapToVariantgroups import view_mapToVariantgroups
	return view_mapToVariantgroups(request)


def toolMap(request):
	from .functions_toolmap import view_toolmap
	return view_toolmap(request)


@csrf_exempt
def maps(request):
	from .functions_maps import view_maps
	return view_maps(request)


def export(request):
	from .functions_export import view_export
	return view_export(request)
