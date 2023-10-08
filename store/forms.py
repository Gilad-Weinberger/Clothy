from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Product, Color, Category
from django.contrib.auth.forms import UserCreationForm

class ProductForm(forms.ModelForm):
    colors = forms.ModelMultipleChoiceField(
        queryset=Color.objects.all(),
        widget=FilteredSelectMultiple("Colors", is_stacked=False),
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=FilteredSelectMultiple("Categories", is_stacked=False),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['colors'].widget.attrs['class'] = 'colored-circles'

    class Meta:
        model = Product
        fields = '__all__'