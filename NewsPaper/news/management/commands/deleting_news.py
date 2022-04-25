from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    # показывает подсказку при вводе "python manage.py <команда> --help"
    help = 'Подсказка вашей команды'
    missing_args_message = 'Недостаточно аргументов'

    # напоминать ли о миграциях. Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)
    requires_migrations_checks = True

    def add_arguments(self, parser):
        # Позиционные аргументы (метод add_argument наследуется от BaseCommand)
        parser.add_argument('category',  # пришедший аргумент будет сохранён под ключом category в словаре option
                            type=str)  # приведение аргумента к указанному типу

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no > ')

        # просто добавил ещё один вариант
        if answer not in ('yes', 'y'):
            self.stdout.write(self.style.ERROR('Отменено'))
            return

        try:
            # выбираем категорию по имени, которое берём из словаря options
            # (именованные аргументы, которые передаются в функцию)
            category = Category.objects.get(name_category=options['category'])

        # в случае, если категории с таким названием не найдено:
        except Category.DoesNotExist:
            raise CommandError(f'Категория отсутствует {options["category"]}')

        # выбираем все посты, которые соответствуют этой категории и удаляем
        Post.objects.filter(category=category).delete()

        # если всё ок - выводим сообщение
        self.stdout.write(self.style.SUCCESS(
            f'Successfully deleted all news from category {category.name_category}'))
