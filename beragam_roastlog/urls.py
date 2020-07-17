"""beragam_roastlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin


from django.urls import include, path
from pages.views import base_view
from production.views import ChartData
from rest_framework.urlpatterns import format_suffix_patterns

admin.site.site_header = 'BERAGAM ROASTLOG'
admin.site.site_title = 'BERAGAM ROASTLOG SYS'
admin.site.index_title = 'ROASTERY DATABASE'





urlpatterns = [
    path('', admin.site.urls),
    path('products/', include('products.urls')),
    path('production/', include('production.urls')),
    path('test', base_view, name='base'),
    path('api/chart/data/', ChartData.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)

