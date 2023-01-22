from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.users'
    verbose_name = 'Пользователи'

    def ready(self) -> None:
        from src.users import signals
