from django import forms
from django.db.models import Count

from .models import Order, Category


class OrderSearchForm(forms.ModelForm):
    name = forms.CharField()
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    categories = forms.ModelMultipleChoiceField(queryset=Category
                                                .objects
                                                .annotate(cnt=Count('order'))
                                                .filter(cnt__gt=0), widget=forms.CheckboxSelectMultiple)
    sort_by = forms.ChoiceField(choices=(
                ("date_desc", "date desc."),
                ("date", "date"),
                ("category", "category A-Z"),
                ("category_desc", "category Z-A"),
        ))

    class Meta:
        model = Order
        fields = ('name', 'start_date', 'end_date', 'categories', 'sort_by')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['start_date'].required = False
        self.fields['end_date'].required = False
        self.fields['categories'].required = False
        self.fields['sort_by'].required = False
