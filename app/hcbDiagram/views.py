from django.apps import apps
from django.conf import settings
import json
from .models import sys_hcb_diagram_tableposition


def getModels(request):
  """Standard Anzeige für Model Diagramme."""
  # Modelposition speichern
  if 'save' in request.POST:
    positions = json.loads(request.POST.get('save'))
    for position in positions:
      try:
        amodel = sys_hcb_diagram_tableposition.objects.get(to_app=position['app'], to_model=position['model'])
      except:
        amodel = sys_hcb_diagram_tableposition()
        amodel.to_app = position['app']
        amodel.to_model = position['model']
      amodel.xt = position['xt']
      amodel.yt = position['yt']
      amodel.save()
  # Models auslesen
  tables = []
  appList = settings.LASDB_APPLIST
  for aApp in appList:
    for model in apps.get_app_config(aApp).models.items():
      if str(model[0])[:4] != 'sys_':
        amodel = apps.get_model(aApp, model[0])
        aFields = []
        xt = 0
        yt = 0
        try:
          asdtp = sys_hcb_diagram_tableposition.objects.get(to_app=aApp, to_model=str(model[0]))
          xt = asdtp.xt
          yt = asdtp.yt
        except:
          pass
        for f in amodel._meta.get_fields():
          if not f.auto_created or amodel._meta.pk.name == f.name:
            aField = {
              'field_name': f.name,
              'verbose_name': f._verbose_name,
              'internal_type': f.get_internal_type(),
              'unique': f.unique,
              'blank': f.blank,
              'null': f.null,
            }
            if amodel._meta.pk.name == f.name:
              aField['pk'] = True
            if f.is_relation:
              aField['related_db_table'] = f.related_model._meta.db_table
              aField['related_name'] = f.related_query_name()
              aField['related_db_table_count'] = f.related_model.objects.all().count()
              aField['related_db_table_count_related'] = f.related_model.objects.exclude(**{ aField['related_name']: None }).distinct().count()
            aFields.append(aField)
        tables.append({
          'model': model[0],
          'app': aApp,
          'verbose_name': str(amodel._meta.verbose_name),
          'verbose_name_plural': str(amodel._meta.verbose_name_plural),
          'count': amodel.objects.count(),
          'db_table': amodel._meta.db_table,
          'fields': aFields,
          'xt': xt,
          'yt': yt,
        })
  return tables
