"""
User page views.

Functions and pages related to site's user.
"""

from .functions import *


def user_page(request, user_id: int) -> HttpResponse:
    """
    User page view.
    """

    context = set_context(request, 'TrueLink | Главная')

    try:
        user_on_page = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('/error/')

    context['user_on_page'] = user_on_page

    if request.method == "POST" and request.POST.get('post_id'):
        heart_post(request, int(request.POST.get('post_id')))

    if request.user.is_authenticated:
        try:
            context['friend_added'] = True if User.objects.get(id=user_id) in list_friends(request.user.id) else False
        except Exception:
            return redirect('/error/')

    friends_list = list_friends(user_id)

    context['friends_amount'] = len(friends_list)

    context['friends_gr1'] = [friends_list[i] for i in range(3)] if len(friends_list) >= 3 else friends_list
    context['friends_gr2'] = [friends_list[i] for i in range(3, 6)] if len(friends_list) >= 6 else friends_list[3:]

    if len(user_on_page.profile.groups) != 0:
        groups = Group.objects.filter(id__in=[int(gr_id) for gr_id in user_on_page.profile.groups.split(' ')])
        groups = groups.order_by('name')
        context['groups'] = groups[:5]

    if request.method == 'POST' and 'pfp_pic' in request.FILES:
        pfp_pic = request.FILES['pfp_pic']

        try:
            trial_image = Image.open(pfp_pic)
            if trial_image.format in image_formats:
                fs = FileSystemStorage()
                filename = fs.save(pfp_pic.name, pfp_pic)
                request.user.profile.pfp_link = fs.url(filename)
                request.user.profile.save()
                return redirect('/id' + str(request.user.id))
        except Exception:
            return redirect('/id' + str(request.user.id))

    context['page_url'] = f'/id{user_id}'

    change_info(request, user_on_page)

    if request.method == 'POST' and 'post_img' in request.FILES and request.POST.get('text'):
        post_img = request.FILES['post_img']
        post_text = request.POST.get('text')
        post_text = re.sub(" +", " ", post_text)
        if len(post_text) > 2060:
            return redirect(f'/id{user_id}')

        try:
            trial_image = Image.open(post_img)
            if trial_image.format in image_formats:
                fs = FileSystemStorage()
                filename = fs.save(post_img.name, post_img)
                UserPost(
                    link_to_img=fs.url(filename),
                    user=request.user,
                    likes=0,
                    text=post_text,
                    datetime=datetime.now(),
                ).save()
                return redirect('/id' + str(request.user.id))
        except Exception:
            return redirect('/id' + str(request.user.id))
    elif request.method == 'POST' and request.POST.get('text'):
        post_text = request.POST.get('text')
        post_text = re.sub(" +", " ", post_text)
        if len(post_text) > 2060:
            return redirect(f'/id{user_id}')
        UserPost(
            link_to_img='',
            user=request.user,
            likes=0,
            text=post_text,
            datetime=datetime.now(),
        ).save()
        return redirect('/id' + str(request.user.id))
    user_posts = UserPost.objects.filter(user=user_on_page).order_by('-datetime')
    for post in user_posts:
        post.datetime = F'{post.datetime.strftime("%d")} {months[str(post.datetime.month)]} в \
        {post.datetime.strftime("%H:%M")}'
        post.text = post.text.split('\r\n')

    context['posts'] = user_posts
    context['images'] = GalleryImage.objects.all().filter(user=context['user_on_page'])

    return render(request, 'pages/user/users_page.html', context)


def change_info(request, user_on_page: User) -> HttpResponse:
    """
    Handles request and changes user info.
    """

    if request.user == user_on_page:
        if request.method == 'POST':
            text = request.POST.get('about_me', None)
            if text is not None:
                request.user.profile.about_me = text
                request.user.save()
    return redirect(f'/id{request.user.id}')


def delete_post_page(request, user_id: int) -> HttpResponse:
    """
    Delete post page view.
    """

    post_id = request.GET.get('post')
    if post_id is not None:
        delete_users_post(request, int(post_id))
    return redirect(f'/id{user_id}')


@login_required
def users_add_friend_page(request, user_id: int) -> HttpResponse:
    """
    Add friend page view.
    """

    next_page = request.GET.get('next', None)

    if request.user.id != user_id:
        Friend.make_friend(request.user, user_id)

    return redirect('/') if next_page is None else redirect(next_page)


@login_required
def users_remove_friend_page(request, user_id: int) -> HttpResponse:
    """
    Remove friend page view.
    """

    next_page = request.GET.get('next', None)

    if request.user.id != user_id:
        Friend.remove_friend(request.user, user_id)

    return redirect('/') if next_page is None else redirect(next_page)


def heart_post(request, post_id: int):
    """
    Toggles like for user post.
    """

    post = UserPost.objects.get(id=post_id)
    if str(post.id) in request.user.profile.posts_liked.split(' '):
        post.likes -= 1
        post.liked_by = remove_number_from_string_list(post.liked_by, request.user.id)
        request.user.profile.posts_liked = remove_number_from_string_list(request.user.profile.posts_liked, post.id)
    else:
        post.likes += 1
        post.liked_by = add_number_to_string_list(post.liked_by, request.user.id)
        request.user.profile.posts_liked = add_number_to_string_list(request.user.profile.posts_liked, post.id)
    post.save()
    request.user.save()


def delete_image(request, image_id: int):
    """
    Deletes GalleryImage objects from database.
    """

    img = GalleryImage.objects.get(id=int(image_id))
    if request.user == img.user:
        img.delete()


def delete_users_post(request, post_id: int):
    """
    Deletes UserProfilePost object from database.
    """

    post = UserPost.objects.get(id=post_id)
    if post.user_id == request.user.id or request.user.is_superuser:
        liked_users = [User.objects.get(id=int(us_id)) for us_id in post.liked_by.split(' ')]\
            if len(post.liked_by) != 0 else []

        for us in liked_users:
            us.profile.posts_liked = remove_number_from_string_list(us.profile.posts_liked, post.id)
            us.save()

        post.delete()


def delete_image_page(request, user_id: int) -> HttpResponse:
    """
    Delete gallery image page view.
    """

    image_id = request.GET.get('id', None)
    if image_id is not None:
        delete_image(request, image_id)
    if request.META.get('HTTP_REFERER') is not None:
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(f'/id{user_id}/gallery/')


def gallery_page(request, user_id: int) -> HttpResponse:
    """
    Gallery page view.
    """

    context = set_context(request, 'Фотографии')
    if request.method == 'POST' and 'pfp_pic' in request.FILES:
        pfp_pic = request.FILES['pfp_pic']

        try:
            trial_image = Image.open(pfp_pic)
            if trial_image.format in image_formats:
                fs = FileSystemStorage()
                filename = fs.save(pfp_pic.name, pfp_pic)
                gi = GalleryImage(
                    user=request.user,
                    link_to_img=fs.url(filename),
                    datetime=datetime.now(),
                )
                gi.save()
                return redirect(f'/id{user_id}/gallery')
        except Exception:
            return redirect(f'/id{user_id}/gallery')

    user_on_page = User.objects.get(id=user_id)

    context['images'] = GalleryImage.objects.all().filter(user=user_on_page)
    context['user_on_page'] = user_on_page

    return render(request, 'pages/user/gallery.html', context)


@login_required
def profile_settings_page(request, user_id: int) -> HttpResponse:
    """
    Profile settings page view.
    """

    context = set_context(request, 'Настройки профиля')
    if request.user.id == user_id:
        if request.method == "POST":
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            age = request.POST.get('age')
            username = request.POST.get('username')

            if old_password and new_password:
                if request.user.check_password(old_password):
                    request.user.set_password(new_password)
                    request.user.save()
                    return redirect(f'/id{request.user.id}/settings')

            if email:
                try:
                    request.user.email = email
                    request.user.save()
                except IntegrityError:
                    return redirect('/error/')

            if first_name:
                request.user.first_name = first_name.capitalize()
                request.user.save()

            if last_name:
                request.user.last_name = last_name.capitalize()
                request.user.save()

            if username:
                try:
                    request.user.username = username
                    request.user.save()
                except IntegrityError:
                    return redirect('/error/')

            if age:
                request.user.profile.age = age
                request.user.save()

        return render(request, 'pages/user/profile.html', context)
    else:
        return redirect(f'/id{user_id}')


@login_required
def private_settings_page(request, user_id: int) -> HttpResponse:
    """
    Private settings page view.
    """

    context = set_context(request, 'Настройки приватности')

    if request.user.id == user_id:
        if request.method == "POST":
            friends = request.POST.get('friends', None)
            music = request.POST.get('music', None)
            groups = request.POST.get('groups', None)
            last_name = request.POST.get('last_name', None)
            age = request.POST.get('age', None)
            photo = request.POST.get('photo', None)

            request.user.profile.friends_visible = True if friends is not None else False
            request.user.profile.music_visible = True if music is not None else False
            request.user.profile.groups_visible = True if groups is not None else False
            request.user.profile.last_name_visible = True if last_name is not None else False
            request.user.profile.age_visible = True if age is not None else False
            request.user.profile.gallery_visible = True if photo is not None else False

            request.user.save()
            return redirect(f'/id{request.user.id}')

        return render(request, 'pages/user/private.html', context)
    else:
        return redirect(f'/id{user_id}')


@login_required
def servers_page(request) -> HttpResponse:
    """
    User's servers page view.
    """

    context = set_context(request, 'Сервера')

    search_request = request.GET.get('search', None)

    if len(request.user.profile.servers) != 0:
        servers = Server.objects.filter(id__in=[int(sr_id) for sr_id in request.user.profile.servers.split(' ')])
        servers = servers.order_by('name')

        if search_request is not None:
            servers = servers.filter(name__contains=str(search_request))

        context['servers'] = servers

    if len(request.user.profile.servers_inv) != 0:
        servers = Server.objects.filter(id__in=[int(sr_id) for sr_id in request.user.profile.servers_inv.split(' ')])
        servers = servers.order_by('name')

        if search_request is not None:
            servers = servers.filter(name__contains=str(search_request))

        context['servers_inv'] = servers

    return render(request, 'pages/user/servers.html', context)


@login_required
def groups_page(request, user_id: int) -> HttpResponse:
    """
    User's groups page view.
    """

    context = set_context(request, 'Группы')

    user_on_page = User.objects.get(id=user_id)
    context['user_on_page'] = user_on_page
    search_request = request.GET.get('search', None)

    if len(user_on_page.profile.groups) > 0:
        groups = Group.objects.filter(id__in=[int(gr_id) for gr_id in user_on_page.profile.groups.split(' ')])
        groups = groups.order_by('name')

        if search_request is not None:
            groups = groups.filter(name__contains=str(search_request))
        context['groups'] = groups

    if len(user_on_page.profile.groups_inv) > 0:
        groups = Group.objects.filter(id__in=[int(gr_id) for gr_id in user_on_page.profile.groups_inv.split(' ')])
        groups = groups.order_by('name')

        if search_request is not None:
            groups = groups.filter(name__contains=str(search_request))
        context['groups_inv'] = groups

    return render(request, 'pages/user/groups.html', context)


@login_required
def friends_page(request, user_id: int) -> HttpResponse:
    """
    User's friends page view.
    """

    context = set_context(request, 'Друзья')

    search_request = request.GET.get('search', None)
    context['search_request'] = search_request

    friends_list = list_friends(user_id)

    context['request_user_friends'] = list_friends(request.user.id)
    context['user_on_page'] = User.objects.get(id=user_id)

    context['friends'] = friends_list
    context['friends_amount'] = len(friends_list)

    context['page_url'] = f'/id{user_id}/friends'

    if search_request is not None:
        users_by_first_name = User.objects.filter(first_name__contains=str(search_request).capitalize())
        users_by_last_name = User.objects.filter(last_name__contains=str(search_request).capitalize())
        users_list = []
        for user in users_by_first_name:
            users_list.append(user)
        for user in users_by_last_name:
            if user.profile.last_name_visible:
                users_list.append(user)
        users_list = list(set(users_list))

        users_list = [item for item in users_list if item in friends_list]
        context['friends_search'] = users_list

    return render(request, 'pages/user/friends.html', context)
