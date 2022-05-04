from lasDB.functions import httpOutput
from django.db.models import Q
import db.functions as dbFunc
import json


def view_form(request):
	if not request.user.is_authenticated:
		return httpOutput(json.dumps({'errors': 'Not authenticated!'}), 'application/json')
	if 'get' in request.POST:
		# print(request.POST)
		if request.POST.get('get') == 'getTables':
			return getTables(request)
		if request.POST.get('get') == 'getTable':
			return getTable(request)
		if request.POST.get('get') == 'getSelect':
			return getSelect(request)
		if request.POST.get('get') == 'getContent':
			return getContent(request)
		if request.POST.get('get') == 'setContent':
			return setContent(request)
		if request.POST.get('get') == 'getRelatedDbTable':
			return getRelatedDbTable(request)
		if request.POST.get('get') == 'delContent':
			return delContent(request)


def getTables(request):
	from django.apps import apps
	from django.conf import settings
	tables = []
	appList = settings.LASDB_APPLIST
	for aApp in appList:
		for model in apps.get_app_config(aApp).models.items():
			if str(model[0])[:4] != 'sys_':
				aModel = apps.get_model(aApp, model[0])
				tables.append({'name': str(model[0]), 'title': str(aModel._meta.verbose_name_plural) + ' (' + str(aModel.objects.count()) + ' Entries)'})
	return httpOutput(json.dumps(tables), 'application/json')


def getTable(request):
	output = {}
	if 'getModel' in request.POST:
		from db.functions_form import getForm
		[output['model'], output['options']] = getForm(request.POST.get('getModel'), request.POST.get('getOptions') if 'getOptions' in request.POST and request.POST.get('getOptions') else None)
	if output:
		return httpOutput(json.dumps(output), 'application/json')
	else:
		return httpOutput(json.dumps({'errors': 'No output!'}), 'application/json')


def getSelect(request):
	output = {}
	from django.apps import apps
	aModel = apps.get_model(app_label=request.POST.get('app'), model_name=request.POST.get('model'))
	aFieldName = request.POST.get('field')
	aField = aModel._meta.get_field(aFieldName)
	searchFilter = None
	if 'searchObj' in request.POST and hasattr(aModel._meta, 'search_fields'):
		searchObj = json.loads(request.POST.get('searchObj'))
		searchingString = searchObj['val'].strip()
		if len(searchingString) > 0:
			searchFilter = Q()
			for searchField in aModel._meta.search_fields:
				filter = searchField + '__icontains'
				searchFilter = searchFilter | Q(**{ filter: searchingString })
	filterFilter = []
	if 'filterObj' in request.POST and hasattr(aModel._meta, 'filter_fields'):
		filterObj = json.loads(request.POST.get('filterObj'))
		if filterObj:
			filterFound = False
			for fKey in filterObj:
				if fKey in aModel._meta.filter_fields:
					if filterObj[fKey]:
						filterFilter.append({ fKey: None if filterObj[fKey] == -1 else filterObj[fKey] })
						filterFound = True
			if not filterFound:
				filterFilter = []
	def getQueryWithExtraFilter(qObj):
		if filterFilter:
			for aFilter in filterFilter:
				qObj = qObj.filter(**aFilter)
		if searchFilter:
			qObj = qObj.filter(searchFilter)
		return qObj
	if 'getLists' in request.POST:
		aId = int(request.POST.get('id'))
		if aField.get_internal_type() == 'CharField':
			output['selectLists'] = [{'name': 'ALL', 'filter': 'all', 'count': getQueryWithExtraFilter(aModel.objects.all()).count(), 'open': False, 'loaded': False, 'loading': False, 'loadnext': 0, 'content': []}]
			for abc in list(map(chr, range(97, 123))):
				aQuery = getQueryWithExtraFilter(aModel.objects.filter(**{ aFieldName + '__istartswith': abc }))
				output['selectLists'].append({
					'name': abc.upper(),
					'filter': 'abc_' + abc,
					'count': aQuery.count(),
					'open': aQuery.filter(id=aId).count() > 0, 'loaded': False, 'loading': False, 'loadnext': 0, 'content': []
				})
			aQuery = getQueryWithExtraFilter(aModel.objects.filter(**{ aFieldName + '__iregex':'^([^a-z].+)' }))
			output['selectLists'].append({
				'name': 'Miscellaneous',
				'filter': 'abc_misc',
				'count': aQuery.count(),
				'open': aQuery.filter(id=aId).count() > 0, 'loaded': False, 'loading': False, 'loadnext': 0, 'content': []
			})
		else:
			output['selectLists'] = [{
				'name': aField.get_internal_type(),
				'filter': 'all',
				'count': getQueryWithExtraFilter(aModel.objects.all()).count(),
				'open': False, 'loaded': False, 'loading': False, 'loadnext': 0, 'content': []
			}]
	if 'getList' in request.POST:
		aFilter = request.POST.get('filter')
		aElements = None
		if aFilter == 'all':
			aElements = getQueryWithExtraFilter(aModel.objects.all())
		elif aFilter[0:4] == 'abc_':
			aLetter = aFilter[4:]
			if len(aLetter) == 1:
				aElements = getQueryWithExtraFilter(aModel.objects.filter(**{ aFieldName + '__istartswith': aLetter }))
			else:
				aElements = getQueryWithExtraFilter(aModel.objects.filter(**{ aFieldName + '__iregex':'^([^a-z].+)' }))
		if aElements:
			aLoadnext = int(request.POST.get('loadnext'))
			maxElements = 150
			aElementsCut = aElements[maxElements * aLoadnext : maxElements * aLoadnext + maxElements]
			aElementsCount = aElements.count()
			output['selectList'] = {
				'count': aElementsCount,
				'loadnext': (aLoadnext + 1) if maxElements * aLoadnext + maxElements < aElementsCount else -1,
				'content': [{ 'title': str(aElement), 'id': aElement.id } for aElement in aElementsCut]
			}
		else:
			output['selectList'] = { 'count': 0, 'loadnext': -1, 'content': [] }
	if output:
		return httpOutput(json.dumps(output), 'application/json')
	else:
		return httpOutput(json.dumps({'errors': 'No output!'}), 'application/json')


def getContent(request):
	output = {}
	from django.apps import apps
	if 'getValues' in request.POST:
		aModel = apps.get_model(app_label=request.POST.get('app'), model_name=request.POST.get('model'))
		aElement = aModel.objects.get(pk=int(request.POST.get('pk')))
		output['values'] = dbFunc.getElementValues(aModel, aElement)
		output['entryStr'] = str(aElement)
	if output:
		return httpOutput(json.dumps(output), 'application/json')
	else:
		return httpOutput(json.dumps({'errors': 'No output!'}), 'application/json')


def setContent(request):
	output = {}
	from django.apps import apps
	if 'setValues' in request.POST:
		# print(json.loads(request.POST.get('data')))
		aModel = apps.get_model(app_label=request.POST.get('app'), model_name=request.POST.get('model'))
		aPk = int(request.POST.get('pk'))
		if aPk > 0:
			aElement = aModel.objects.get(pk=aPk)
		else:
			aElement = aModel()
		for aKey, aFieldData in json.loads(request.POST.get('data')).items():
			aField = aModel._meta.get_field(aKey)
			if not aModel._meta.pk.name == aKey:
				aVal = aFieldData['val']
				# print(aKey, type(aVal), aVal, aField, aField.get_internal_type())
				if aField.get_internal_type() == 'ForeignKey':
					setattr(aElement, aKey + '_id', aVal)
				else:
					setattr(aElement, aKey, aVal)
		try:
			aElement.save()
			output['values'] = dbFunc.getElementValues(aModel, aElement)
			output['entryStr'] = str(aElement)
			output['saved'] = True
		except Exception as e:
			output['errors'] = 'Error: ' + str(type(e)) + ' - ' + str(e)
	if output:
		return httpOutput(json.dumps(output), 'application/json')
	else:
		return httpOutput(json.dumps({'errors': 'No output!'}), 'application/json')


def getRelatedDbTable(request):
	output = {}
	if 'getRelatedDbTable' in request.POST:
		from django.apps import apps
		aModel = apps.get_model(app_label='db', model_name=request.POST.get('getRelatedDbTable'))
		aQuery = aModel.objects.all().distinct()
		if 'onlyRelated' in request.POST and request.POST.get('onlyRelated'):
			aQuery = aQuery.exclude(**{ request.POST.get('getRelatedName'): None })
		output['countall'] = len(aQuery)
		if 'searchString' in request.POST and hasattr(aModel._meta, 'search_fields') and aModel._meta.search_fields:
			searchingString = request.POST.get('searchString').strip()
			searchFilter = Q()
			for searchField in aModel._meta.search_fields:
				filter = searchField + '__icontains'
				searchFilter = searchFilter | Q(**{ filter: searchingString })
			aQuery = aQuery.filter(searchFilter)
		if 'filter[]' in request.POST and request.POST.getlist('filter[]'):
			aFilter = request.POST.getlist('filter[]')
			aQuery = aQuery.filter(**{ aFilter[0]: aFilter[1] })
		output['all'] = [{
			'val': aRow.id,
			'str': str(aRow)
		} for aRow in aQuery]
		output['count'] = len(aQuery)
	if output:
		return httpOutput(json.dumps(output), 'application/json')
	else:
		return httpOutput(json.dumps({'errors': 'No output!'}), 'application/json')


def delContent(request):
	output = {}
	if 'delContent' in request.POST:
		from django.apps import apps
		aModel = apps.get_model(app_label=request.POST.get('app'), model_name=request.POST.get('model'))
		aElements = aModel.objects.filter(pk=int(request.POST.get('pk')))
		from django.contrib.admin.utils import NestedObjects
		from django.db import DEFAULT_DB_ALIAS
		collector = NestedObjects(using=DEFAULT_DB_ALIAS)
		collector.collect(aElements)
		if len(collector.nested()) > 1:
			output['errors'] = 'Related Objects would be deleted!'
		else:
			aElements.delete()
			output['deleted'] = True
	if output:
		return httpOutput(json.dumps(output), 'application/json')
	else:
		return httpOutput(json.dumps({'errors': 'No output!'}), 'application/json')
