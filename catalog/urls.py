from django.urls import path
from catalog.views import home_view, contacts_view, product_detail

urlpatterns = [
    path('', home_view, name='home'),
    path('contacts/', contacts_view, name='contacts'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
]