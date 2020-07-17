import django_filters
from .models import *

class RoasterFilter(django_filters.FilterSet):
	class Meta:
		model = Roaster
		fields = '__all__'
