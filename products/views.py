from django.shortcuts import render, get_object_or_404, redirect
from .forms import RoasterForm
from .models import Roaster
from .filters import RoasterFilter


def product_create_view(request):
    form = RoasterForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = RoasterForm()
    context = {
        'form': form
    }
    return render(request, "products/product_create.html", context)


def product_update_view(request, id=id):
    obj = get_object_or_404(Product, id=id)
    form = RoasterForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "products/product_create.html", context)


def product_list_view(request):
    queryset = Roaster.objects.all() # list of objects
    context = {
        "object_list": queryset
    }
    return render(request, "products/product_list.html", context)

def search(request):
    product_list = Roaster.objects.all()
    myFilter = RoasterFilter()
    context = {
    'myFilter':myFilter
    }

    return render(request, 'products/product_filter.html', context )

def product_detail_view(request, id):
    obj = get_object_or_404(Roaster, id=id)
    context = {
        "object": obj
    }
    return render(request, "products/product_detail.html", context)


def product_delete_view(request, id):
    obj = get_object_or_404(Roaster, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('../../')
    context = {
        "object": obj
    }
    return render(request, "products/product_delete.html", context)