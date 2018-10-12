import xadmin
from .models import commands


class CommandsAdmin:
    list_display = ('title', 'command', 'describe')


xadmin.site.register(commands, CommandsAdmin)
