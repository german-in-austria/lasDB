from lasDB.functions import httpOutput
import json
from django.conf import settings
import os
from db.models import pdf_file, location, loc_type, informant, lex_variable, questions, data, lex_variant


def view_editData(request):
  if not request.user.is_authenticated:
    return httpOutput(json.dumps({'errors': 'Not authenticated!'}), 'application/json')
  if 'get' in request.POST:
    if request.POST.get('get') == 'getPdfFiles':
      return getPdfFiles(request)
    if request.POST.get('get') == 'getBaseData':
      return getBaseData(request)
    if request.POST.get('get') == 'getVariableByOCR':
      return getVariableByOCR(request)
    if request.POST.get('get') == 'getVariableData':
      return getVariableData(request)
    if request.POST.get('get') == 'searchVariant':
      return searchVariant(request)
  if 'set' in request.POST:
    if request.POST.get('set') == 'setPdfOptions':
      return setPdfOptions(request)
    if request.POST.get('set') == 'setVariableByOCR':
      return setVariableByOCR(request)
    if request.POST.get('set') == 'saveData':
      return saveData(request)
    if request.POST.get('set') == 'deleteData':
      return deleteData(request)


def getPdfFiles(request):
  output = {}
  output['pdfFiles'] = []
  filePath = os.path.join(settings.PRIVATE_STORAGE_ROOT, 'pdf')
  for aFile in sorted(os.listdir(filePath)):
    if aFile[-4:].lower() == '.pdf':
      aQuery = pdf_file.objects.filter(filename=aFile)
      if aQuery.count() < 2:
        aFileData = {'filename': aFile, 'size': os.path.getsize(os.path.join(filePath, aFile))}
        if aQuery.count() == 0:
          aElement = pdf_file()
          aElement.filename = aFile
          aElement.save()
        elif aQuery.count() == 1:
          aElement = aQuery[0]
        aFileData['title'] = aElement.title
        aFileData['edit_data'] = aElement.edit_data
        aFileData['options'] = aElement.options
        aFileData['page_options'] = aElement.page_options
        aFileData['comment'] = aElement.comment
        output['pdfFiles'].append(aFileData)
  if output:
    return httpOutput(json.dumps(output), 'application/json')
  else:
    return httpOutput(json.dumps({'errors': 'No output!'}), 'application/json')


def setPdfOptions(request):
  aData = json.loads(request.POST.get('data'))
  aQuery = pdf_file.objects.filter(filename=aData['filename'])
  if aQuery.count() == 0:
    return httpOutput(json.dumps({'errors': 'File not found!'}), 'application/json')
  elif aQuery.count() == 1:
    aElement = aQuery[0]
    aElement.title = aData['title']
    aElement.edit_data = aData['edit_data']
    aElement.options = json.dumps(aData['options'])
    aElement.page_options = json.dumps(aData['page_options'])
    aElement.comment = aData['comment']
    aElement.save()
    return httpOutput(json.dumps({'ok': True}), 'application/json')
  return httpOutput(json.dumps({'errors': 'Multiple Files found!'}), 'application/json')


def getBaseData(request):
  type = [
    {
      'id': aType.id,
      'name': aType.name,
      'description': aType.description,
      'comment': aType.comment
    }
    for aType in loc_type.objects.all()
  ]
  locations = []
  for aLocation in location.objects.filter(type_id__in=[1, 2]):
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
      'sort': aLocation.sort,
      'controlled': aLocation.controlled
    })
  informants = [
    {
      'id': aInf.id,
      'volume': aInf.volume,
      'las_num': aInf.las_num,
      'for_district': aInf.for_district_id
    }
    for aInf in informant.objects.filter(las_num__gt = 0)
  ]
  # for_district
  return httpOutput(json.dumps({'loc_types': type, 'locations': locations, 'informants': informants}), 'application/json')


def getVariableByOCR(request):
  ocrId = request.POST.get('ocrId')
  aQuery = lex_variable.objects.filter(pdf_ocr_identifier__icontains=ocrId)
  if aQuery and len(aQuery) > 0:
    aQuery = aQuery[0].id
  else:
    aQuery = -1
  aQuestion = [
    {
      'id': aQuest.id,
      'survey_number': aQuest.survey_number,
      'question_number': aQuest.question_number,
      'postal_survey': aQuest.postal_survey,
      'question': aQuest.question,
      'question_type': aQuest.question_type,
      'comment': aQuest.comment
    }
    for aQuest in questions.objects.filter(survey_number=request.POST.get('survey_number'), question_number=request.POST.get('question_number'))
  ]
  return httpOutput(json.dumps({'ocrId': ocrId, 'variableId': aQuery, 'question': aQuestion}), 'application/json')


def setVariableByOCR(request):
  aData = json.loads(request.POST.get('data'))
  qId = aData['in_question']['id']
  if qId < 0:
    nQuestion = questions()
    nQuestion.survey_number = aData['in_question']['survey_number']
    nQuestion.question_number = aData['in_question']['question_number']
    nQuestion.postal_survey = aData['in_question']['postal_survey']
    nQuestion.question = aData['in_question']['question']
    nQuestion.question_type = aData['in_question']['question_type']
    nQuestion.comment = aData['in_question']['comment']
    nQuestion.save()
    qId = nQuestion.id
  nVariable = lex_variable()
  nVariable.variable = aData['variable']
  nVariable.in_question_id = qId
  nVariable.comment = aData['comment']
  nVariable.pdf_ocr_identifier = aData['pdf_ocr_identifier']
  nVariable.save()
  return httpOutput(json.dumps({'ok': True, 'variableId': nVariable.id}), 'application/json')


def getVariableData(request):
  lexVariable = []
  for aVariable in lex_variable.objects.filter(id=request.POST.get('id')):
    lexVariable.append({
      'id': aVariable.id,
      'variable': aVariable.variable,
      'in_question': {
        'id': aVariable.in_question.id,
        'survey_number': aVariable.in_question.survey_number,
        'question_number': aVariable.in_question.question_number,
        'postal_survey': aVariable.in_question.postal_survey,
        'question': aVariable.in_question.question,
        'question_type': aVariable.in_question.question_type,
        'comment': aVariable.in_question.comment,
      },
      'comment': aVariable.comment,
      'pdf_ocr_identifier': aVariable.pdf_ocr_identifier,
    })
  variantIds = []
  dData = []
  if len(lexVariable) > 0:
    for aData in data.objects.filter(lex_variable=lexVariable[0]['id']).order_by('sort'):
      if aData.lex_variant_id not in variantIds:
        variantIds.append(aData.lex_variant_id)
      dData.append({
        'id': aData.id,
        'lex_variable': aData.lex_variable_id,
        'lex_variant': aData.lex_variant_id,
        'by_inf': aData.by_inf_id,
        'semantic_special': aData.semantic_special,
        'comment': aData.comment,
        'pdf_ocr_identifier': aData.pdf_ocr_identifier,
        'pdf_filename': aData.pdf_filename,
        'pdf_page': aData.pdf_page,
        'sort': aData.sort,
        'plus': aData.plus,
        'star': aData.star,
        'italics': aData.italics,
        'superscript': aData.superscript
      })
  # print(variantIds)
  variants = []
  if len(variantIds) > 0:
    for aVariant in lex_variant.objects.filter(id__in=variantIds):
      variants.append({
        'id': aVariant.id,
        'variant': aVariant.variant,
        'comment': aVariant.comment
      })
  return httpOutput(json.dumps({'ok': True, 'lex_variable': lexVariable, 'data': dData, 'lex_variant': variants}), 'application/json')


def searchVariant(request):
  variants = [
    {
      'id': aVariant.id,
      'variant': aVariant.variant
    }
    for aVariant in lex_variant.objects.filter(variant__icontains=request.POST.get('str'))
  ]
  return httpOutput(json.dumps({'ok': True, 'variants': variants}), 'application/json')


def saveData(request):
  aData = json.loads(request.POST.get('data'))
  # print('saveData', aData)
  aPlaceId = aData['placeId']
  for aVariant in aData['variants']:
    aVarId = aVariant['id']
    aOcrId = aVariant['variantInfsOcrId'] if 'variantInfsOcrId' in aVariant else None
    aPdfFilename = aVariant['pdfFilename'] if 'pdfFilename' in aVariant else None
    aPdfPage = aVariant['pdfPage'] if 'pdfPage' in aVariant else None
    aSort = aVariant['sort'] if 'sort' in aVariant else None
    # print(aOcrId)
    if aVarId < 1:
      aVarStr = aVariant['variantText'].strip()
      aVarQuery, aVarCreated = lex_variant.objects.get_or_create(variant__exact=aVarStr)
      if aVarCreated:
        aVarQuery.variant = aVarStr
        aVarQuery.save()
      aVarId = aVarQuery.id
    # Get Data
    oldDataQuery = [d.id for d in data.objects.filter(lex_variable_id=aData['variableId'], lex_variant_id=aVarId, by_inf__for_district__belongs_to_id=aPlaceId)]
    # print('data - old', oldDataQuery)
    aDg = 0
    for aInf in aVariant['informants']['list']:
      aDataQuery, aDataCreated = data.objects.get_or_create(lex_variable_id=aData['variableId'], lex_variant_id=aVarId, by_inf_id=aInf['infObj']['id'])
      if aOcrId:
        aDataQuery.pdf_ocr_identifier = aOcrId
      if aPdfFilename:
        aDataQuery.pdf_filename = aPdfFilename
      if aPdfPage:
        aDataQuery.pdf_page = aPdfPage
      aDataQuery.sort = aDg
      aDataQuery.plus = aInf['plus'] if 'plus' in aInf else False
      aDataQuery.star = aInf['star'] if 'star' in aInf else False
      aDataQuery.italics = aInf['italics'] if 'italics' in aInf else False
      aDataQuery.superscript = aInf['superscript'] if 'superscript' in aInf else False
      aDataQuery.save()
      if aDataQuery.id in oldDataQuery:
        oldDataQuery.remove(aDataQuery.id)
      aDg += 1
      # print('aData', aInf['id'], aDataCreated, str(aDataQuery))
    # print('data - remove', oldDataQuery)
    if oldDataQuery:
      data.objects.filter(id__in=oldDataQuery).delete()
    # ToDo ...
  return httpOutput(json.dumps({'ok': True}), 'application/json')


def deleteData(request):
  aData = json.loads(request.POST.get('data'))
  aPlaceId = aData['placeId']
  for aVariant in aData['variants']:
    aVarId = aVariant['id']
    data.objects.filter(lex_variable_id=aData['variableId'], lex_variant_id=aVarId, by_inf__for_district__belongs_to_id=aPlaceId).delete()
  return httpOutput(json.dumps({'ok': True}), 'application/json')
