from django import forms
from django.core.exceptions import ValidationError
from catalog.models import Product

FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control-file'

    def save(self, commit=True):
        product = super().save(commit=False)
        if self.user and not product.owner:
            product.owner = self.user
        if commit:
            product.save()
        return product

    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        for word in FORBIDDEN_WORDS:
            if word in name:
                raise forms.ValidationError(f'Запрещенное слово: {word}')
        return self.cleaned_data['name']

    def clean_description(self):
        description = self.cleaned_data['description'].lower()
        for word in FORBIDDEN_WORDS:
            if word in description:
                raise forms.ValidationError(f'Запрещенное слово: {word}')
        return self.cleaned_data['description']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Размер файла не должен превышать 5 МБ')
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise ValidationError('Формат файла должен быть JPEG или PNG')
        return image