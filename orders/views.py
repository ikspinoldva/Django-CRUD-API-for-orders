from django.views.generic.list import ListView
from datetime import date
from .forms import OrderSearchForm
from .models import Order, Category
from .reports import summary_per_category, get_min_date, summary_total, get_per_year_month_summary, get_about_categories


class OrderListView(ListView):
    model = Order
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = OrderSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            min_date = form.cleaned_data.get('start_date')
            max_date = form.cleaned_data.get('end_date')
            categories = form.cleaned_data.get('categories')
            sort_by = form.cleaned_data.get('sort_by')

            if name:
                queryset = queryset.filter(name__icontains=name)

            if min_date or max_date:
                if not min_date:
                    min_date = get_min_date(queryset)
                if not max_date:
                    max_date = date.today()
                queryset = queryset.filter(date__range=(min_date, max_date))

            if categories:
                category_list = []
                for c in categories:
                    category_list.append(c)
                queryset = queryset.filter(category__name__in=category_list)

            if sort_by:
                if sort_by == 'date_desc':
                    queryset = queryset.order_by('-date', '-pk')
                elif sort_by == 'date':
                    queryset = queryset.order_by('date', 'pk')
                elif sort_by == 'category':
                    queryset = queryset.order_by('category', 'name')
                elif sort_by == 'category_desc':
                    queryset = queryset.order_by('-category', '-name')

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            summary_total=summary_total(queryset),
            get_per_year_month_summary=get_per_year_month_summary(queryset),
            **kwargs)


class CategoryListView(ListView):
    model = Category
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        context = super().get_context_data(
            object_list=queryset,
            about_categories=get_about_categories(queryset),
            ** kwargs)
        return context