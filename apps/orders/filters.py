import django_filters
from django.db.models.functions import Cast
from django.db.models import DateField, Q
from .models import Orders


class OrderFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    surname = django_filters.CharFilter(field_name="surname", lookup_expr="icontains")
    email = django_filters.CharFilter(field_name="email", lookup_expr="icontains")
    phone = django_filters.CharFilter(field_name="phone", lookup_expr="icontains")
    age = django_filters.NumberFilter(field_name="age")
    course = django_filters.CharFilter(field_name="course", lookup_expr="exact")
    course_format = django_filters.CharFilter(field_name="course_format", lookup_expr="exact")
    course_type = django_filters.CharFilter(field_name="course_type", lookup_expr="exact")
    status = django_filters.CharFilter(method="filter_status")
    group = django_filters.CharFilter(field_name="group", lookup_expr="exact")
    start_date = django_filters.DateFilter(method="filter_start_date")
    end_date = django_filters.DateFilter(method="filter_end_date")
    only_my_applications = django_filters.BooleanFilter(method="filter_by_manager")

    def filter_status(self, queryset, name, value):
        if value == "New":
            return queryset.filter(Q(status="New"))
        return queryset.filter(status=value)

    def filter_start_date(self, queryset, name, value):
        return queryset.annotate(date_only=Cast("created_at", DateField())).filter(date_only__gte=value)

    def filter_end_date(self, queryset, name, value):
        return queryset.annotate(date_only=Cast("created_at", DateField())).filter(date_only__lte=value)

    def filter_by_manager(self, queryset, name, value):
        if value:
            return queryset.filter(manager=self.request.user)
        return queryset

    class Meta:
        model = Orders
        fields = [
            "name", "surname", "email", "phone", "age",
            "course", "course_format", "course_type",
            "status", "group", "start_date", "end_date",
            "only_my_applications"
        ]
