from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config


class Command(BaseCommand):
    """
    Cria automaticamente um usuário comum (student ou teacher) via variáveis do .env.

    Uso:
        poetry run python manage.py createuser --role=student
        poetry run python manage.py createuser --role=teacher

    Exemplo de .env:
        DJANGO_USER_EMAIL=aluno@example.com
        DJANGO_USER_PASSWORD=aluno123
        DJANGO_USER_USERNAME=aluno
    """

    help = "Cria um usuário comum automaticamente via .env (student ou teacher)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--role",
            type=str,
            choices=["student", "teacher"],
            required=True,
            help="Papel do usuário (student ou teacher)",
        )

    def handle(self, *args, **options):
        User = get_user_model()

        email = config("DJANGO_USER_EMAIL", default=None)
        password = config("DJANGO_USER_PASSWORD", default=None)
        username = config("DJANGO_USER_USERNAME", default="user")
        role = options["role"]

        if not email or not password:
            self.stdout.write(
                self.style.ERROR(
                    "ERRO: Defina DJANGO_USER_EMAIL e DJANGO_USER_PASSWORD no .env"
                )
            )
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"Usuário com email {email} já existe. Nada a fazer."
                )
            )
            return

        self.stdout.write(self.style.SUCCESS(f"Criando usuário {role}..."))

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
        )

        self.stdout.write(
            self.style.SUCCESS(f"Usuário {role} criado com sucesso: {email}")
        )
