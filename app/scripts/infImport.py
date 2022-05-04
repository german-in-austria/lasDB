import db.models as dbModels
import re

def infImportTest():
  print('infImportTest')
  csvLines = open("scripts/infs-vol2-2021-03-26.csv", "r", encoding="utf-8")
  fields = ['las_county', 'las_numb', 'residency', 'grid', 'name', 'sex', 'age', 'residence_yrs', 'birth_inf', 'birth_mot', 'birth_fat', 'school', 'comment', 'multiple', 'multiple_age', 'multiple_res']
  statistic = {}
  knownBirthPlaces = 0
  unknownBirthPlaces = 0
  createdBirthPlaces = 0
  sameBirthPlaces = 0
  dg = 0
  for csvLine in csvLines:
    if dg > 0:
      dataLine = csvLine.strip().split(';')
      for cellNr, dataCell in enumerate(dataLine):
        dataCell = dataCell.strip()
        dataCell = re.sub(' +', ' ', dataCell)
        if fields[cellNr] not in statistic:
          statistic[fields[cellNr]] = {'null': 0, 'values': []}
        if not dataCell or dataCell == '–' or dataCell == '-':
          dataCell = None
        if not dataCell:
          statistic[fields[cellNr]]['null'] += 1
        else:
          addIt = True
          for aVal in statistic[fields[cellNr]]['values']:
            if aVal['val'] == dataCell:
              aVal['count'] += 1
              addIt = False
              break
          if addIt:
            statistic[fields[cellNr]]['values'].append({'val': dataCell, 'count': 1})
        dataLine[cellNr] = dataCell
      csv = csvLine.strip()
      # print(dg, str(dataLine).encode("ascii","ignore").decode('utf-8'))
      aElement = dbModels.informant()
      aElement.csv = str(csv)
      print('csv:', str(csv).encode("ascii","ignore").decode('utf-8'))
      aElement.volume = 2
      print('Zeile: ', dg)
      las_numb = dataLine[1]
      aElement.las_num = las_numb
      print('las_numb:', las_numb)
      name = dataLine[4]
      aElement.name_ini = name
      print('name:', str(name).encode("ascii","ignore").decode('utf-8'))
      if dataLine[5]:
        sex = 'f' if dataLine[5][0] == 'f' else 'm' if dataLine[5][0] == 'm' else None
      else:
        sex = None
      aElement.sex = sex
      age = dataLine[6]
      if age:
        age = int(age)
      aElement.age = age
      print('age:', age)
      residence_yrs = dataLine[7]
      if residence_yrs:
        if residence_yrs == 'since birth':
          residence_yrs = age
        else:
          residence_yrs = re.sub('·', '', residence_yrs)
          residence_yrs = re.sub('¼', '.25', residence_yrs)
          residence_yrs = re.sub('½', '.5', residence_yrs)
          residence_yrs = re.sub('¾', '.75', residence_yrs)
          if residence_yrs[0] == '.':
            residence_yrs = '0' + residence_yrs
          residence_yrs = float(residence_yrs)
      aElement.length_res = residence_yrs
      print('residence_yrs:', residence_yrs)
      aElement.school = True if 11 in dataLine and dataLine[11] else False
      print('school:', aElement.school)

      # loc_type -> 1 - lcounty, 2 - ltown, 3 - unknown
      lasCountry = dataLine[0]
      if lasCountry:
        lasCountryElement = dbModels.location.objects.filter(name=lasCountry)
        if lasCountryElement.count() > 0:
          lasCountryElement = lasCountryElement[0]
        else:
          lasCountryElement = dbModels.location()
          lasCountryElement.name = lasCountry
          lasCountryElement.type_id = 1 # lcounty
          lasCountryElement.save()
      else:
        lasCountryElement = None
      print('las_country:', str(lasCountry).encode("ascii","ignore").decode('utf-8'), '->', str(lasCountryElement).encode("ascii","ignore").decode('utf-8'))
      residency = dataLine[2]
      grid = re.sub(' *', '', str(dataLine[3])) if dataLine[3] else None
      if residency:
        residencyElement = dbModels.location.objects.filter(name=residency, grid_org=grid)
        if residencyElement.count() > 0:
          residencyElement = residencyElement[0]
        else:
          residencyElement = dbModels.location()
          residencyElement.name = residency
          residencyElement.grid_org = grid
          residencyElement.type_id = 2 # ltown
          residencyElement.belongs_to = lasCountryElement
          residencyElement.save()
          createdBirthPlaces += 1
      else:
        residencyElement = None
      aElement.for_district = residencyElement
      print('residency/grid:', str(residency).encode("ascii","ignore").decode('utf-8'),  str(grid).encode("ascii","ignore").decode('utf-8'), '->', str(residencyElement).encode("ascii","ignore").decode('utf-8'))

      birthPlaces = [
        { 'field': 'birth_inf', 'dbField': 'place_birth_inf', 'val': dataLine[8], 'element': None },
        { 'field': 'birth_mot', 'dbField': 'place_birth_mot', 'val': dataLine[9] if 9 in dataLine and dataLine[9] else None, 'element': None },
        { 'field': 'birth_fat', 'dbField': 'place_birth_fat', 'val': dataLine[10], 'element': None },
      ]
      for birthPlace in birthPlaces:
        if birthPlace['val'] == 'same':
          sameBirthPlaces += 1
          birthPlace['element'] = birthPlaces[0]['element']
        else:
          if residencyElement and residencyElement.name == birthPlace['val']:
            birthPlace['element'] = residencyElement
            knownBirthPlaces += 1
          else:
            birthPlace['element'] = dbModels.location.objects.filter(name=birthPlace['val'], type=3)
            if birthPlace['element'].count() > 0:
              birthPlace['element'] = birthPlace['element'][0]
            else:
              birthPlace['element'] = dbModels.location()
              birthPlace['element'].name = birthPlace['val']
              birthPlace['element'].type_id = 3 # unknown
              birthPlace['element'].save()
            unknownBirthPlaces += 1
        setattr(aElement, birthPlace['dbField'], birthPlace['element'])
        print(birthPlace['field'], str(birthPlace['val']).encode("ascii","ignore").decode('utf-8'), '->', str(birthPlace['element']).encode("ascii","ignore").decode('utf-8'))

      aElement.comment =  dataLine[12]
      print('comment', dataLine[12])
      if len(dataLine) > 13:
        multiple = dataLine[13]
        if multiple:
          multiple = int(multiple)
        aElement.multiple = multiple
        print('multiple', str(dataLine[13]).encode("ascii","ignore").decode('utf-8'))
        if len(dataLine) > 14:
          aElement.multiple_age = dataLine[14]
          print('multiple_age', str(dataLine[14]).encode("ascii","ignore").decode('utf-8'))
          if len(dataLine) > 15:
            aElement.multiple_res = dataLine[15]
            print('multiple_res', str(dataLine[15]).encode("ascii","ignore").decode('utf-8'))
      print(str(aElement).encode("ascii","ignore").decode('utf-8'))
      print('=========')
      aElement.save()
    dg += 1
  print('Statistik:', (dg - 1), 'Zeilen')
  print()
  for key in fields:
    if key in statistic:
      val = statistic[key]
      print(key + ':')
      print('-> Null:', val['null'])
      print('-> Different Values:', len(val['values']))
      print('-> Top5:')
      for top5 in sorted(val['values'], key = lambda i: i['count'], reverse=True)[:5]:
        print('      ', top5['count'], ' x ', top5['val'])
      print()
      # print(key, str(val).encode("ascii","ignore").decode('utf-8'))
  print('knownBirthPlaces:', knownBirthPlaces)
  print('unknownBirthPlaces:', unknownBirthPlaces)
  print('sameBirthPlaces:', sameBirthPlaces)
  print('createdBirthPlaces', createdBirthPlaces)
  # print(str(statistic).encode("ascii","ignore").decode('utf-8'))
  # print([aStat for aStat in statistic])
