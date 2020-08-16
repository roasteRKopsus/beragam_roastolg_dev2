from django.urls import path, include
from .views import *
from .models import ProductionDiv

app_name = 'production'
urlpatterns = [
    path('', production_list_view, name='production-list'),
    path('filter', search_2, name='search-2'),
    path('create/', production_create_view, name='production-list'),
    path('karantina/', production_karantina_production_view, name='production-karantina'),
    path('karantina/', production_karantina_qc_view, name='production-karantina'),
    path('<int:id>/', production_detail_view, name='production-detail'),
    path('<int:id>/update/', production_update_view, name='production-update'),
    path('<int:id>/delete/', production_delete_view, name='production-delete'),
    path('statistik', production_karantina_chart, name='charts-produksi-karantina'),
    path('compilestat', StatsView.as_view(), name='stats'),
    path('blendreport-api', StatsView.as_view(), name='stats'),
    
    # path('compilestat', agtron_stat, name='agtron-stat'),
]