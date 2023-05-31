"""
Messager views.

Functions and pages related to site's messager.
"""

from .functions import *


@login_required
def messager_page(request):
    """
    Messager page view.
    """

    context = set_context(request, 'Чаты')

    all_messages = Message.objects.all().order_by('-datetime')
    user_with = request.GET.get('u', None)
    if user_with is not None:
        context['user_with'] = User.objects.get(id=int(user_with))

    add_message_to_db(request, user_with, context)

    users_messages = []
    for mes in all_messages:
        if mes.sender == request.user or mes.receiver == request.user:
            users_messages.append(mes)

    context['chats_exist'] = True
    if len(users_messages) == 0 and user_with is None:
        context['chats_exist'] = False

    context['chat_chosen'] = True if user_with is not None else False

    if len(users_messages) > 0:
        user_repeats = []
        left_users = []

        for mes in users_messages:
            if f"{mes.sender.id} {mes.receiver.id}" not in user_repeats\
                    and f"{mes.receiver.id} {mes.sender.id}" not in user_repeats:
                left_users.append(mes)
                user_repeats.append(f"{mes.sender.id} {mes.receiver.id}")

        left_users_dict = []
        for user in left_users:
            if request.user == user.sender:
                user_dict = {
                    'user_with': user.receiver,
                    'show_message': f"Вы: {user.message}" if len(user.message) <= 17 else f"Вы: {user.message[:17]}..."
                }
                left_users_dict.append(user_dict)
            elif request.user == user.receiver:
                user_dict = {
                    'user_with': user.sender,
                    'show_message': f"{user.message}" if len(user.message) <= 20 else f"{user.message[:20]}...",
                }
                left_users_dict.append(user_dict)

        context['left_users'] = left_users_dict

        if user_with is not None:
            user_with = User.objects.get(id=int(user_with))
            messages_with_user = all_messages.filter(
                users__in=[f'{request.user.id} {user_with.id}', f'{user_with.id} {request.user.id}']
            ).order_by('datetime')

            for mes in messages_with_user:
                mes.datetime = F'{mes.datetime.strftime("%d")} {months[str(mes.datetime.month)]} в \
                {mes.datetime.strftime("%H:%M")}'

            context['messages'] = messages_with_user

    return render(request, 'pages/chats.html', context)


def add_message_to_db(request, user_with: int, context: typing.Dict) -> HttpResponse:
    """
    Handles post request and creates new Message object.
    """

    if request.method == 'POST' and request.POST.get('message') and\
            str(user_with) not in request.user.profile.black_list.split(' ') and\
            str(request.user.id) not in context['user_with'].profile.black_list.split(' '):
        message = request.POST.get('message')
        message = re.sub(" +", " ", message)
        if len(message) > 2000:
            return redirect(f'/messager/?u={user_with}')
        Message(
            sender=request.user,
            receiver=User.objects.get(id=int(user_with)),
            users=f'{request.user.id} {User.objects.get(id=int(user_with)).id}',
            message=message,
            datetime=datetime.now(),
        ).save()


def get_messages(request) -> HttpResponse:
    """
    Retrieve last message from database and returns it in HttpResponse.
    """

    if len(Message.objects.all()) != 0:
        last_message = Message.objects.all().order_by("-datetime")[0]
        last_message = {
            'id': last_message.id,
            'message': last_message.message,
            'receiver_id': last_message.receiver.id,
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


def delete_message_page(request) -> HttpResponse:
    """
    Delete message page.
    """

    message_id = request.GET.get('message_id', None)
    if message_id is not None:
        delete_message(request, message_id)
    if request.META.get('HTTP_REFERER') is not None:
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('/messager/')


def delete_message(request, message_id: int):
    """
    Deletes Message object from data base by id.
    """

    message = Message.objects.get(id=message_id)
    if request.user.id == message.sender_id:
        message.delete()


def black_list_page(request) -> HttpResponse:
    """
    Black list page.
    """

    user_id = request.GET.get('u', None)

    if user_id is not None:
        black_list(request, user_id)

    return redirect(f'/messager?u={user_id}')


def black_list(request, user_id: int):
    """
    Adds user to request user's black list by id.
    """

    if request.user.id != int(user_id):
        if str(user_id) not in request.user.profile.black_list.split(' '):
            request.user.profile.black_list = add_number_to_string_list(request.user.profile.black_list, user_id)
        else:
            request.user.profile.black_list = remove_number_from_string_list(request.user.profile.black_list, user_id)
        request.user.save()
