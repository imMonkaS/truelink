"""
Functions and imports.
"""

from datetime import datetime

from PIL import Image

import re
import typing

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from django.db import IntegrityError
from django.contrib import messages

from main.models import Message, Friend, UserPost, Group, GroupPost, Server, ServerMessage,\
    ServerChat, GalleryImage


months = {
    '1': "Января",
    '2': "Февраля",
    '3': "Марта",
    '4': "Апреля",
    '5': "Мая",
    '6': "Июня",
    '7': "Июля",
    '8': "Августа",
    '9': "Сентября",
    '10': "Октября",
    '11': "Ноября",
    '12': "Декабря",
}

image_formats = [
    'TIFF',
    'PJP',
    'JFIF',
    'SVG',
    'BMP',
    'PNG',
    'JPEG',
    'SVGZ',
    'JPG',
    'WEBP',
    'ICO',
    'XBM',
    'DIB',
    'TIF',
    'PJPEG',
    'AVIF',
]


def set_context(request, page_title: str) -> typing.Dict:
    """
    Defines basic page context.
    """

    context = {
        'user': request.user,
        'title': page_title,
        'isAnon': True if str(request.user) == 'AnonymousUser' else False,
    }
    return context


def add_number_to_string_list(str_line: str, num_to_add: int) -> str:
    """
    Adds integer to a string of numbers divided by space. Returns new string.
    """

    tmp_list = str_line.split(' ') if len(str_line) != 0 else []
    tmp_list.append(str(num_to_add))
    return ' '.join(str(el) for el in tmp_list)


def remove_number_from_string_list(str_line: str, num_to_add: int) -> str:
    """
    Removes integer from string of numbers divided by space. Returns new string.
    """

    tmp_list = str_line.split(' ') if len(str_line) != 0 else []
    tmp_list.remove(str(num_to_add))
    return ' '.join(str(el) for el in tmp_list)


def list_friends(user_id: int) -> typing.List:
    """
    Returns a list of Friend objects.
    """

    friend_object, created = Friend.objects.get_or_create(current_user=User.objects.get(id=user_id))
    friends = [friend for friend in friend_object.users.all() if friend != User.objects.get(id=user_id)]
    return friends
