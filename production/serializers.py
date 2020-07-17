from rest_framework import serializers
from .models import *


class ProductionDivSerializer(serializers.ModelSerializer):
	blend_pass_count = serializers.IntegerField(source = 'production_check_pass.filter(production_check_pass=True).count', read_only=True)

	class Meta:
		model = ProductionDiv
		fields = "__all__"


	