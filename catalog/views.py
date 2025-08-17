from django.shortcuts import render, get_object_or_404
from catalog.models import Product, Contact

def home_view(request):
    products = Product.objects.all().order_by('-created_at')[:5]
    return render(request, 'home.html', {'products': products})

def contacts_view(request):
    contacts = Contact.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        Contact.objects.create(name=name, phone=phone, message=message)
        success = True
    else:
        success = False
    return render(request, 'contacts.html', {'success': success, 'contacts': contacts})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})