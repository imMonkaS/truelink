"""
Group views.

Functions and pages related to site's groups.
"""

from .functions import *


def group_solo_page(request, group_id: int) -> HttpResponse:
    """
    Group paeg view
    """

    current_group = Group.objects.get(id=group_id)
    context = set_context(request, current_group.name)

    if request.method == "POST" and request.POST.get('post_id'):
        heart_group_post(request, int(request.POST.get('post_id')))

    user_is_member = False
    if str(request.user.id) in current_group.members.split(' '):
        user_is_member = True

    user_sent_inv = False
    if str(request.user.id) in current_group.invitations.split(' '):
        user_sent_inv = True

    context['user_is_member'] = user_is_member
    context['user_sent_inv'] = user_sent_inv

    context['admins'] = reversed([User.objects.get(id=int(us_id)) for us_id in current_group.admins.split(' ')])
    context['members'] = reversed([User.objects.get(id=int(us_id)) for us_id in current_group.members.split(' ')])

    if request.method == "POST" and 'pfp_pic' in request.FILES:
        pfp_pic = request.FILES['pfp_pic']

        try:
            trial_image = Image.open(pfp_pic)
            if trial_image.format in image_formats:
                fs = FileSystemStorage()
                filename = fs.save(pfp_pic.name, pfp_pic)
                current_group.link_to_img = fs.url(filename)
                current_group.save()
                return redirect(f'/groups/{group_id}')
        except Exception:
            return redirect(f'/groups/{group_id}')

    if request.method == 'POST' and 'post_img' in request.FILES and request.POST.get('text'):
        post_img = request.FILES['post_img']
        text = request.POST.get('text')
        text = re.sub(" +", " ", text)
        if len(text) > 2060:
            return redirect(f'/groups/id{group_id}')
        try:
            trial_image = Image.open(post_img)
            if trial_image.format in image_formats:
                fs = FileSystemStorage()
                filename = fs.save(post_img.name, post_img)

                GroupPost(
                    group=current_group,
                    user=request.user,
                    text=text,
                    likes=0,
                    liked_by='',
                    link_to_img=fs.url(filename),
                    datetime=datetime.now(),
                ).save()

                return redirect(f'/groups/{group_id}')
        except Exception:
            return redirect('/id' + str(request.user.id))

    elif request.method == 'POST' and request.POST.get('text'):
        text = request.POST.get('text')
        text = re.sub(" +", " ", text)
        if len(text) > 2060:
            return redirect(f'/id{group_id}')
        GroupPost(
            group=current_group,
            user=request.user,
            text=text,
            likes=0,
            liked_by='',
            link_to_img='',
            datetime=datetime.now(),
        ).save()

        return redirect(f'/groups/{group_id}')

    posts = GroupPost.objects.filter(group=current_group).order_by('-datetime')
    for post in posts:
        post.datetime = F'{post.datetime.strftime("%d")} {months[str(post.datetime.month)]} в \
        {post.datetime.strftime("%H:%M")}'
        post.text = post.text.split('\r\n')
    context['posts'] = posts

    context['group'] = current_group

    return render(request, 'pages/group/group_solo.html', context)


@login_required
def follow_group(request, group_id: int) -> HttpResponse:
    """
    Adds request user to group's members list.
    """

    group = Group.objects.get(id=group_id)

    if str(request.user.id) not in group.bans.split(' '):
        if str(request.user.id) in group.members.split(' ') or str(request.user.id) in group.invitations.split(' '):
            return redirect('/groups/')
        else:
            if not group.visible:
                group.invitations = add_number_to_string_list(group.invitations, request.user.id)
                request.user.profile.groups_inv = add_number_to_string_list(request.user.profile.groups_inv, group_id)
                request.user.profile.save()
                group.save()
                return redirect(f'/groups/{group_id}')
            else:
                group.members = add_number_to_string_list(group.members, request.user.id)
                request.user.profile.groups = add_number_to_string_list(request.user.profile.groups, group_id)
                request.user.profile.save()
                group.save()
                return redirect(f'/groups/{group_id}')
    else:
        return redirect(f'/id{request.user.id}/groups/')


@login_required
def unfollow_group(request, group_id: int) -> HttpResponse:
    """
    Removes request user from group's members list.
    """

    leave_group(request.user.id, group_id)
    return redirect('/groups/')


def delete_group_page(request, group_id: int) -> HttpResponse:
    """
    Delete group page view.
    """

    delete_group(request, group_id)
    return redirect('/groups/')


def group_ban_page(request, group_id: int) -> HttpResponse:
    """
    Group ban page view.
    """

    user_id = request.GET.get('u', None)
    group = Group.objects.get(id=group_id)
    if user_id is not None:
        if str(request.user) in group.admins.split(' ') and user_id not in group.admins.split(' ') \
                or request.user == group.creator and user_id != group.creator.id:
            group_ban(user_id, group_id)

    return redirect(f'/groups/{group.id}/members')


def group_kick_page(request, group_id: int) -> HttpResponse:
    """
    Group kick page view.
    """

    user_id = request.GET.get('u', None)
    group = Group.objects.get(id=group_id)
    if user_id is not None:
        if str(request.user) in group.admins.split(' ') and user_id not in group.admins.split(' ')\
                or request.user == group.creator and user_id != group.creator.id:
            leave_group(user_id, group_id)

    return redirect(f'/groups/{group_id}/members')


def group_make_admin_page(request, group_id: int) -> HttpResponse:
    """
    Group page that makes user an admin.
    """

    user_id = request.GET.get('u', None)
    group = Group.objects.get(id=group_id)
    if user_id is not None:
        if request.user == group.creator and user_id != group.creator.id:
            group_make_admin(user_id, group_id)

    return redirect(f'/groups/{group.id}/members')


def group_ban(user_id, group_id: int):
    """
    Adds user to group's bans list.
    """

    group = Group.objects.get(id=group_id)
    user = User.objects.get(id=user_id)

    if str(user.id) not in group.bans.split(' '):
        group.bans = add_number_to_string_list(group.bans, user.id)
    else:
        group.bans = remove_number_from_string_list(group.bans, user.id)
    group.save()

    leave_group(user_id, group_id)


def group_make_admin(user_id, group_id: int):
    """
    Adds user to group's admins list.
    """

    group = Group.objects.get(id=group_id)
    user = User.objects.get(id=user_id)

    if str(user.id) not in group.admins.split(' '):
        group.admins = add_number_to_string_list(group.admins, user.id)
    else:
        group.admins = remove_number_from_string_list(group.admins, user.id)
    group.save()


def leave_group(user_id, group_id: int):
    """
    Removes user from group's members list.
    """

    user = User.objects.get(id=user_id)
    group = Group.objects.get(id=group_id)

    if user == group.creator:
        return redirect(f'/groups/{group.id}')

    if str(user.id) in group.invitations.split(' '):
        if str(user.id) in group.admins.split(' '):
            group.admins = remove_number_from_string_list(group.admins, user.id)
        group.invitations = remove_number_from_string_list(group.invitations, user.id)
        user.profile.groups_inv = remove_number_from_string_list(user.profile.groups_inv, group_id)
        user.profile.save()
        group.save()

    elif str(user.id) in group.members.split(' '):
        group.members = remove_number_from_string_list(group.members, user.id)
        user.profile.groups = remove_number_from_string_list(user.profile.groups, group_id)
        user.profile.save()
        group.save()


def delete_group_post_page(request, group_id: int) -> HttpResponse:
    """
    Delete group post page view.
    """

    post_id = request.GET.get('post', None)
    if post_id is not None:
        delete_group_post(request, post_id)
    if request.META.get('HTTP_REFERER') is not None:
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('/feed/')


@login_required
def create_new_group(request) -> HttpResponse:
    """
    Handles request post and creates new Group object.
    """

    context = set_context(request, 'Создание группы')

    if request.method == "POST":
        group_name = request.POST.get('group_name')
        group_closed = request.POST.get('closed')
        if group_name:
            created_group = Group(
                name=group_name,
                creator=request.user,
                members=f"{request.user.id}",
                invitations="",
                admins=f"{request.user.id}",
                visible=False if group_closed is not None else True,
                datetime=datetime.now(),
            )
            created_group.save()
            request.user.profile.groups = add_number_to_string_list(request.user.profile.groups, created_group.id)
            request.user.save()
            return redirect(f'/groups/{created_group.id}')
        else:
            return redirect(f'/id{request.user.id}/groups/')

    return render(request, 'pages/group/create_new_group.html', context)


@login_required
def settings_group(request, group_id: int) -> HttpResponse:
    """
    Group's settings page view.
    """

    context = set_context(request, 'Настройки группы')
    group = Group.objects.get(id=group_id)
    context['group'] = group
    context['users_requests'] = [User.objects.get(id=int(us_id)) for us_id in group.invitations.split(' ')]\
        if len(group.invitations) > 0 else []

    if request.method == "POST":
        users_from_req_field = request.POST.getlist('requests')
        req_mode = request.POST.get('request_mode')

        if req_mode is not None:
            if req_mode == 'yes':
                for us_id in users_from_req_field:
                    us = User.objects.get(id=int(us_id))
                    group.members = add_number_to_string_list(group.members, us_id)
                    group.invitations = remove_number_from_string_list(group.invitations, us_id)
                    us.profile.groups_inv = remove_number_from_string_list(us.profile.groups_inv, group_id)
                    us.profile.groups = add_number_to_string_list(us.profile.groups, group_id)
                    us.save()
            else:
                for us_id in users_from_req_field:
                    us = User.objects.get(id=int(us_id))
                    group.invitations = remove_number_from_string_list(group.invitations, us_id)
                    us.profile.groups_inv = remove_number_from_string_list(us.profile.groups_inv, group_id)
                    us.save()

        gr_name = request.POST.get('name')
        is_visible = request.POST.get('visible', None)
        is_visible = False if is_visible is not None else True

        if gr_name:
            group.name = gr_name
        group.visible = is_visible
        group.save()
        return redirect(f'/groups/{group_id}')

    return render(request, 'pages/group/settings_group.html', context)


def members_group_page(request, group_id: int) -> HttpResponse:
    """
    Group's members page view.
    """

    context = set_context(request, 'Участники')
    group = Group.objects.get(id=group_id)
    search_request = request.GET.get('search', None)

    context['group'] = group
    members = User.objects.filter(id__in=[int(us_id) for us_id in group.members.split(' ')]).order_by('-first_name')
    if search_request is not None:
        members = members.filter(first_name__icontains=search_request) |\
                  members.filter(last_name__icontains=search_request)
    context['members'] = members

    context['banned_users'] = User.objects.filter(id__in=[int(us_id) for us_id in group.bans.split(' ')])\
        if len(group.bans) != 0 else []

    return render(request, 'pages/group/members_group.html', context)


def delete_group(request, group_id: int):
    """
    Deletes Group object from database by id.
    """

    group = Group.objects.get(id=group_id)
    if request.user.id == group.creator_id or request.user.is_superuser:
        group_posts = GroupPost.objects.all().filter(group_id=group.id)
        group_members = [User.objects.get(id=int(us_id)) for us_id in group.members.split(' ')]\
            if len(group.members) != 0 else []
        group_invites = [User.objects.get(id=int(us_id)) for us_id in group.invitations.split(' ')]\
            if len(group.invitations) != 0 else []

        for us in group_members:
            us.profile.groups = remove_number_from_string_list(us.profile.groups, group_id)
            us.save()

        for us in group_invites:
            us.profile.groups_inv = remove_number_from_string_list(us.profile.groups_inv, group_id)
            us.save()

        for post in group_posts:
            delete_group_post(request, post.id)
        group.delete()


def delete_group_post(request, post_id: int):
    """
    Deletes GroupPost object from database by id.
    """

    post = GroupPost.objects.get(id=post_id)
    group = Group.objects.get(id=post.group_id)
    if str(request.user.id) in group.admins.split(' ') or request.user.is_superuser or request.user.id == post.user_id:
        liked_users = [User.objects.get(id=int(us_id)) for us_id in post.liked_by.split(' ')]\
            if len(post.liked_by) != 0 else []

        for us in liked_users:
            us.profile.group_posts_liked = remove_number_from_string_list(us.profile.group_posts_liked, post.id)
            us.save()

        post.delete()


def heart_group_post(request, post_id: int):
    """
    Toggles like on group post by id.
    """

    post = GroupPost.objects.get(id=post_id)
    if str(post.id) in request.user.profile.group_posts_liked.split(' '):
        post.likes -= 1
        post.liked_by = remove_number_from_string_list(post.liked_by, request.user.id)
        request.user.profile.group_posts_liked = remove_number_from_string_list(
            request.user.profile.group_posts_liked,
            post.id,
        )
    else:
        post.likes += 1
        post.liked_by = add_number_to_string_list(post.liked_by, request.user.id)
        request.user.profile.group_posts_liked = add_number_to_string_list(
            request.user.profile.group_posts_liked,
            post.id,
        )
    post.save()
    request.user.save()


def feed_page(request) -> HttpResponse:
    """
    Feed page view.
    """

    context = set_context(request, 'Новости')

    if request.method == "POST" and request.POST.get('post_id'):
        heart_group_post(request, int(request.POST.get('post_id')))

    if len(request.user.profile.groups) != 0:
        groups = Group.objects.filter(id__in=[int(gr_id) for gr_id in request.user.profile.groups.split(' ')])
        groups = groups.order_by('name')
        context['groups'] = groups[:5]

    user_groups_list = request.user.profile.groups.split(' ')
    if len(request.user.profile.groups) != 0:
        posts = GroupPost.objects.filter(group_id__in=[int(gr_id) for gr_id in user_groups_list])
        posts = posts.order_by('-datetime')
        for post in posts:
            post.datetime = F'{post.datetime.strftime("%d")} {months[str(post.datetime.month)]} в \
            {post.datetime.strftime("%H:%M")}'
            post.text = post.text.split('\r\n')
        context['posts'] = posts

    return render(request, 'pages/group/feed.html', context)
