from django.urls import path
from django.contrib.auth import views as auth_views

from news import views

urlpatterns = [
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('', views.HomeView.as_view(), name='home'),
    path('account_activation_sent', views.account_activation_sent,
         name='account_activation_sent'),
    path(
        'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})',
        views.activate,
        name='activate'),
    path('login', auth_views.LoginView.
         as_view(template_name='news/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('all_my_posts', views.AllUserPostsView.as_view(
        template_name='news/all_user_posts.html'), name='all_my_posts'),
    path('create_post',
         views.CreatePostView.as_view(template_name='news/create_post.html'),
         name='create_post'),
    path('<int:pk>', views.PostDetailView.as_view(
        template_name='news/post_detail.html'), name='post_detail'),
    path('<int:pk>/edit_post', views.PostEditView.as_view(),
         name='edit_post'),
    path('<int:pk>/delete_post', views.DeletePostView.as_view(),
         name='delete_post'),
    path('<int:pk>/create_comment', views.CreateCommentView.as_view(),
         name='create_comment'),

    path('<int:pk>/comment_detail', views.CommentDetailView.as_view(
        template_name='news/comment_detail.html'), name='comment_detail'),
    path('<int:pk>/edit_comment',
         views.EditCommentView.as_view(template_name='news/edit_comment.html'),
         name='edit_comment'),
    path('all_my_comments', views.AllUserCommentsView.as_view(
        template_name='news/all_user_comments.html'), name='all_my_comments'),
    path('<int:pk>/delete_comment', views.DeleteCommentView.as_view(),
         name='delete_comment'),
]
