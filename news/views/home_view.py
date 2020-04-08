from django.views.generic import ListView

from news.models import Post


class HomeView(ListView):
    template_name = 'news/home.html'

    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(status=1).order_by('title')
