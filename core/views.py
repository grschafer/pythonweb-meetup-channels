from django.contrib.auth import get_user_model, login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template.response import TemplateResponse


def index(request):
    if request.method == 'POST':
        User = get_user_model()
        username = request.POST['username']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username)
        # hack
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect(reverse('chat'))

    if not request.user.is_anonymous():
        return redirect(reverse('chat'))

    return TemplateResponse(request, 'core/index.html', {})


def chat(request):
    if request.user.is_anonymous():
        return redirect(reverse('index'))

    return TemplateResponse(request, 'core/chat.html', {})
