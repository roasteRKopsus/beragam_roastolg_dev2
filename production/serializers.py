from rest_framework import serializers
from .models import *
# from django.core import serializers
from io import StringIO



# class ProductionDivSerializer(serializers.ModelSerializer):
# 	blend_pass_count = serializers.IntegerField(source = 'production_check_pass.filter(production_check_pass=True).count', read_only=True)

# 	class Meta:
# 		model = ProductionDiv
# 		fields = "__all__"
class ProductionDivSerializer():
	pass


class BlendNameSerializer(serializers.ModelSerializer):

	class Meta:
		model = BlendName
		fields = ( "__all__")


class RunTimeStockSerializer(serializers.ModelSerializer):

	blend_name = BlendNameSerializer()

	class Meta:
		model = RunTimeStock
		fields = ( "__all__")


class BlendReportSerializer(serializers.ModelSerializer):
	blend_name = RunTimeStockSerializer()
	weight = serializers.FloatField(source='total_weight', read_only=True)

	class Meta:
		model = BlendReport
		fields = ( "__all__")






# class PropBaseSerializer(serializers.base.Serializer):
	
# 	def serialize(self, queryset, **options):
# 		self.selected_props = options.pop('props')
# 		return super().serialize(queryset, **options)

# 	def serialize_property(self, obj):
# 		model = type(obj)
# 		for prop in self.selected_props:
# 			if hasattr(model, prop) and type(getattr(model, prop)) == property:
# 				self.handle_prop(obj, prop)

# 	def handle_prop(self, obj, prop):
# 		self._current[prop] = getattr(obj, prop)

# 	def end_object(self, obj):
# 		self.serialize_property(obj)
# 		super().end_object(obj)


# class PropPythonSerializer(PropBaseSerializer, serializers.python.Serializer):
# 	pass


# class PropJsonSerializer(PropPythonSerializer, serializers.json.Serializer):
# 	pass
# 	