from lasDB.functions import httpOutput
from django.db.models import Q
from django.db.models import Count
import json


def view_export(request):
	if not request.user.is_authenticated:
		return httpOutput(json.dumps({'errors': 'Not authenticated!'}), 'application/json')
	# print(request.POST)
	if 'get' in request.POST:
		if request.POST.get('get') == 'variantgroups':
			return getVariantGroups(request)


def getVariantGroups(request):
	output = {}
	if 'id' in request.POST:
		from django.apps import apps
		aModel = apps.get_model(app_label='db', model_name='lex_variantgroup')
		aQuery = aModel.objects.get(id=request.POST.get('id'))
		output['variantgroup'] = {
			'id': aQuery.id,
			'name': aQuery.name,
			'description': aQuery.description,
			'legend_text': aQuery.legend_text,
			'original': aQuery.original,
			'origin_lang': (str(aQuery.origin_lang) + ' (' + str(aQuery.origin_lang_id) + ')') if aQuery.origin_lang else None,
			'frequency_category': aQuery.frequency_category,
			'status': aQuery.status,
			'onomatopoetic': aQuery.onomatopoetic,
			'comment': aQuery.comment,
			'type': (str(aQuery.type) + ' (' + str(aQuery.type_id) + ')') if aQuery.type else None,
			'str': str(aQuery)
		}
		aModel = apps.get_model(app_label='db', model_name='lex_variant')
		aQuery = aModel.objects.filter(lex_variant_to_variantgroup__variantgroup_id=request.POST.get('id')).distinct()
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
				'infCount': len(aRow.data_set.all().values('by_inf').annotate(c=Count('by_inf')).order_by('by_inf')),
				'infDistCount': len(aRow.data_set.all().values('by_inf__for_district').annotate(c=Count('by_inf__for_district')).order_by('by_inf__for_district')),
				'infBelongCount': len(aRow.data_set.all().values('by_inf__for_district__belongs_to').annotate(c=Count('by_inf__for_district__belongs_to')).order_by('by_inf__for_district__belongs_to'))
			})
		output['count'] = len(aQuery)
	if output:
		return httpOutput(json.dumps(output), 'application/json')
	else:
		return httpOutput(json.dumps({'errors': 'No output!'}), 'application/json')
