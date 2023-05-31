"""
Search page views.

Functions and pages related to site's searching system.
"""

from .functions import *


def search(request) -> HttpResponse:
    """
    Search page view.
    """

    context = set_context(request, 'Результаты поиска')

    search_request = request.GET.get('search', None)
    context['search_request'] = search_request
    if search_request is None:
        return redirect('/error/')
    elif search_request:
        if str(search_request[0]) == '#':
            return redirect(f'/id{search_request[1:]}')
        else:
            users_by_first_name = User.objects.filter(first_name__contains=str(search_request).capitalize())
            users_by_last_name = User.objects.filter(last_name__contains=str(search_request).capitalize())
            users_list = []
            for user in users_by_first_name:
                users_list.append(user)
            for user in users_by_last_name:
                if user.profile.last_name_visible:
                    users_list.append(user)
            users_list = list(set(users_list))
            context['users_results'] = len(users_list)
            users_list = users_list[:3]

            groups_by_name = Group.objects.filter(name__contains=str(search_request))
            context['groups_results'] = len(groups_by_name)
            groups_by_name = groups_by_name[:3]

            servers_by_name = Server.objects.filter(name__contains=str(search_request))
            context['servers_results'] = len(servers_by_name)
            servers_by_name = servers_by_name[:3]

            context['groups'] = [{
                'group_name': gr.name,
                'link_to_img': gr.link_to_img,
                'follower': True if str(request.user.id) in gr.members.split(' ') else False,
                'wants_to_join': True if str(request.user.id) in gr.invitations.split(' ') else False,
                'id': gr.id,
            } for gr in groups_by_name]

            context['users'] = users_list

            context['servers'] = [{
                'server': sr,
                'follower': True if str(request.user.id) in sr.members.split(' ') else False,
                'wants_to_join': True if str(request.user.id) in sr.invitations.split(' ') else False,
            } for sr in servers_by_name]

    return render(request, 'pages/search/search_results.html', context)


def more_people(request) -> HttpResponse:
    """
    More users page view. All search results for users.
    """

    context = set_context(request, 'Результаты поиска | Люди')

    search_request = request.GET.get('search', None)
    if search_request is None:
        return redirect('/error/')
    elif search_request:
        users_by_first_name = User.objects.filter(first_name__contains=str(search_request).capitalize())
        users_by_last_name = User.objects.filter(last_name__contains=str(search_request).capitalize())
        users_list = []
        for user in users_by_first_name:
            users_list.append(user)
        for user in users_by_last_name:
            if user.profile.last_name_visible:
                users_list.append(user)
        users_list = list(set(users_list))
        context['users'] = users_list

    return render(request, 'pages/search/more_people.html', context)


def more_groups(request) -> HttpResponse:
    """
    More groups page view. All search results for groups.
    """

    context = set_context(request, 'Результаты поиска | Группы')

    search_request = request.GET.get('search', None)
    if search_request is None:
        return redirect('/error/')
    elif search_request:
        groups_by_name = Group.objects.filter(name__contains=str(search_request))

        context['groups'] = [{
            'group_name': gr.name,
            'link_to_img': gr.link_to_img,
            'follower': True if str(request.user.id) in gr.members.split(' ') else False,
            'wants_to_join': True if str(request.user.id) in gr.invitations.split(' ') else False,
            'id': gr.id,
        } for gr in groups_by_name]

    return render(request, 'pages/search/more_groups.html', context)


@login_required
def more_servers(request) -> HttpResponse:
    """
    More servers page view. All search results for servers.
    """

    context = set_context(request, 'Результаты поиска | Сервера')

    search_request = request.GET.get('search', None)
    if search_request is None:
        return redirect('/error/')
    elif search_request:
        servers_by_name = Server.objects.filter(name__contains=str(search_request))

        context['servers'] = [{
            'server': sr,
            'follower': True if str(request.user.id) in sr.members.split(' ') else False,
            'wants_to_join': True if str(request.user.id) in sr.invitations.split(' ') else False,
        } for sr in servers_by_name]

    return render(request, 'pages/search/more_servers.html', context)
