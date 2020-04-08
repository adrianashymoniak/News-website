from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.base import View

from news.forms.post_form import PostForm
from news.models import Post, CustomGroup


class AllUserPostsView(ListView):
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user).order_by('title')


class CreatePostView(View):
    template_name = 'news/create_post.html'

    def get(self, request):
        form = PostForm()
        return render(request, 'news/create_post.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            all_groups = CustomGroup.objects.all()
            for group in all_groups:
                pre_moderation = getattr(group, 'pre_moderation')
                if post.author.groups.filter(name=group).exists() and \
                        pre_moderation is False:
                    post.status = Post.ACCEPTED
                else:
                    post.status = Post.IN_MODERATION
            post.save()
            return redirect('home')
        else:
            post = Post()
            post.title = request.POST['title']
            post.description = request.POST['description']
            return render(request, 'news/create_post.html', {'form': form})
