from lasDB.functions import httpOutput
from django.db.models import Q
from django.db.models import Count
import json


def view_variantgroups(request):
	if not request.user.is_authenticated:
		return httpOutput(json.dumps({'errors': 'Not authenticated!'}), 'application/json')
	# print(request.POST)
	if 'get' in request.POST:
		if request.POST.get('get') == 'getVariantByVariable':
			return getVariantByVariable(request)
	if 'set' in request.POST:
		if request.POST.get('set') == 'setVariantgroup':
			return setVariantgroup(request)
	if 'del' in request.POST:
		if request.POST.get('del') == 'delVariantgroup':
			return delVariantgroup(request)
	if 'update' in request.POST:
		if request.POST.get('update') == 'variantgroups':
			return updateVariantgroup(request)


def updateVariantgroup(request):
	output = {}
	from django.apps import apps
	aModel = apps.get_model(app_label='db', model_name='lex_variantgroup')
	aModelV = apps.get_model(app_label='db', model_name='lex_variant_to_variantgroup')
	aQuery = aModel.objects.exclude(lex_variable_id__gte=1)
	if aQuery.count() > 0:
		for vg in aQuery:
			print('=====')
			print('=', vg)
			print('-----')
			orgId = vg.id
			variableIds = []
			for v in vg.lex_variant_to_variantgroup_set.all():
				variables = v.lex_variant.data_set.all().values('lex_variable').annotate(c=Count('lex_variable')).order_by('lex_variable')
				for vx in variables:
					if vx['lex_variable'] not in variableIds:
						variableIds.append(vx['lex_variable'])
			# print('-', variableIds)
			if len(variableIds) > 0:
				dg = 0
				for vId in variableIds:
					vg.lex_variable_id = vId
					if dg > 0:
						vg.pk = None
					vg.save()
					# ToDo: lex_variant_to_variantgroup_set anpassen !!!!!
					print('Variant Group ' + ('updated' if dg == 0 else 'created') + ' ...', vg.pk, '->', vId, vg)
					dg += 1
			else:
				print('Keine ...', variableIds)
				print(vg.lex_variant_to_variantgroup_set.all())
				if 'emptyGroups' not in output:
					output['emptyGroups'] = []
				output['emptyGroups'].append(str(vg.id) + ' - ' + str(vg))
			# print(vg.lex_variant_to_variantgroup_set.all().values('lex_variant').annotate(c=Count('lex_variant')).order_by('lex_variant'))
	output['count'] = aQuery.count()
	if output:
		return httpOutput(json.dumps(output), 'application/json')
	else:
		return httpOutput(json.dumps({'errors': 'No output!'}), 'application/json')


def delVariantgroup(request):
	output = {}
	if 'id' in request.POST:
		from django.apps import apps
		aModel = apps.get_model(app_label='db', model_name='lex_variantgroup')
		aQuery = aModel.objects.get(id=request.POST.get('id'))
		aQuery.delete()
	if output:
		return httpOutput(json.dumps(output), 'application/json')
	else:
		return httpOutput(json.dumps({'errors': 'No output!'}), 'application/json')


def setVariantgroup(request):
	output = {'warnings': []}
	if 'variableID' in request.POST and 'variantIDs' in request.POST and 'groupID' in request.POST:
		# print(request.POST.get('variableID'), json.loads(request.POST.get('variantIDs')), request.POST.get('groupID'))
		from django.apps import apps
		aModel = apps.get_model(app_label='db', model_name='lex_variant_to_variantgroup')
		gID = int(request.POST.get('groupID'))
		if gID < 0 and request.POST.get('name'):
				# print('new', gID, request.POST.get('name'))
				gModel = apps.get_model(app_label='db', model_name='lex_variantgroup')
				vGroup = gModel.objects.filter(lex_variable_id=request.POST.get('variableID'), name=request.POST.get('name'))
				if len(vGroup) > 0:
					gID = vGroup[0].id
					output['warnings'].append('Variant Group with name "' + request.POST.get('name') + '" already exists! Used Variant Group with id ' + str(gID) + '.')
				else:
					nGroup = gModel()
					nGroup.name = request.POST.get('name')
					nGroup.lex_variable_id = request.POST.get('variableID')
					nGroup.save()
					gID = nGroup.id
		if gID > 0:
			for variantID in json.loads(request.POST.get('variantIDs')):
				# print(variantID, len(aModel.objects.filter(lex_variant_id=variantID, variantgroup=request.POST.get('groupID'))))
				if len(aModel.objects.filter(lex_variant_id=variantID, variantgroup_id=gID)) == 0:
					newV2Group = aModel()
					newV2Group.lex_variant_id = variantID
					newV2Group.variantgroup_id = gID
					newV2Group.save()
				else:
					output['warnings'].append('Variant to Variant Group connection already exists!')
	if output:
		return httpOutput(json.dumps(output), 'application/json')
	else:
		return httpOutput(json.dumps({'errors': 'No output!'}), 'application/json')


def getVariantByVariable(request):
	output = {}
	if 'variableID' in request.POST:
		variableID = request.POST.get('variableID')
		from django.apps import apps
		aModel = apps.get_model(app_label='db', model_name='lex_variable')
		aQuery = aModel.objects.get(id=variableID)
		output['variable'] = {
			'id': aQuery.id,
			'variable': aQuery.variable,
			'comment': aQuery.comment,
			'in_question': aQuery.in_question_id,
			'pdf_ocr_identifier': aQuery.pdf_ocr_identifier,
			'str': str(aQuery)
		}
		aModel = apps.get_model(app_label='db', model_name='lex_variant')
		aQuery = aModel.objects.filter(data__lex_variable_id=variableID).distinct()
		# print(aQuery)
		output['variants'] = []
		for aRow in aQuery:
			# print(aRow.id, len(aRow.data_set.all().values('by_inf').annotate(c=Count('by_inf'))), len(aRow.data_set.all().values('by_inf__for_district').annotate(c=Count('by_inf__for_district'))), len(aRow.data_set.all().values('by_inf__for_district__belongs_to').annotate(c=Count('by_inf__for_district__belongs_to'))))
			output['variants'].append({
				'id': aRow.id,
				'variant': aRow.variant,
				'group': [{
										'id': g.id,
										'group': { 'id': g.variantgroup_id, 'name': g.variantgroup.name } if g.variantgroup_id else None
									} for g in aRow.lex_variant_to_variantgroup_set.all()],
				'comment': aRow.comment,
				'str': str(aRow),
				'infCount': len(aRow.data_set.filter(lex_variable_id=variableID).values('by_inf').annotate(c=Count('by_inf')).order_by('by_inf')),
				'infDistCount': len(aRow.data_set.filter(lex_variable_id=variableID).values('by_inf__for_district').annotate(c=Count('by_inf__for_district')).order_by('by_inf__for_district')),
				'infBelongCount': len(aRow.data_set.filter(lex_variable_id=variableID).values('by_inf__for_district__belongs_to').annotate(c=Count('by_inf__for_district__belongs_to')).order_by('by_inf__for_district__belongs_to'))
			})
		output['count'] = len(aQuery)
	if output:
		return httpOutput(json.dumps(output), 'application/json')
	else:
		return httpOutput(json.dumps({'errors': 'No output!'}), 'application/json')
