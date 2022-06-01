from lasDB.functions import httpOutput
import json
from db.models import map, map_to_variantgroup, location, lex_variable, lex_variant


def view_maps(request):
	if 'get' in request.POST:
		if request.POST.get('get') == 'maps':
			return getMaps(request)
		if request.POST.get('get') == 'map':
			return getMap(request)
		if request.POST.get('get') == 'variants':
			return getVariants(request)
		if request.POST.get('get') == 'variantsMap':
			return getVariantsMap(request)


def getMaps(request):
	maps = []
	mapQuery = map.objects.filter(public=True)
	if request.user.is_authenticated:
		mapQuery = map.objects.all()
	for aMap in mapQuery:
		maps.append({
			'id': aMap.id,
			'name': aMap.name,
			'title': aMap.title,
			'legend_title': aMap.legend_title,
			'comment': aMap.comment,
			'description': aMap.description
		})
	variables = []
	for aVariable in lex_variable.objects.all():
		variables.append({
			'id': aVariable.id,
			'variable': aVariable.variable,
			'in_question': str(aVariable.in_question),
			'comment': aVariable.comment
		})
	locations = []
	for loc in location.objects.all():
		locations.append({
			'id': loc.id,
			'name': loc.name,
			'lon_new': loc.lon_new,
			'lat_new': loc.lat_new,
			'osm_id': loc.osm_id,
			'osm_type': loc.osm_type,
			'belongs_to': loc.belongs_to_id
		})
	return httpOutput(json.dumps({'maps': maps, 'locations': locations, 'variables': variables}), 'application/json')


def getMap(request):
	vg = []
	for aMapToVar in map_to_variantgroup.objects.filter(map=request.POST.get('mapId')):
		variants = []
		# print('aMapToVar', aMapToVar, aMapToVar.variantgroup, aMapToVar.variantgroup.lex_variant_to_variantgroup_set.all().count())
		for variant in aMapToVar.variantgroup.lex_variant_to_variantgroup_set.select_related('lex_variant').all():
			# print('variant', variant, 'lex_variant', variant.lex_variant)
			# print('lex_variable_id', aMapToVar.variantgroup.lex_variable_id)
			aDS = variant.lex_variant.data_set.select_related('by_inf')
			if aMapToVar.variantgroup.lex_variable_id:
				aDS = aDS.filter(lex_variable_id=aMapToVar.variantgroup.lex_variable_id)
			vData = []
			for data in aDS.all():
				vData.append({
					'id': data.id,
					'infId': data.by_inf.id,
					'fDist': data.by_inf.for_district_id,
					'biInf': data.by_inf.place_birth_inf_id,
					'biMot': data.by_inf.place_birth_mot_id,
					'biFat': data.by_inf.place_birth_fat_id
				})
			variants.append({
				'id': variant.lex_variant.id,
				'variant': variant.lex_variant.variant,
				'data': vData
			})
		vg.append({
			'id': aMapToVar.id,
			'variantgroup': {
				'str': str(aMapToVar.variantgroup),
				'name': aMapToVar.variantgroup.name,
				'legendText': aMapToVar.variantgroup.legend_text,
				'variants': variants
			},
			'preset_color': aMapToVar.preset_color
		})
	return httpOutput(json.dumps({'vg': vg}), 'application/json')


def getVariants(request):
	variants = []
	for aVariant in lex_variant.objects.filter(data__lex_variable_id=request.POST.get('variableId')).distinct():
		variants.append({
			'id': aVariant.id,
			'variant': aVariant.variant,
			'comment': aVariant.comment
		})
	return httpOutput(json.dumps({'variants': variants}), 'application/json')


def getVariantsMap(request):
	variants = []
	print(request.POST.get('variableId'), request.POST.getlist('variantIds[]'))
	# variableId variantIds
	variableId = request.POST.get('variableId')
	for variantId in request.POST.getlist('variantIds[]'):
		variant = lex_variant.objects.get(id=variantId)
		print(variantId, variantId, variant)
		vData = []
		for data in variant.data_set.select_related('by_inf').filter(lex_variable_id=variableId):
			vData.append({
				'id': data.id,
				'infId': data.by_inf.id,
				'fDist': data.by_inf.for_district_id,
				'biInf': data.by_inf.place_birth_inf_id,
				'biMot': data.by_inf.place_birth_mot_id,
				'biFat': data.by_inf.place_birth_fat_id
			})
		variants.append({
			'id': variant.id,
			'variant': variant.variant,
			'data': vData
		})
	return httpOutput(json.dumps({'variants': variants}), 'application/json')
