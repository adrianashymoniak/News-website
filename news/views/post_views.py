from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
from django.views.generic.base import View

from news.forms.post_form import PostForm
from news.models import Post, CustomGroup, Comment


class AllUserPostsView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user).order_by('title')


class CreatePostView(LoginRequiredMixin, View):
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
            return redirect('all_my_posts')
        else:
            post = Post()
            post.title = request.POST['title']
            post.description = request.POST['description']
            return render(request, 'news/create_post.html', {'form': form})


class PostEditView(LoginRequiredMixin, UpdateView):
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


class PostDetailView(View):
    model = Post
    context_object_name = 'post'
    template_name = 'news/post_detail.html'

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        comments = Comment.objects.filter(post=post)
        paginator = Paginator(comments, 3)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(
            request, 'news/post_detail.html', {
                'post': post, 'comments': comments, 'page_obj': page_obj})


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('all_my_posts')

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        if post.author != request.user:
            raise Http404
        else:
            return self.delete(request, *args, **kwargs)
