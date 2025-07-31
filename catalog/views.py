from django.shortcuts import render
from catalog.models import Product, Contact

def home_view(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    for product in latest_products:
        print(product.name)
    return render(request, 'home.html')

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
