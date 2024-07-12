from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Django команда для создания суперпользователя с заданным номером телефона, если он не существует.

    Если пользователь с указанным номером телефона уже существует, выводится сообщение об этом.

    Methods:
        handle: Основной метод команды, который выполняет создание пользователя и установку пароля.
    """

    def handle(self, *args, **kwargs):
        """
        Создает суперпользователя с номером телефона '123456', если такой не существует.
        """
        phone_number = "123456"
        if not User.objects.filter(phone_number=phone_number).exists():
            user = User.objects.create(
                phone_number=phone_number,
                first_name="Admin",
                last_name="Admin",
                is_staff=True,
                is_superuser=True,
            )

            user.set_password("Admin")
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Суперпользователь с phone_number "{phone_number}" успешно создан.'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'Пользователь с phone_number "{phone_number}" уже существует.'
                )
            )
