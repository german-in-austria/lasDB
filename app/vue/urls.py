from django.conf.urls import include
from django.urls import path
from . import views


urlpatterns = [
	path('system/', views.system, name='system'),
	path('tools/diagram/', views.hcbDiagram, name='hcbDiagram'),
	path('tools/map/', views.toolMap, name='toolMap'),
	path('editData/', views.editData, name='editData'),
	path('form/', views.form, name='form'),
	path('variantgroups/', views.variantgroups, name='variantgroups'),
	path('maptovariantgroups/', views.mapToVariantgroups, name='maptovariantgroups'),
	path('maps/', views.maps, name='maps'),
	path('export/', views.export, name='export'),
	path('', views.start, name='start'),
]
