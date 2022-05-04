from django.contrib import admin
from django.apps import apps


for model in apps.get_app_config('db').models.items():
	admin.site.register(apps.get_model("db", model[0]))
