from collections import OrderedDict
from django.db.models import Sum, Value, Count, Min
from django.db.models.functions import Coalesce


def get_about_categories(queryset):
    about_categories = queryset \
        .annotate(orders_cnt=Count('order')) \
        .order_by('-orders_cnt')
    return about_categories


def get_per_year_month_summary(queryset):
    queryset = queryset.all()\
        .values_list('date__year', 'date__month')\
        .annotate(Sum('amount'))\
        .order_by('date__year', 'date__month')
    result = OrderedDict()
    for period in queryset:
        if str(period[0]) not in result:
            result[str(period[0])] = 0
        result[f'{period[0]}-{period[1]}'] = period[2]
        result[str(period[0])] += period[2]
    return result


def summary_total(queryset):
    result = queryset.aggregate(Sum('amount'))['amount__sum']
    if not result:
        result = 0
    return result


def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(category_name=Coalesce('category__name', Value('-')))
        .order_by()
        .values('category_name')
        .annotate(s=Sum('amount'))
        .values_list('category_name', 's')
    ))


def get_min_date(queryset):
    return queryset.aggregate(Min('date'))['date__min']


