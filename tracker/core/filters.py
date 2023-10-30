from django_filters import rest_framework as django_filters

from core.models import Skills
from users.models import Candidate


class AndFilter(django_filters.ModelMultipleChoiceFilter):
    """Фильтр с логикой 'И'"""

    def __init__(self, *args, **kwargs):
        super(AndFilter, self).__init__(*args, **kwargs)
        self.conjoined = True


class CandidateFilter(django_filters.FilterSet):
    skills = AndFilter(
        field_name="skills__name",
        to_field_name="name",
        queryset=Skills.objects.all(),
    )
    work_arrangement = django_filters.CharFilter(
        field_name="work_arrangement__name", lookup_expr="iexact"
    )
    form_of_empoyment = django_filters.CharFilter(
        field_name="form_of_empoyment__name", lookup_expr="iexact"
    )
    city = django_filters.CharFilter(field_name="city__name", lookup_expr="iexact")
    education = django_filters.CharFilter(
        field_name="education__name", lookup_expr="iexact"
    )
    education_YP = django_filters.CharFilter(
        field_name="education_YP__name", lookup_expr="iexact"
    )
    status_from_kt = django_filters.CharFilter(
        field_name="status_from_kt__name", lookup_expr="iexact"
    )

    class Meta:
        model = Candidate
        fields = []
