from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        phone_number = '123456'
        if not User.objects.filter(phone_number=phone_number).exists():
            user = User.objects.create(
                phone_number=phone_number,
                first_name='Admin',
                last_name='Admin',
                is_staff=True,
                is_superuser=True
            )

            user.set_password('Admin')
            user.save()
        else:
            print(f'Пользователь с phone_number "{phone_number}" уже существует.')
