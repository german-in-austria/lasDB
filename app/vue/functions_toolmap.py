from lasDB.functions import httpOutput
import json
from db.models import location, loc_type


def view_toolmap(request):
	if not request.user.is_authenticated:
		return httpOutput(json.dumps({'errors': 'Not authenticated!'}), 'application/json')
	if 'get' in request.POST:
		if request.POST.get('get') == 'getLocations':
			return getLocations(request)
	if 'set' in request.POST:
		if request.POST.get('set') == 'setLocations':
			return setLocations(request)


def getLocations(request):
	types = [
		{
			'id': aType.id,
			'name': aType.name,
			'description': aType.description,
			'comment': aType.comment
		}
		for aType in loc_type.objects.all()
	]
	locations = []
	for aLocation in location.objects.all():
		locations.append({
			'id': aLocation.id,
			'name': aLocation.name,
			'grid_org': aLocation.grid_org,
			'osm_id': aLocation.osm_id,
			'osm_type': aLocation.osm_type,
			'lon_new': aLocation.lon_new,
			'lat_new': aLocation.lat_new,
			'lon_imp': aLocation.lon_imp,
			'lat_imp': aLocation.lat_imp,
			'belongs_to': aLocation.belongs_to_id,
			'type': aLocation.type_id,
			'comment': aLocation.comment,
			'geodata': aLocation.geodata,
			'controlled': aLocation.controlled,
			'informants': [{
				'id': aInf.id,
				'las_num': aInf.las_num
			} for aInf in aLocation.informant_set.all().order_by('las_num')]
		})
	return httpOutput(json.dumps({'locations': locations, 'types': types}), 'application/json')


def setLocations(request):
	# print('setLocations', request.POST)
	for sLocation in json.loads(request.POST.get('locations')):
		lElement = location.objects.get(id=sLocation['id'])
		lElement.name = sLocation['name']
		lElement.grid_org = sLocation['grid_org']
		lElement.osm_id = sLocation['osm_id']
		lElement.osm_type = sLocation['osm_type']
		lElement.lon_new = sLocation['lon_new']
		lElement.lat_new = sLocation['lat_new']
		lElement.lon_imp = sLocation['lon_imp']
		lElement.lat_imp = sLocation['lat_imp']
		lElement.belongs_to_id = sLocation['belongs_to']
		lElement.type_id = sLocation['type']
		lElement.comment = sLocation['comment']
		lElement.geodata = sLocation['geodata']
		lElement.controlled = sLocation['controlled']
		lElement.save()
	return httpOutput(json.dumps({'saved': True}), 'application/json')
