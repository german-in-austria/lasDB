from django.conf.urls import include
from django.contrib import admin
from django.urls import path
import private_storage.urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('private-media/', include(private_storage.urls)),
    path('', include(('vue.urls', 'vue'), namespace='vue')),
]
