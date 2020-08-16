from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductionDivForm
from .models import ProductionDiv
from .filters import ProductionDivFilter
from datetime import date
from django.db.models import Count, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import View
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import viewsets
from .serializers import *


class StatsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'production/all_statistic.html')

def production_create_view(request):
    form = ProductionDivForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ProductionDivForm()
    context = {
        'form': form
    }
    return render(request, "production/production_create.html", context)


def production_update_view(request, id=id):
    obj = get_object_or_404(Product, id=id)
    form = ProductionDivForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "production/production_create.html", context)


def production_list_view(request):
    queryset = ProductionDiv.objects.all() # list of objects
    context = {
        "object_list": queryset
    }
    return render(request, "production/production_list.html", context)

def production_karantina_production_view(request):
    queryset = ProductionDiv.objects.filter(production_check_pass=True) 
    context = {
        "object_list": queryset
    }
    return render(request, "production/production_karantina.html", context)

def production_karantina_qc_view(request):
	today = date.today
	queryset = ProductionDiv.objects.filter(qc_check_pass=True) - today
	time_expanding = ProductionDiv.objects.tanggal_blend()-today
	context = {"object_list": queryset,
'time_expanding' : time_expanding
	}
	return render(request, "production/production_karantina.html", context)


def search_2(request):
    product_list = ProductionDiv.objects.all()
    myFilter2 = ProductionDivFilter()
    context = {
    'myFilter2':myFilter2
    }

    return render(request, 'production/production_filter.html', context )

def production_detail_view(request, id):
    obj = get_object_or_404(Product, id=id)
    context = {
        "object": obj
    }
    return render(request, "production/production_detail.html", context)


def production_delete_view(request, id):
    obj = get_object_or_404(Product, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('../../')
    context = {
        "object": obj
    }
    return render(request, "production/production_delete.html", context)

# def time ():
# 	queryset = ProductionDiv.objects.filter(karantina_qc=True)
# 	product_stuck = []
# 	for product in queryset:
# 		today = date.today
# 		time_expanding = ProductionDiv.objects.tanggal_blend-today
# 		product_age = [queryset, time_expanding]
# 		product_stuck.append(product_age)
# 	context = {
# 	'product_stuck':product_stuck
# 	}
# 	return render(request, "production/production_karantina.html", context)



def production_karantina_chart (request):
	
	labels = ['karantina', 'tidak karantina']
	data = []

	queryset = ProductionDiv.objects.filter(production_check_pass=True)

	queryset2 = ProductionDiv.objects.filter(production_check_pass=False)
	lenq1 = len(queryset)
	data.append(lenq1)
	lenq2 = len(queryset2)
	data.append(lenq2)

	return render(request, 'production/production_statistic.html', {
        'labels': labels,
        'data': data,
    })


# def all_karantina (request):


# 	labels_prod = ['blend ok', 'karantina_produksi', 'karantina_qc']
# 	data_prod = []

# 	queryset = ProductionDiv.objects.filter(production_check_pass=True)
# 	queryset2 = ProductionDiv.objects.filter(production_check_pass=False)
# 	queryset_qc = ProductionDiv.objects.filter(qc_check_pass=True)
# 	queryset_qc2 = ProductionDiv.objects.filter(qc_check_pass=False)
# 	# lenq1 = len(queryset)
# 	# data_prod.append(lenq1)
# 	# lenq2 = len(queryset2)
# 	# data_prod.append(lenq2)
# 	# lenq_qc = len(queryset_qc)
# 	# data_qc.append(lenq_qc)
# 	# lenq_qc2 = len(queryset_qc2)
# 	# data_qc.append(lenq_qc2)

# 	blend_aman = len(queryset)+len(queryset_qc)
# 	data_prod.append(blend_aman)

# 	karantina_prod = len(queryset2)
# 	data_prod.append(karantina_prod)

# 	karantina_qc = len(queryset_qc2)
# 	data_prod.append(karantina_qc)
# 	print(data_prod)


# 	# labels_blend = []
# 	# data_blend = []

# 	# qs = ProductionDiv.objects.order_by('jenis_blend')

# 	# for object in qs:
# 	# 	labels_blend.append(object.jenis_blend)
# 	# 	data_blend.append(object.agtron_meter)

# 	# print(labels_blend)
# 	# print(data_blend)

# 	return render(request, 'production/all_statistic.html', {
# 		'labels_prod':labels_prod,
# 		'data_prod': data_prod,
# 		# 'labels_blend':labels_blend, 
# 		# 'data_blend':data_blend, 
# 		# 'qs':qs
# 		}
# 	)

# def agtron_stat (request):
	
# 	labels_blend = []
# 	data_blend = []

# 	qs = ProductionDiv.objects.all()

# 	for object in qs:
# 		labels_blend.append(object.jenis_blend)
# 		data_blend.append(object.agtron_meter)

# 	print('this--------------------------------')	
# 	print(labels_blend)
# 	print(data_blend)


# 	return render(request, 'production/all_statistic.html', {
# 		'labels_blend':labels_blend, 
# 		'data_blend':data_blend, 
# 		'qs':qs})

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []


    def get(self, request):
        productiondiv = ProductionDiv.objects.all()
        queryset = ProductionDiv.objects.filter(production_check_pass=True).count()
        queryset2 = ProductionDiv.objects.filter(production_check_pass=False).count()
        queryset_qc = ProductionDiv.objects.filter(qc_check_pass=True).count()
        queryset_qc2 = ProductionDiv.objects.filter(qc_check_pass=False).count()
        agtronval =[]
        queryset_agtron =ProductionDiv.objects.values('agtron_meter')
        for query in queryset_agtron:
            agtronval.append(query)

        queryset_blend =ProductionDiv.objects.values('jenis_blend')
        return Response(data)

    def post(self, request):
        pass

class BlendReportData(APIView):

    def get(self, request):
        queryset = BlendReport.objects.all()
        serializer = BlendReportSerializer(queryset, many=True)
        return Response(serializer.data)

