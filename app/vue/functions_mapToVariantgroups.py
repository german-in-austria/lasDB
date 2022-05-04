from lasDB.functions import httpOutput
from django.db.models import Q
from django.db.models import Count
import json


def view_mapToVariantgroups(request):
	if not request.user.is_authenticated:
		return httpOutput(json.dumps({'errors': 'Not authenticated!'}), 'application/json')
	# print(request.POST)
	if 'get' in request.POST:
		if request.POST.get('get') == 'getMapToVariantgroupData':
			return getMapToVariantgroupData(request)
	if 'set' in request.POST:
		if request.POST.get('set') == 'setMapToVariantgroupData':
			return setMapToVariantgroupData(request)


def setMapToVariantgroupData(request):
	output = {'warnings': []}
	if 'mapID' in request.POST and 'mtvObjs' in request.POST:
		from django.apps import apps
		aModel = apps.get_model(app_label='db', model_name='map_to_variantgroup')
		for mtvObj in json.loads(request.POST.get('mtvObjs')):
			print(mtvObj)
			if 'delete' in mtvObj:
				if mtvObj['id'] > 0:
					aQuery = aModel.objects.get(id=mtvObj['id'])
					aQuery.delete()
			else:
				if mtvObj['id'] > 0:
					aQuery = aModel.objects.get(id=mtvObj['id'])
				else:
					aQuery = aModel()
				aQuery.map_id = request.POST.get('mapID')
				aQuery.variantgroup_id = mtvObj['variantgroup']['id']
				aQuery.order = mtvObj['order']
				aQuery.preset_color = mtvObj['preset_color']
				aQuery.save()
	if output:
		return httpOutput(json.dumps(output), 'application/json')
	else:
		return httpOutput(json.dumps({'errors': 'No output!'}), 'application/json')


def getMapToVariantgroupData(request):
	output = {}
	if 'mapID' in request.POST:
		# print(request.POST.get('variableID'))
		from django.apps import apps
		aModel = apps.get_model(app_label='db', model_name='map_to_variantgroup')
		aQuery = aModel.objects.filter(map__id=request.POST.get('mapID')).distinct()
		output['map_to_variantgroup'] = []
		for aRow in aQuery:
			output['map_to_variantgroup'].append({
				'id': aRow.id,
				'variantgroup': {
										'id': aRow.variantgroup.id,
										'name': aRow.variantgroup.name,
										'lexVariable': aRow.variantgroup.lex_variable_id,
										'lexVariableStr': str(aRow.variantgroup.lex_variable)
									},
				'order': aRow.order,
				'preset_color': aRow.preset_color,
				'str': str(aRow),
			})
		output['count'] = len(aQuery)
	if output:
		return httpOutput(json.dumps(output), 'application/json')
	else:
		return httpOutput(json.dumps({'errors': 'No output!'}), 'application/json')
