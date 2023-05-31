"""
Server page views.

Functions and pages related to site's servers.
"""

from .functions import *


def delete_server_message(request, message_id: int):
    """
    Deletes ServerMessage object from database.
    """

    message = ServerMessage.objects.get(id=message_id)
    server = Server.objects.get(id=message.server_id)
    if request.user.id == message.sender_id or request.user.id == server.creator_id:
        message.delete()


def delete_server(request, server_id: int):
    """
    Deletes Server object from database.
    """

    server = Server.objects.get(id=server_id)
    if request.user.id == server.creator_id or request.user.is_superuser:
        server_chats = ServerChat.objects.all().filter(server_id=server.id)
        server_messages = ServerMessage.objects.all().filter(server_id=server.id)
        for chat in server_chats:
            chat.delete()

        for mes in server_messages:
            mes.delete()

        server_members = [User.objects.get(id=int(us_id)) for us_id in server.members.split(' ')] \
            if len(server.members) != 0 else []
        server_invites = [User.objects.get(id=int(us_id)) for us_id in server.invitations.split(' ')] \
            if len(server.invitations) != 0 else []

        for us in server_members:
            us.profile.servers = remove_number_from_string_list(us.profile.servers, server.id)
            us.save()

        for us in server_invites:
            us.profile.servers_inv = remove_number_from_string_list(us.profile.servers_inv, server.id)
            us.save()

        server.delete()


def members_server_page(request, server_id: int) -> HttpResponse:
    """
    Server members page view.
    """

    context = set_context(request, 'Участники')

    server = Server.objects.get(id=server_id)
    search_request = request.GET.get('search', None)

    if str(request.user.id) not in server.members.split(' '):
        return redirect('/servers/{{server.id}}/invite')

    context['server'] = server
    members = User.objects.filter(id__in=[int(us_id) for us_id in server.members.split(' ')]).order_by('-first_name')
    if search_request is not None:
        members = members.filter(first_name__icontains=search_request) |\
                  members.filter(last_name__icontains=search_request)
    context['members'] = members

    context['banned_users'] = User.objects.filter(id__in=[int(us_id) for us_id in server.bans.split(' ')]) \
        if len(server.bans) != 0 else []

    return render(request, 'pages/server/members_server.html', context)


@login_required
def settings_server(request, server_id: int) -> HttpResponse:
    """
    Server settings page view.
    """

    context = set_context(request, 'Настройки сервера')

    server = Server.objects.get(id=int(server_id))
    context['server'] = server
    context['users_requests'] = [User.objects.get(id=int(us_id)) for us_id in server.invitations.split(' ')] \
        if len(server.invitations) > 0 else []

    if request.method == "POST":
        users_from_req_field = request.POST.getlist('requests')
        req_mode = request.POST.get('request_mode')

        if req_mode is not None:
            if req_mode == 'yes':
                for us_id in users_from_req_field:
                    us = User.objects.get(id=int(us_id))
                    server.members = add_number_to_string_list(server.members, us_id)
                    server.invitations = remove_number_from_string_list(server.invitations, us_id)
                    us.profile.servers_inv = remove_number_from_string_list(us.profile.servers_inv, server_id)
                    us.profile.servers = add_number_to_string_list(us.profile.servers, server_id)
                    us.save()
            else:
                for us_id in users_from_req_field:
                    us = User.objects.get(id=int(us_id))
                    server.invitations = remove_number_from_string_list(server.invitations, us_id)
                    us.profile.servers_inv = remove_number_from_string_list(us.profile.servers_inv, server_id)
                    us.save()

        sr_name = request.POST.get('name')
        closed = True if request.POST.get('visible') is not None else False

        if sr_name:
            server.name = sr_name

        server.closed = closed
        server.save()
        return redirect(f'/servers/{server.id}')

    return render(request, 'pages/server/settings_server.html', context)


@login_required
def create_new_server(request) -> HttpResponse:
    """
    Create new server page view. Creates Server object.
    """

    context = set_context(request, 'Создание сервера')

    if request.method == "POST" and request.POST.get('name'):
        server_name = request.POST.get('name')
        server_is_closed = True if request.POST.get('closed') is not None else False

        created_server = Server(
            name=server_name,
            members=f'{request.user.id}',
            invitations='',
            admins=f'{request.user.id}',
            chats='',
            closed=server_is_closed,
            creator=request.user,
            datetime=datetime.now(),
        )
        created_server.save()
        request.user.profile.servers = add_number_to_string_list(request.user.profile.servers, created_server.id)
        request.user.save()
        sr_chat = ServerChat(
            server=created_server,
            name='general',
            datetime=datetime.now(),
        )
        sr_chat.save()
        created_server.chats = f'{sr_chat.id}'
        created_server.save()
        return redirect(f'/servers/{created_server.id}')

    return render(request, 'pages/server/create_new_server.html', context)


def delete_server_page(request, server_id) -> HttpResponse:
    """
    Delete server page view.
    """

    delete_server(request, server_id)
    return redirect('/servers/')


@login_required
def server_solo_page(request, server_id: int) -> HttpResponse:
    """
    Server page view.
    """

    chat_id = request.GET.get('chat', None)

    server = Server.objects.get(id=server_id)
    context = set_context(request, server.name)
    server_chats = server.chats.split(' ')

    if chat_id is None or chat_id not in server_chats:
        return redirect(f'/servers/{server.id}?chat={server_chats[0]}')

    if str(request.user.id) not in server.members.split(' '):
        return redirect(f'/servers/{server.id}/invite')

    context['server'] = server
    context['server_chats'] = ServerChat.objects.filter(id__in=[int(sr_id) for sr_id in server_chats])

    context['members'] = reversed([User.objects.get(id=int(us_id)) for us_id in server.members.split(' ')])

    if request.method == "POST" and 'pfp_pic' in request.FILES:
        pfp_pic = request.FILES['pfp_pic']

        try:
            trial_image = Image.open(pfp_pic)
            if trial_image.format in image_formats:
                fs = FileSystemStorage()
                filename = fs.save(pfp_pic.name, pfp_pic)
                server.link_to_img = fs.url(filename)
                server.save()
                return redirect(f'/servers/{server.id}/')
        except Exception:
            return redirect(f'/servers/{server.id}/')

    if request.method == 'POST' and request.POST.get('name'):
        chat_name = request.POST.get('name')

        created_chat = ServerChat(
            name=chat_name,
            server=server,
            datetime=datetime.now(),
        )
        created_chat.save()
        server.chats = add_number_to_string_list(server.chats, created_chat.id)
        server.save()
        return redirect(f'/servers/{server.id}?chat={created_chat.id}')

    current_chat = ServerChat.objects.get(id=int(chat_id))
    context['current_chat'] = current_chat

    if request.method == 'POST' and request.POST.get('message'):
        post_message = request.POST.get('message')
        post_message = re.sub(" +", " ", post_message)
        if len(post_message) > 2000:
            return redirect(f'/servers/id{server_id}')
        server_message = ServerMessage(
            server=server,
            chat=current_chat,
            message=post_message,
            sender=request.user,
            datetime=datetime.now(),
        )
        server_message.save()

    servers_chat_messages = ServerMessage.objects.all().filter(server=server, chat=current_chat).order_by('datetime')

    if len(servers_chat_messages) != 0:
        for mes in servers_chat_messages:
            mes.datetime = F'{mes.datetime.strftime("%d")} {months[str(mes.datetime.month)]} в \
            {mes.datetime.strftime("%H:%M")}'

        context['messages'] = servers_chat_messages

    return render(request, 'pages/server/server_solo.html', context)


def server_kick_page(request, server_id: int) -> HttpResponse:
    """
    Server kick page.
    """

    user_id = request.GET.get('u', None)
    server = Server.objects.get(id=server_id)

    if user_id is not None:
        if str(user_id) not in server.admins.split(' ') and str(request.user.id) in server.admins.split(' ') or\
                request.user == server.creator and user_id != request.user.id:
            leave_server(user_id, server_id)

    return redirect(f'/servers/{server_id}/members')


def server_ban_page(request, server_id: int) -> HttpResponse:
    """
    Server ban page.
    """

    user_id = request.GET.get('u', None)
    server = Server.objects.get(id=server_id)

    if user_id is not None:
        if str(user_id) not in server.admins.split(' ') and str(request.user.id) in server.admins.split(' ') or\
                request.user == server.creator and user_id != request.user.id:
            server_ban(user_id, server_id)

    return redirect(f'/servers/{server_id}/members')


def server_make_admin_page(request, server_id: int) -> HttpResponse:
    """
    Server page that makes user an admin.
    """

    user_id = request.GET.get('u', None)
    server = Server.objects.get(id=server_id)

    if user_id is not None:
        if request.user == server.creator and user_id != request.user.id:
            server_make_admin(user_id, server_id)

    return redirect(f'/servers/{server_id}/members')


def server_ban(user_id, server_id: int):
    """
    Adds user to server's bans list.
    """

    server = Server.objects.get(id=server_id)
    user = User.objects.get(id=user_id)

    if str(user.id) not in server.bans.split(' '):
        server.bans = add_number_to_string_list(server.bans, user.id)
    else:
        server.bans = remove_number_from_string_list(server.bans, user.id)
    server.save()

    leave_server(user_id, server_id)


def server_make_admin(user_id, server_id: int):
    """
    Adds user to server's admins list.
    """

    server = Server.objects.get(id=server_id)
    user = User.objects.get(id=user_id)

    if str(user.id) not in server.admins.split(' '):
        server.admins = add_number_to_string_list(server.admins, user.id)
    else:
        server.admins = remove_number_from_string_list(server.admins, user.id)
    server.save()


def leave_server(user_id, server_id: int):
    """
    Removes user from server's members list.
    """

    server = Server.objects.get(id=int(server_id))
    user = User.objects.get(id=user_id)

    if user == server.creator:
        return redirect(f'/servers/{server_id}')

    if str(user.id) in server.members.split(' '):
        if str(user.id) in server.admins.split(' '):
            server.admins = remove_number_from_string_list(server.admins, user.id)
        server.members = remove_number_from_string_list(server.members, user.id)
        user.profile.servers = remove_number_from_string_list(user.profile.servers, server.id)
        server.save()
        user.save()

    elif str(user.id) in server.invitations.split(' '):
        server.invitations = remove_number_from_string_list(server.invitations, user.id)
        user.profile.servers_inv = remove_number_from_string_list(user.profile.servers_inv, server.id)
        server.save()
        user.save()


def leave_server_page(request, server_id: int):
    """
    Leave server page view.
    """

    leave_server(request.user.id, server_id)
    return redirect('/servers/')


def get_server_messages(request) -> HttpResponse:
    """
    Returns last message from database as a JsonReponse
    """

    if len(ServerMessage.objects.all()) != 0:
        last_message = ServerMessage.objects.all().order_by('-datetime')[0]
        last_message = {
            'id': last_message.id,
            'message': last_message.message,
            'chat_id': last_message.chat.id,
            'server_id': last_message.server.id,
            'sender_id': last_message.sender.id,
            'sender_first_name': last_message.sender.first_name,
            'sender_last_name': last_message.sender.last_name if last_message.sender.profile.last_name_visible else '',
            'pfp_link': last_message.sender.profile.pfp_link,
            'datetime': F'{last_message.datetime.strftime("%d")} {months[str(last_message.datetime.month)]} в \
{last_message.datetime.strftime("%H:%M")}',
        }
    else:
        last_message = {'id': -2}
    return JsonResponse({'message': last_message}, status=200)


def delete_server_message_page(request) -> HttpResponse:
    """
    Delete server message page view.
    """

    message_id = request.GET.get('message_id', None)
    if message_id is not None:
        delete_server_message(request, message_id)
    if request.META.get('HTTP_REFERER') is not None:
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('/chats/')


@login_required
def invite_server_page(request, server_id: int) -> HttpResponse:
    """
    Server invite page view.
    """

    context = set_context(request, 'Приглашение на сервер')

    server = Server.objects.get(id=int(server_id))

    if str(request.user.id) in server.members.split(' ') or str(request.user.id) in server.invitations.split(' '):
        return redirect('/servers/')

    context['server'] = server

    return render(request, 'pages/server/invite_server.html', context)


@login_required
def invite_server_handler_page(request, server_id: int):
    """
    Adds user to server's members list.
    """

    server = Server.objects.get(id=int(server_id))

    if str(request.user.id) not in server.bans.split(' '):

        if str(request.user.id) in server.members.split(' ') or str(request.user.id) in server.invitations.split(' '):
            return redirect('/server/')

        if server.closed:
            server.invitations = add_number_to_string_list(server.invitations, request.user.id)
            request.user.profile.servers_inv = add_number_to_string_list(request.user.profile.servers_inv, server.id)
            server.save()
            request.user.save()
            return redirect('/servers/')
        else:
            server.members = add_number_to_string_list(server.members, request.user.id)
            request.user.profile.servers = add_number_to_string_list(request.user.profile.servers, server.id)
            server.save()
            request.user.save()
            return redirect(f'/servers/{server.id}')
    else:
        return redirect('/servers/')
