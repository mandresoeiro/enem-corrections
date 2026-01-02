from getpass import getpass

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Cria um superusuário de forma interativa.

    Uso:
        poetry run python manage.py createsuperuser

    O comando solicita:
        - Username
        - Email
        - Senha (confirmação)
    """

    help = "Cria um novo superusuário de forma interativa"

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            type=str,
            help="Username do superusuário",
        )
        parser.add_argument(
            "--email",
            type=str,
            help="Email do superusuário",
        )
        parser.add_argument(
            "--password",
            type=str,
            help="Senha do superusuário (não recomendado por segurança)",
        )

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Pega os argumentos ou solicita interativamente
        username = kwargs.get("username")
        email = kwargs.get("email")
        password = kwargs.get("password")

        # Se não fornecidos via argumentos, solicita interativamente
        if not username:
            username = input("Username: ")

        if not email:
            email = input("Email: ")

        if not password:
            while True:
                password = getpass("Senha: ")
                password_confirm = getpass("Confirme a senha: ")

                if password == password_confirm:
                    break
                else:
                    self.stdout.write(
                        self.style.ERROR("Senhas não coincidem. Tente novamente.")
                    )

        # Validações básicas
        if not username or not email or not password:
            self.stdout.write(self.style.ERROR("Todos os campos são obrigatórios!"))
            return

        # Verifica se já existe
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.ERROR(f'Usuário com username "{username}" já existe!')
            )
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.ERROR(f'Usuário com email "{email}" já existe!')
            )
            return

        # Cria o superusuário
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                role="admin",
            )

            self.stdout.write(
                self.style.SUCCESS(f'✅ Superusuário "{username}" criado com sucesso!')
            )
            self.stdout.write(f"   📧 Email: {email}")
            self.stdout.write(f"   🔑 ID: {user.id}")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao criar superusuário: {str(e)}"))
