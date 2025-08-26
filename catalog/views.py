from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from catalog.models import Product, Contact
from catalog.forms import ProductForm

class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(publish_status='published').order_by('-created_at')[:5]

class ContactsView(TemplateView):
    template_name = 'contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contact.objects.all()
        context['success'] = False
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        Contact.objects.create(name=name, phone=phone, message=message)
        context = self.get_context_data()
        context['success'] = True
        return self.render_to_response(context)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        product = self.get_object()
        return product.owner == self.request.user

class ModeratorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm('catalog.can_unpublish_product')

class ProductUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('home')

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        product = self.get_object()
        return (product.owner == self.request.user or 
                self.request.user.has_perm('catalog.delete_product'))

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class ProductUnpublishView(LoginRequiredMixin, ModeratorRequiredMixin, UpdateView):
    model = Product
    fields = []
    template_name = 'product_confirm_unpublish.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        product = form.save(commit=False)
        product.publish_status = 'draft'
        product.save()
        return super().form_valid(form)