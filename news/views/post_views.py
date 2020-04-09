from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView, DeleteView
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


class PostEditView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/edit_post.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user

            post.save()
            return redirect('post_detail', pk=post.pk)
        else:
            post.title = request.POST['title']
            post.description = request.POST['description']
            return render(request, 'news/edit_post.html',
                          {'form': form, 'post': post})


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs.get('pk'))


class DeletePostView(DeleteView):
    model = Post
    success_url = reverse_lazy('all_my_posts')

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post,  pk=self.kwargs.get('pk'))
        if post.author != request.user:
            raise Http404
        else:
            return self.delete(request, *args, **kwargs)
