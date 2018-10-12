import xadmin
from .models import BlogUser


class BlogUserAdmin:
    list_display = ('id', 'nickname', 'username', 'email', 'last_login', 'date_joined')
    list_display_links = ('id', 'username')

# xadmin.site.register(BlogUser, BlogUserAdmin)