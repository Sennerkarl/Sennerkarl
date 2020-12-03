from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self): # making signals work
        import users.signals
