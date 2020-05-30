import django_filters
from .models import Post
class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        #fields = ['title', 'author']
        ordering = ['-date_posted']
        fields = {
            'title': ['exact'],
            'author': ['exact'],
        }