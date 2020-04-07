from django.urls import path

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

]
