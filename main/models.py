"""
Django models inherited from models.Model
"""

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Message(models.Model):
    """
    Stores user's private messages.

    :param sender: User object, the one who send message
    :param receiver: User object, the one who get message
    :param users: str, sender and receiver ids (e.g. '1 2')
    :param message: str, message
    :param datetime: 'datetime.datetime()', date of creating
    """

    sender = models.ForeignKey(User, related_name="sender", null=True, on_delete=models.SET_NULL)
    receiver = models.ForeignKey(User, related_name="receiver", null=True, on_delete=models.SET_NULL)
    users = models.TextField()
    message = models.TextField()
    datetime = models.DateTimeField()


class Friend(models.Model):
    """
    Stores user's friends.

    :param users: User objects, other users
    :param current_user: User object, request user
    """

    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name="owner", null=True, on_delete=models.CASCADE)

    @classmethod
    def make_friend(cls, current_user: User, new_friend: User):
        """
        Adds Friend to User friends.
        """

        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def remove_friend(cls, current_user: User, new_friend: User):
        """
        Removes Friend from User friends.
        """

        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)

    def __str__(self) -> str:
        """
        String output of class Friend
        """

        return str(self.current_user)


class UserPost(models.Model):
    """
    Stores user's posts.

    :param user: User object, the one who owns post
    :param datetime: 'datetime.datetime()', date of creating
    :param link_to_img: str, link to img in media
    :param likes: int, amount of likes
    :param liked_by: str, line of user's that liked the post
    :param text: str, post's text
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    link_to_img = models.TextField()
    likes = models.IntegerField()
    liked_by = models.TextField(default='')
    text = models.TextField()


class Profile(models.Model):
    """
    Stores user's profile.

    :param user: User object, profile owner
    :param pfp_link: str, link to profile picture in media
    :param groups: str, ids of groups user is member of
    :param groups_inv: str, ids of groups user sent invite to
    :param servers: str, ids of servers user is member of
    :param servers_inv: str, ids of servers user sent invite to
    :param black_list: str, id' of users blocked by user
    :param posts_liked: str, id' of user posts liked by user
    :param group_posts_liked: str, id' of group posts liked by user
    :param age: int, user's age
    :param friends_visible: bool, defines user's friends visibility to other users
    :param groups_visible: bool, defines user's groups visibility to other users
    :param last_name_visible: bool, defines user's last_name visibility to other users
    :param age_visible: bool, defines user's age visibility to other users
    :param gallery_visible: bool, defines user's gallery visibility to other users
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pfp_link = models.TextField()
    groups = models.TextField(default='')
    groups_inv = models.TextField(default='')
    servers = models.TextField(default='')
    servers_inv = models.TextField(default='')
    black_list = models.TextField(default='')
    posts_liked = models.TextField(default='')
    group_posts_liked = models.TextField(default='')
    age = models.IntegerField(default=0)
    about_me = models.TextField(default='')
    friends_visible = models.BooleanField(default=True)
    groups_visible = models.BooleanField(default=True)
    last_name_visible = models.BooleanField(default=False)
    age_visible = models.BooleanField(default=False)
    gallery_visible = models.BooleanField(default=True)


class Group(models.Model):
    """
    Stores groups.

    :param name: str, group's name
    :param creator: User object, the one who owns group
    :param members: str, ids of group members
    :param invitations: str, ids of members, that dropped a request to join group
    :param bans: str, ids of banned users
    :param admins: str, ids of group admins
    :param link_to_img: str, link to img in media
    :param datetime: 'datetime.datetime()', date of creating
    :param visible: bool, defines group's posts visibility to users that are not members
    """

    name = models.TextField()
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    members = models.TextField()
    invitations = models.TextField(default="")
    bans = models.TextField(default="")
    admins = models.TextField()
    link_to_img = models.TextField(default='/static/images/default_pfp.jpg')
    datetime = models.DateTimeField()
    visible = models.BooleanField()


class GroupPost(models.Model):
    """
    Stores groups posts.

    :param group: Group object, post's group
    :param user: User object, the one who created post
    :param text: str, post's text
    :param likes: int, post's likes
    :param liked_by: str, ids of user's that liked the post
    :param link_to_img: str, link to img in media
    :param datetime: 'datetime.datetime()', date of creating
    """

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    text = models.TextField()
    likes = models.IntegerField()
    liked_by = models.TextField(default='')
    link_to_img = models.TextField()
    datetime = models.DateTimeField()


class GalleryImage(models.Model):
    """
    Stores users images.

    :param user: User object, the one who owns image
    :param link_to_img: str, link to img in media
    :param datetime: 'datetime.datetime()', date of creating
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link_to_img = models.TextField()
    datetime = models.DateTimeField()


class Server(models.Model):
    """
    Stores servers.

    :param name: str, server's name
    :param members: str, ids of server members
    :param invitations: str, ids of members, that dropped a request to join server
    :param bans: str, ids of banned users
    :param creator: User object, the one who owns server
    :param admins: str, ids of server admins
    :param chats: str, ids of server chats
    :param link_to_img: str, link to img in media
    :param datetime: 'datetime.datetime()', date of creating
    :param closed: bool, defines if users need to send request for joining
    """

    name = models.TextField()
    members = models.TextField()
    invitations = models.TextField(default="")
    bans = models.TextField(default="")
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    admins = models.TextField()
    chats = models.TextField()
    link_to_img = models.TextField(default='/static/images/default_pfp.jpg')
    datetime = models.DateTimeField()
    closed = models.BooleanField()


class ServerChat(models.Model):
    """
    Stores servers chats.

    :param name: str, chats's name
    :param server: Server object, chat's server
    :param datetime: 'datetime.datetime()', date of creating
    """

    name = models.TextField()
    server = models.ForeignKey(Server, null=True, on_delete=models.CASCADE)
    datetime = models.DateTimeField()


class ServerMessage(models.Model):
    """
    Stores servers messages.

    :param server: Server object, message's server
    :param chat: ServerChat object, message's chat
    :param message: str, text
    :param sender: User object, the one, who sent message
    :param datetime: 'datetime.datetime()', date of creating
    """

    server = models.ForeignKey(Server, null=True, on_delete=models.CASCADE)
    chat = models.ForeignKey(ServerChat, null=True, on_delete=models.CASCADE)
    message = models.TextField()
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    datetime = models.DateTimeField()


@receiver(post_save, sender=User)
def create_user_profile(sender: User, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender: User, instance, **kwargs):
    instance.profile.save()
