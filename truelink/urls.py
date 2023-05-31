"""truelink URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('id<int:user_id>/', views.user_page, name="user"),
    path('id<int:user_id>/delete_post', views.delete_post_page),
    path('id<int:user_id>/add_friend/', views.users_add_friend_page),
    path('id<int:user_id>/remove_friend/', views.users_remove_friend_page),
    path('id<int:user_id>/settings/', views.profile_settings_page, name='profile'),
    path('id<int:user_id>/private/', views.private_settings_page, name='private'),
    path('id<int:user_id>/gallery/', views.gallery_page, name='gallery'),
    path('id<int:user_id>/gallery/delete_image', views.delete_image_page),
    path('id<int:user_id>/friends/', views.friends_page, name='friends'),
    path('id<int:user_id>/groups/', views.groups_page, name='groups'),
    path('', views.landing_page),
    path('logout/', views.logout_page),
    path('messager/', views.messager_page),
    path('messager/black_list', views.black_list_page),
    path('delete_message/', views.delete_message_page),
    path('delete_server_message/', views.delete_server_message_page),
    path('feed/', views.feed_page),
    path('forgot_password/', views.forgot_password_page),
    path('servers/', views.servers_page, name='servers'),
    path('groups/<int:group_id>/', views.group_solo_page, name='group'),
    path('groups/<int:group_id>/follow/', views.follow_group),
    path('groups/<int:group_id>/settings/', views.settings_group),
    path('groups/<int:group_id>/unfollow/', views.unfollow_group),
    path('groups/<int:group_id>/delete_post/', views.delete_group_post_page),
    path('groups/<int:group_id>/delete_group/', views.delete_group_page),
    path('groups/<int:group_id>/members/', views.members_group_page, name='group_members'),
    path('groups/<int:group_id>/ban/', views.group_ban_page),
    path('groups/<int:group_id>/kick/', views.group_kick_page),
    path('groups/<int:group_id>/make_admin/', views.group_make_admin_page),
    path('servers/<int:server_id>/', views.server_solo_page, name='server'),
    path('servers/<int:server_id>/settings', views.settings_server),
    path('servers/<int:server_id>/invite/', views.invite_server_page),
    path('servers/<int:server_id>/handle_invite/', views.invite_server_handler_page),
    path('servers/<int:server_id>/leave/', views.leave_server_page),
    path('servers/<int:server_id>/delete_server/', views.delete_server_page),
    path('servers/<int:server_id>/members/', views.members_server_page, name='server_members'),
    path('servers/<int:server_id>/ban/', views.server_ban_page),
    path('servers/<int:server_id>/kick/', views.server_kick_page),
    path('servers/<int:server_id>/make_admin/', views.server_make_admin_page),
    path('__debug__/', include(debug_toolbar.urls)),
    path('create_new_group/', views.create_new_group, name="new_group"),
    path('create_new_server/', views.create_new_server, name="new_server"),
    path('search/', views.search, name='search'),
    path('more_people/', views.more_people),
    path('more_groups/', views.more_groups),
    path('more_servers/', views.more_servers),
    path('error/', views.error_page),
    path('get_messages/', views.get_messages),
    path('get_server_messages/', views.get_server_messages),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'main.views.page_404'
handler403 = 'main.views.page_403'
handler500 = 'main.views.page_500'
