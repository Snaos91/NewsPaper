from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter
from .models import Post, Author
from django.forms.widgets import SelectDateWidget


class PostFilter(FilterSet):
    time_filter = DateFilter(field_name='data_time_creation', lookup_expr='gte', label='Новости позже даты',
                             widget=SelectDateWidget)

    title_filter = CharFilter(field_name='title', lookup_expr='icontains', label='Поиск по названию')

    author_filter = ModelChoiceFilter(field_name='author', queryset=Author.objects.all(), label='Автор')

    class Meta:
        model = Post
        fields = [
        ]
