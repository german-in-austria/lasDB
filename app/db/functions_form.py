from django.apps import apps
import db.functions as dbFunc


def getForm(modelName, options):
  aModel = apps.get_model(app_label='db', model_name=modelName)
  aModelObj = dbFunc.getModel(aModel)
  if options:
    if options == 'informant':
      aOutputObj = getBaseOptions(aModelObj, {
        'name_ini': { 'width': 25 },
        'multiple': { 'width': 33.3 },
        'multiple_res': { 'width': 33.3 },
        'multiple_age': { 'width': 33.3 },
        'csv': { 'show': False }
      })
    elif options == 'location':
      aOutputObj = getBaseOptions(aModelObj, {
        'name': { 'width': 100 },
        'grid_org': { 'width': 100 },
        'osm_id': { 'width': 50 },
        'lon_imp': { 'nl': True },
        'belongs_to': { 'nl': True },
        'type': { 'nl': True }
      })
    else:
      print('getForm - options - unknown', options)
      aOutputObj = getBaseOptions(aModelObj)
    aOutputObj['name'] = options
  else:
    aOutputObj = getBaseOptions(aModelObj)
  return [aModelObj, aOutputObj]


def getBaseOptions(modelObj, options = None):
  # Automatic Options
  fWidths = {
    'default': 100,
    'choices': 25,
    'AutoField': 100,
    'ForeignKey': 25,
    'BooleanField': 25,
    'TextField': 100,
    'CharField': 50,
    'IntegerField': 25,
    'FloatField': 25
  }
  aOutput = {
    'name': None,
    'fields': [],
    'ordering': modelObj['ordering']
  }
  for aField in modelObj['fields']:
    aFieldOptions = {
      'field_name': aField['field_name'],
      'width': fWidths['choices'] if 'choices' in aField else fWidths[aField['internal_type']] if aField['internal_type'] in fWidths else fWidths['default'],
      'show': True
    }
    if options and aField['field_name'] in options:
      for aOptionKey in options[aField['field_name']]:
        aFieldOptions[aOptionKey] = options[aField['field_name']][aOptionKey]
    aOutput['fields'].append(aFieldOptions)
  return aOutput
