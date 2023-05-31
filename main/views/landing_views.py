"""
Landing page views.

Functions and pages related to site's landing stage.
"""

from .functions import *


def logout_page(request) -> HttpResponse:
    """
    Logout request user
    """

    logout(request)
    return redirect('/')


def landing_page(request) -> HttpResponse:
    """
    Page view. First page that user see's when he visits site for the first time.
    """

    if request.user.is_authenticated:
        return redirect('/id' + str(request.user.id))

    context = set_context(request, 'TrueLink | Добро пожаловать')

    next_page = request.GET.get('next', None)

    # Register
    if request.method == "POST":
        form_username = request.POST.get('username')
        form_first_name = request.POST.get('first_name')
        form_last_name = request.POST.get('last_name')
        form_email = request.POST.get('email')
        form_password = request.POST.get('password')
        if form_username and form_first_name and form_last_name and form_email and form_password:
            try:
                user = User.objects.create_user(
                    username=form_username,
                    email=form_email,
                    password=form_password,
                    first_name=form_first_name.capitalize(),
                    last_name=form_last_name.capitalize(),
                )
            except IntegrityError:
                messages.add_message(request, messages.ERROR, "Пользователь уже существует")
                return redirect('/')
            user.save()
            user.profile.pfp_link = '/static/images/default_pfp.jpg'
            user.profile.save()
            login(request, user)
            return redirect('/')

        login_username = request.POST.get('login_username')
        login_password = request.POST.get('login_password')

        if login_password and login_username:
            if '@' in login_username:
                username = User.objects.get(email=login_username).username
                user = authenticate(
                    request,
                    username=username,
                    password=login_password,
                )
            else:
                user = authenticate(
                    request,
                    username=login_username,
                    password=login_password,
                )

            if user is not None:
                login(request, user)
                return redirect(next_page) if next_page is not None else redirect('/')
            else:
                messages.add_message(request, messages.ERROR, "Неправильное имя пользователя или пароль")

    return render(request, 'pages/landing/landing.html', context)


def forgot_password_page(request) -> HttpResponse:
    """
    Forgot password page view.
    """

    if request.user.is_authenticated:
        return redirect('/id' + str(request.user.id))

    context = set_context(request, 'Восстановление пароля')
    return render(request, 'pages/landing/forgot_password.html', context)
