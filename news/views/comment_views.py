from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView, ListView
from django.views.generic.base import View

from news.forms.comment_form import CommentForm
from news.models import Post, Comment
from news_website.settings.base import SENDER
from news_website.tasks import send_email


class CreateCommentView(LoginRequiredMixin, View):
    template_name = 'news/create_comment.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs.get('pk'))

    def get(self, request, pk):
        form = CommentForm
        return render(request, 'news/create_comment.html',
                      {'form': form})

    def post(self, request, pk):
        form = CommentForm(request.POST)
        post = self.get_object()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            receiver = [post.author.email]
            sender = SENDER
            subject = 'Comment was added to your post'
            message = render_to_string(
                'news/comment_added_notification_email.html', {
                    'post': post,
                    'comment': comment,
                })
            if comment.author != post.author:
                send_email(subject, message, sender, receiver)
            return redirect('post_detail', pk=post.pk)
        else:
            comment = Comment()
            comment.description = request.POST.get('description')
            return render(request, 'news/create_comment.html',
                          {'form': form})


class EditCommentView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'news/edit_comment.html'
    context_object_name = 'comment'

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, pk=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        comment = self.get_object()
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user

            comment.save()
            return redirect('comment_detail', pk=comment.pk)
        else:
            comment.description = request.POST.get('description')
            return render(request, 'news/edit_comment.html',
                          {'form': form, 'comment': comment})


class CommentDetailView(View):
    model = Comment
    context_object_name = 'comment'
    template_name = 'news/comment_detail.html'

    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        return render(request, 'news/comment_detail.html',
                      {'comment': comment})


class AllUserCommentsView(LoginRequiredMixin, ListView):
    model = Comment
    context_object_name = 'comments'
    paginate_by = 3

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(author=user).order_by('description')


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy('all_my_comments')

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        if comment.author != request.user:
            raise Http404
        else:
            return self.delete(request, *args, **kwargs)
