from decouple import config
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Cria automáticamente um superusuário utilizando variáveis do .env.

    Uso:
        poetry run python manage.py createadmin

    Exemplo de .env:
        DJANGO_ADMIN_EMAIL=admin@example.com
        DJANGO_ADMIN_PASSWORD=admin123
        DJANGO_ADMIN_USERNAME=admin
    """

    help = "Cria um superusuário automaticamente via .env"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        email = config("DJANGO_ADMIN_EMAIL", default=None)
        password = config("DJANGO_ADMIN_PASSWORD", default=None)
        username = config("DJANGO_ADMIN_USERNAME", default="admin")

        if not email or not password:
            self.stdout.write(
                self.style.error(
                    "ERRO: Defina DJANGO_ADMIN_EMAIL e DJANGO_ADMIN_PASSWORD no .env"
                )
            )
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"Superusuário com email {email} já existe. Nada a fazer."
                )
            )
            return

        self.stdout.write(self.style.SUCCESS("Criando superusuário..."))

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            role="admin",
        )

        self.stdout.write(
            self.style.SUCCESS(f"Superusuário criado com sucesso: {email}")
        )
