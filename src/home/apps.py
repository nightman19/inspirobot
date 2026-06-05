from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    
    name = 'home'


    def ready(self):
        from django.contrib.auth.models import User

        if not User.objects.filter(username="nuru").exists():
            User.objectd.create_user(
                username="nuru",
                password="test1234"
            )
