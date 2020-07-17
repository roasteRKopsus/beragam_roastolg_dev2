import django_filters
from .models import ProductionDiv

class ProductionDivFilter(django_filters.FilterSet):
	class Meta:
		model = ProductionDiv
		fields = '__all__'
