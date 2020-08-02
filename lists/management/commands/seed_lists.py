import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models

NAME = "lists"


class Command(BaseCommand):

    # 해당 py file이 어떤 역할을 하는지에 대한 설명
    help = f"This command creates {NAME}"

    # 해당 python 의 arg를 추가해준다. 이 경우는 필요없다.
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help=f"how many {NAME} do you want to create",
        )

    # arg에 따라 실행해줄 동작을 정의한다.
    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        seeder.add_entity(
            list_models.List, number, {"user": lambda x: random.choice(users),},
        )
        created = seeder.execute()
        cleaned = flatten(list(created.values()))
        for pk in cleaned:
            list_model = list_models.List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]
            list_model.rooms.add(
                *to_add
            )  # *을 붙이게 되면, 해당 array의 요소를 모두 추가하게 된다. 아닐 경우 배열 자체가 추가된다.
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
