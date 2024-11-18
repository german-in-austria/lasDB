from django.db import models

models.options.DEFAULT_NAMES += ('search_fields',)
models.options.DEFAULT_NAMES += ('filter_fields',)


class informant(models.Model):
  for_district = models.ForeignKey('location', on_delete=models.SET_NULL,
                                    blank=True, null=True)
  las_num = models.CharField(max_length=128,
                              db_index=True,
                              blank=True, null=True)
  place_residence = models.IntegerField(db_index=True, blank=True, null=True)
  name_ini = models.CharField(max_length=128,
                              db_index=True,
                              blank=True, null=True)
  CHOICE_SEX = (
      ('m', 'male'),
      ('f', 'female'),
  )
  sex = models.CharField(max_length=1,
                          choices=CHOICE_SEX,
                          db_index=True,
                          blank=True, null=True)
  age = models.IntegerField(blank=True, null=True)
  length_res = models.FloatField(blank=True, null=True)
  place_birth_inf = models.ForeignKey('location',
                                      on_delete=models.SET_NULL,
                                      related_name="informant_place_birth_inf",
                                      blank=True, null=True)
  place_birth_mot = models.ForeignKey('location',
                                      on_delete=models.SET_NULL,
                                      related_name="informant_place_birth_mot",
                                      blank=True, null=True)
  place_birth_fat = models.ForeignKey('location',
                                      on_delete=models.SET_NULL,
                                      related_name="informant_place_birth_fat",
                                      blank=True, null=True)
  school = models.BooleanField(default=False)
  comment = models.TextField(blank=True, null=True)
  multiple = models.IntegerField(blank=True, null=True)
  multiple_res = models.CharField(max_length=512,
                                  blank=True, null=True)
  multiple_age = models.CharField(max_length=512,
                                  blank=True, null=True)
  volume = models.IntegerField()
  csv = models.CharField(max_length=512,
                          blank=True, null=True)

  def __str__(self):
    return (self.las_num if self.las_num and len(self.las_num) > 0 else '?') + ' (' + (self.name_ini if self.name_ini else '?') + ', ' + (str(self.age) if self.age else '?') + ', ' + (self.sex if self.sex else '?') + ', ' + (self.for_district.belongs_to.name if self.for_district and self.for_district.belongs_to else '?') + ')'

  class Meta:
    verbose_name = "informant"
    verbose_name_plural = "informants"
    ordering = ('las_num',)
    default_permissions = ()
    search_fields = ['las_num', 'name_ini', 'for_district__belongs_to__name']
    filter_fields = ['for_district', 'for_district__belongs_to__name']


class location(models.Model):
  name = models.CharField(max_length=128, db_index=True, blank=True, null=True)
  grid_org = models.CharField(max_length=128, db_index=True, blank=True, null=True)
  osm_id = models.BigIntegerField(blank=True, null=True)
  osm_type = models.CharField(max_length=128,
                              blank=True, null=True)
  lon_new = models.FloatField(blank=True, null=True)
  lat_new = models.FloatField(blank=True, null=True)
  lon_imp = models.FloatField(blank=True, null=True)
  lat_imp = models.FloatField(blank=True, null=True)
  belongs_to = models.ForeignKey('location',
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
  type = models.ForeignKey('loc_type',
                           on_delete=models.SET_NULL,
                           blank=True, null=True)
  comment = models.TextField(blank=True, null=True)
  geodata = models.TextField(blank=True, null=True)
  sort = models.IntegerField(blank=True, null=True)
  controlled = models.BooleanField(default=False)

  def __str__(self):
    return str(self.name) + ' (' + str(self.grid_org) + ((', ' + str(self.belongs_to.name)) if self.belongs_to else '') + ')'

  class Meta:
    verbose_name = "location"
    verbose_name_plural = "locations"
    ordering = ('name',)
    default_permissions = ()
    search_fields = ['name', 'belongs_to__name']
    filter_fields = ['type', 'belongs_to']


class loc_type(models.Model):
  name = models.CharField(db_index=True, max_length=128)
  description = models.CharField(max_length=128,
                                 blank=True, null=True)
  comment = models.TextField(blank=True, null=True)

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = "loc_type"
    verbose_name_plural = "loc_types"
    ordering = ('name',)
    default_permissions = ()
    search_fields = ['name']


class data(models.Model):
  lex_variable = models.ForeignKey('lex_variable', on_delete=models.SET_NULL)
  lex_variant = models.ForeignKey('lex_variant', on_delete=models.SET_NULL)
  by_inf = models.ForeignKey('informant', on_delete=models.SET_NULL)
  semantic_special = models.CharField(max_length=128,
                                      blank=True, null=True)
  comment = models.TextField(blank=True, null=True)
  pdf_ocr_identifier = models.TextField(blank=True, null=True)
  pdf_filename = models.CharField(max_length=128, blank=True, null=True)
  pdf_page = models.IntegerField(blank=True, null=True)
  sort = models.IntegerField(blank=True, null=True)
  plus = models.BooleanField(default=False)
  star = models.BooleanField(default=False)
  italics = models.BooleanField(default=False)
  superscript = models.CharField(max_length=2, blank=True, null=True)

  def __str__(self):
    return str(self.lex_variable) + ', ' + str(self.lex_variant) + ', ' + str(self.by_inf) + ', ' + str(self.by_inf)

  class Meta:
    verbose_name = "data"
    verbose_name_plural = "datas"
    ordering = ('lex_variable',)
    default_permissions = ()
    filter_fields = ['by_inf', 'lex_variable', 'lex_variant']


class lex_variable(models.Model):
  variable = models.CharField(db_index=True, max_length=256)
  in_question = models.ForeignKey('questions',
                                  on_delete=models.SET_NULL,
                                  blank=True, null=True)
  comment = models.TextField(blank=True, null=True)
  pdf_ocr_identifier = models.TextField(blank=True, null=True)

  def __str__(self):
    return self.variable + ' (' + str(self.in_question.question_number) + ', ' + str(self.in_question.survey_number) + ')'

  class Meta:
    verbose_name = "lex_variable"
    verbose_name_plural = "lex_variables"
    ordering = ('variable',)
    default_permissions = ()
    search_fields = ['variable']


class lex_variant(models.Model):
  variant = models.CharField(db_index=True, max_length=128)
  comment = models.TextField(blank=True, null=True)

  def __str__(self):
      return self.variant

  class Meta:
    verbose_name = "lex_variant"
    verbose_name_plural = "lex_variants"
    ordering = ('variant',)
    default_permissions = ()
    search_fields = ['variant']


class questions(models.Model):
  survey_number = models.IntegerField()
  question_number = models.CharField(max_length=128)
  postal_survey = models.BooleanField(default=True)
  question = models.TextField()
  question_type = models.CharField(max_length=128,
                                   blank=True, null=True)
  comment = models.TextField(blank=True, null=True)

  def __str__(self):
    aQuestion = self.question
    if len(aQuestion) > 16:
      aQuestion = aQuestion[:12] + '...'
    return 'PQ' + str(self.survey_number) + ' - ' + self.question_number + ' - ' + aQuestion

  class Meta:
    verbose_name = "question"
    verbose_name_plural = "questions"
    ordering = ('survey_number',)
    default_permissions = ()
    search_fields = ['question']


class map(models.Model):
  name = models.CharField(max_length=128,
                          db_index=True,
                          blank=True, null=True)
  title = models.CharField(max_length=128,
                           db_index=True,
                           blank=True, null=True)
  legend_title = models.CharField(max_length=128,
                           db_index=True,
                           blank=True, null=True)
  public = models.BooleanField(default=False)
  description = models.TextField(blank=True, null=True)
  comment = models.TextField(blank=True, null=True)

  def __str__(self):
    return (str(self.name) if self.name else str(self.legend_title)) + ('' if self.public else ' - PRIVATE')

  class Meta:
    verbose_name = "map"
    verbose_name_plural = "maps"
    ordering = ('name',)
    default_permissions = ()
    search_fields = ['name']


class lex_variantgroup(models.Model):
  name = models.CharField(max_length=128,
                          db_index=True,
                          blank=True, null=True)
  lex_variable = models.ForeignKey('lex_variable',
                           on_delete=models.SET_NULL,
                           blank=True, null=True)
  description = models.TextField(blank=True, null=True)
  legend_text = models.CharField(max_length=128,
                                 blank=True, null=True)
  original = models.BooleanField(default=False)
  origin_lang = models.ForeignKey('languages',
                           on_delete=models.SET_NULL,
                           blank=True, null=True)
  CHOICE_FC = (
      ('major', 'major'),
      ('minor', 'minor'),
      ('oncer', 'oncer'),
  )
  frequency_category =  models.CharField(max_length=16,
                          choices=CHOICE_FC,
                          db_index=True,
                          blank=True, null=True)
  CHOICE_STATUS = (
      ('denotans', 'denotans'),
      ('non-denotans', 'non-denotans'),
      ('unkown', 'unkown'),
      ('mistaken', 'mistaken'),
      ('idiosyncratic', 'idiosyncratic'),
  )
  status =  models.CharField(max_length=16,
                          choices=CHOICE_STATUS,
                          db_index=True,
                          blank=True, null=True)
  onomatopoetic = models.BooleanField(default=False)
  comment = models.TextField(blank=True, null=True)
  type = models.ForeignKey('lex_variantgroup_types',
                           on_delete=models.SET_NULL,
                           blank=True, null=True)

  def __str__(self):
    return self.name + ' (' + str(self.lex_variable) + ')'

  class Meta:
    verbose_name = "lex_variantgroup"
    verbose_name_plural = "lex_variantgroups"
    ordering = ('name',)
    default_permissions = ()
    search_fields = ['name']
    filter_fields = ['lex_variable']


class languages(models.Model):
  short_name = models.CharField(max_length=128,
                          db_index=True)
  name = models.CharField(max_length=128,
                          db_index=True)
  description = models.TextField(blank=True, null=True)
  comment = models.TextField(blank=True, null=True)

  def __str__(self):
    return self.short_name + ' - ' + self.name

  class Meta:
    verbose_name = "language"
    verbose_name_plural = "languages"
    ordering = ('short_name', 'name',)
    default_permissions = ()
    search_fields = ['short_name', 'name']


class lex_variantgroup_types(models.Model):
  name = models.CharField(max_length=128,
                          db_index=True,
                          blank=True, null=True)
  description = models.TextField(blank=True, null=True)
  example = models.TextField(blank=True, null=True)

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = "lex_variantgroup_types"
    verbose_name_plural = "lex_variantgroup_types"
    ordering = ('name',)
    default_permissions = ()
    search_fields = ['name']


class lex_variant_to_variantgroup(models.Model):
  lex_variant = models.ForeignKey('lex_variant',
                                  blank=True, null=True,
                                  on_delete=models.SET_NULL)
  variantgroup = models.ForeignKey('lex_variantgroup',
                                   on_delete=models.SET_NULL,
                                   blank=True, null=True)
  order = models.IntegerField(blank=True, null=True)

  def __str__(self):
    return str(self.lex_variant) + ' -> ' + str(self.variantgroup)

  class Meta:
    verbose_name = "lex_variant_to_variantgroup"
    verbose_name_plural = "lex_variant_to_variantgroups"
    ordering = ('order', 'lex_variant',)
    default_permissions = ()


class map_to_variantgroup(models.Model):
  map = models.ForeignKey('map',
                          on_delete=models.SET_NULL)
  variantgroup = models.ForeignKey('lex_variantgroup',
                                   on_delete=models.SET_NULL)
  order = models.IntegerField(blank=True, null=True)
  preset_color = models.CharField(max_length=7,
                                  blank=True, null=True)

  def __str__(self):
    return str(self.map) + ' -> ' + str(self.variantgroup)

  class Meta:
    verbose_name = "map_to_variantgroup"
    verbose_name_plural = "maps_to_variantgroups"
    ordering = ('order',)
    default_permissions = ()


class pdf_file(models.Model):
  filename = models.CharField(max_length=256,
                              db_index=True,
                              unique=True)
  title = models.CharField(max_length=256,
                            db_index=True,
                            blank=True, null=True)
  edit_data = models.BooleanField(default=False)
  options = models.TextField(blank=True, null=True)
  page_options = models.TextField(blank=True, null=True)
  comment = models.TextField(blank=True, null=True)

  def __str__(self):
    return str(self.filename) + ' (' + str(self.title) + ')'

  class Meta:
    verbose_name = "PDF File"
    verbose_name_plural = "PDF Files"
    ordering = ('filename',)
    default_permissions = ()
    search_fields = ['filename', 'title', 'comment']
