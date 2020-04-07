from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View

from news.forms.sign_up_form import SignUpForm
from news.views.tokens import account_activation_token


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'news/sign_up.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False

            user.save()
            my_group = Group.objects.get(name='users')
            my_group.user_set.add(user)
            my_group.save()
            mail_subject = 'Activate your account.'
            current_site = get_current_site(request)
            message = render_to_string('news/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            user.email_user(mail_subject, message)

        return redirect('account_activation_sent')
