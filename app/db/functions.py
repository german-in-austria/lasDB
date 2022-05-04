

def getModel(aModel):
  aFields = []
  for f in aModel._meta.get_fields():
    if not f.auto_created or aModel._meta.pk.name == f.name:
      aField = {
        'field_name': f.name,
        'verbose_name': f._verbose_name,
        'internal_type': f.get_internal_type(),
        'unique': f.unique,
        'blank': f.blank,
        'null': f.null,
      }
      if f.choices:
        aField['choices'] = f.choices
      if aModel._meta.pk.name == f.name:
        aField['pk'] = True
      if f.is_relation:
        aField['related_model'] = str(f.related_model._meta.model_name)
        aField['related_db_table'] = f.related_model._meta.db_table
        aField['related_name'] = f.related_query_name()
        aField['related_search_fields'] = f.related_model._meta.search_fields if hasattr(f.related_model._meta, 'search_fields') else []
        aField['related_db_table_count'] = f.related_model.objects.all().count()
        aField['related_db_table_count_related'] = f.related_model.objects.exclude(**{ aField['related_name']: None }).distinct().count()
      aFields.append(aField)
  return {
    'model': aModel.__name__,
    'app': 'db',
    'verbose_name': str(aModel._meta.verbose_name),
    'verbose_name_plural': str(aModel._meta.verbose_name_plural),
    'count': aModel.objects.count(),
    'db_table': aModel._meta.db_table,
    'ordering': aModel._meta.ordering,
    'fields': aFields,
    'search_fields': aModel._meta.search_fields if hasattr(aModel._meta, 'search_fields') else [],
    'filter_fields': aModel._meta.filter_fields if hasattr(aModel._meta, 'filter_fields') else []
  }


def getElementValues(aModel, aElement):
  aModel = aModel
  aObject = {}
  for f in aModel._meta.get_fields():
    if not f.auto_created or aModel._meta.pk.name == f.name:
      if f.get_internal_type() == 'ForeignKey':
        aObject[f.name] = { 'val': getattr(aElement, f.name + '_id'), 'str': str(getattr(aElement, f.name)) }
      else:
        aObject[f.name] = { 'val': getattr(aElement, f.name) }
  return aObject
