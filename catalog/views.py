from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')

def contacts_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        success = True
    else:
        success = False
    return render(request, 'contacts.html', {'success': success})
